import requests
from urlparse import urlparse

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from breadability.readable import Article

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from pyquery import PyQuery as pq
from guess_language import guess_language_name

from core.models import DateTimeModel

import settings as text_settings


class Text(DateTimeModel):

    """ An api user """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    url = models.CharField(_('url'), max_length=512, blank=True)
    raw = models.TextField(_('raw'), blank=True)
    language = models.CharField(_('language'), max_length=50, blank=True)
    summary = models.TextField(_('summary'), blank=True)
    readable = models.TextField(_('readable'), blank=True)
    status = models.CharField(_('layout'), max_length=32,
                              choices=text_settings.TEXT_STATUS_CHOICES,
                              default=text_settings.TEXT_STATUS_PENDING)
    task_id = models.CharField(_('task id'), max_length=255, blank=True)

    def parse(self):
        self._get_raw()
        self._get_readable()
        self._get_language()
        self._get_summary()
        self.save()

    def _fix_images_path(self, html, base_url):
        data = pq(html)
        images = data('img')
        for image in images:
            image = pq(image)
            src = image.attr('src')
            if src is not None:
                if src.startswith('/'):
                    src = u'%s%s' % (base_url, src)
                elif src.startswith('http') is False:
                    src = u'%s/%s' % (base_url, src)
            image.attr('src', src)

        return data.html()

    def _get_raw(self):
        if self.url == '':
            return
        r = requests.get(self.url)
        if r.status_code != 200:
            return

        if 'meta charset="UTF-8"' in r.text or 'meta charset="utf-8"' in r.text or 'meta charset="utf8"' in r.text or "meta charset='utf8'" in r.text:
            r.encoding = 'utf-8'
        self.raw = r.text

    def _get_readable(self):
        if self.raw == '':
            return
        self.readable = Article(self.raw).readable

        base_url = self._get_base_url()
        self.readable = self._fix_images_path(self.readable, base_url)

    def _get_language(self):
        if self.readable == '':
            return
        self.language = guess_language_name(self.readable)

    def _get_summary(self):
        if self.readable == '':
            return

        language = self.language.lower()
        if language == '':
            language = 'english'

        parser = HtmlParser.from_string(
            self.readable, self.url, Tokenizer(language))
        stemmer = Stemmer(language)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(language)
        summary = []
        for sentence in summarizer(parser.document, 10):
            if sentence.is_heading:
                summary.append('<h2>%s</h2>' % (unicode(sentence)))
            else:
                summary.append('<p>%s</p>' % (unicode(sentence)))

        self.summary = ''.join(summary)

    def _get_base_url(self):
        """
        Args:
            self.url: https://medium.com/foo/bar

        Returns:
            base_url: https://medium.com
        """
        if self.url is None:
            return None
        parsed_uri = urlparse(self.url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return domain

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')

    def __unicode__(self):
        return self.url
