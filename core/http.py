from django.conf import settings
from django.contrib.sites.models import Site

import logging
logger = logging.getLogger("core")


def absolute_url(url):
    """
    return absolute url :

    /myurl --> https://xxx.com/myurl

    """
    if url is None:
        return None
    current_site = Site.objects.get_current()
    protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
    absolute_url = u"%s://%s%s" % (protocol, unicode(current_site.domain), url)
    return absolute_url
