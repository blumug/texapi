#!/bin/bash
set -e
LOGFILE=/var/www/texapi/logs/guni.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
ADDRESS=127.0.0.1:8011
cd /home/texapi/
source ./vars.sh
cd /var/www/texapi/root/texapi/
source /var/www/texapi/root/venv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn texapi.wsgi:application -w $NUM_WORKERS --bind=$ADDRESS \
  --log-level=debug \
  --pythonpath=/var/www/texapi/root/
  --log-file=$LOGFILE 2>>$LOGFILE