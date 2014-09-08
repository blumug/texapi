#!/bin/bash
curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz
tar xzf virtualenv-1.10.1.tar.gz
rm virtualenv-1.10.1.tar.gz
python virtualenv-1.10.1/virtualenv.py --no-site-packages venv
rm -rf virtualenv-1.10.1
./update_env_production.sh

./venv/bin/python ./manage.py collectstatic --noinput
./venv/bin/python ./manage.py syncdb --noinput
./venv/bin/python ./manage.py migrate --noinput
