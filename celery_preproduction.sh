#!/bin/bash
cd /home/texapipreprod/
source ./vars.sh
cd /var/www/texapipreprod/root/
source /home/texapipreprod/Envs/texapipreprod/bin/activate
export DJANGO_SETTINGS=texapi.settings.preproduction
exec celery -A texapi worker -Q texapi -l info