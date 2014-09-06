from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

user = os.environ.get('USER')

if user == 'vagrant':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'texapi.settings.local')
elif user == 'texapipreprod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'texapi.settings.preproduction')
else:
    if os.environ.get('DJANGO_MODE', 'production') == 'development':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'texapi.settings.development')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'texapi.settings.production')

app = Celery('texapi')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')
