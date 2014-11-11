from django.conf.urls import *

urlpatterns = patterns(
    'text.api.views',
    url(r'^analyze/$', 'analyze', name='api_text_analyze'),

    url(r'^$', 'texts', name='api_texts'),
    url(r'^(?P<task_id>[-\w]+)/$', 'text', name='api_text'),
)
