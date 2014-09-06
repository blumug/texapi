#!/bin/bash
set -e
LOGFILE=/var/www/texapipreprod/logs/guni.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
ADDRESS=127.0.0.1:8009
cd /home/texapipreprod/
source ./vars.sh
cd /var/www/texapipreprod/root/
source /home/texapipreprod/Envs/texapipreprod/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn texapi.wsgi:application -w $NUM_WORKERS --bind=$ADDRESS \
  --log-level=debug \
  --pythonpath=/var/www/texapipreprod/root/
  --log-file=$LOGFILE 2>>$LOGFILE