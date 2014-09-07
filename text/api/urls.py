from django.conf.urls import *

urlpatterns = patterns(
    'text.api.views',
    url(r'^analyze/$', 'analyze', name='api_text_analyze'),
)
