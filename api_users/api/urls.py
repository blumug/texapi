from django.conf.urls import *
from rest_framework import routers

urlpatterns = patterns(
    'api_users.api.views',
    url(r'^login/$', 'login', name='api_login'),
    url(r'^signup/$', 'signup', name='api_signup'),
    url(r'^lost_pword/$', 'lost_password', name='api_lost_password'),
    url(r'^me/$', 'me', name='api_me'),
)
