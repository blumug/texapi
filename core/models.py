from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import utc
import datetime


class DateTimeModel(models.Model):
    created = models.DateTimeField(_('created'), editable=False)
    updated = models.DateTimeField(_('updated'), editable=False)

    def save(self, *args, **kwargs):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if not self.id:
            self.created = now
        self.updated = now
        super(DateTimeModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
