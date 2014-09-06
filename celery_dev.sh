#!/bin/bash
cd /home/texapi/
source ./vars.sh
cd /var/www/texapi/root/
source /home/texapi/Envs/texapi/bin/activate
export DJANGO_SETTINGS=texapi.settings.development
exec celery -A texapi worker -Q texapi -l info