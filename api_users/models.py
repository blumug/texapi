from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import signals
from django.contrib.auth import get_user_model

from core.models import DateTimeModel


import signals as api_users_signals
from geoposition.fields import GeopositionField


class ApiUser(DateTimeModel):
    """ An api user """
    user = models.OneToOneField(User, verbose_name=_('user'), related_name='api_user')
    facebook_id = models.CharField(_('facebook id'), max_length=255, blank=True)
    facebook_token = models.TextField(_('facebook token'), blank=True)
    twitter_id = models.CharField(_('twitter id'), max_length=200, blank=True)
    twitter_token = models.CharField(_('twitter token'), max_length=255, blank=True)
    twitter_screen_name = models.CharField(_('twitter screen name'), max_length=255, blank=True)
    twitter_token_secret = models.CharField(_('twitter token secret'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('app user')
        verbose_name_plural = _('app users')

    def __unicode__(self):
        return unicode(self.user)


def install_handlers():
    signals.post_save.connect(api_users_signals.create_auth_token, sender=get_user_model())
    signals.post_save.connect(api_users_signals.api_user_updated, sender=ApiUser)
install_handlers()
