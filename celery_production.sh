#!/bin/bash
cd /home/texapi/
source ./vars.sh
cd /var/www/texapi/root/
source /var/www/texapi/root/venv/bin/activate
export DJANGO_SETTINGS=texapi.settings.production
exec celery -A texapi worker -Q texapi -l info