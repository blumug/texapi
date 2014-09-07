from fabric.api import *
import fabtools.require

from fabtools.vagrant import vagrant


@task
def upgrade():

    # Update packages list and upgrade system before running install
    sudo("apt-get -q update")
    sudo("aptitude -q -y safe-upgrade")


@task
def install():

    fabtools.require.deb.packages([
        'python',
        'build-essential',
        'devscripts',
        'locales',
        'nginx',
        'sqlite3',
        'ruby',
        'curl',
        'git',
        'gcc',
        'python-dev',
        'python-psycopg2',
        'python-lxml',
        'libxml2-dev',
        'libxslt1-dev',
        'libpq-dev',
        'libpng-dev',
        'libjpeg-dev',
        'zlib1g-dev',
        'memcached',
        'openjdk-7-jre-headless',
        'enchant',
    ], update=False)

    sudo("cp /vagrant/wkhtmltopdf /usr/bin/")

    fabtools.require.system.locale('fr_FR.UTF-8')
    fabtools.require.postgres.server()
    fabtools.require.postgres.user('vagrant', 'vagrant', createrole=True)
    fabtools.require.postgres.database('texapi', 'vagrant')
    fabtools.require.postgres.database('jor', 'vagrant')
    fabtools.require.redis.instance('texapi')

    if not fabtools.files.is_file('.pgpass'):
        run('echo "*:*:texapi:texapi:texapi" >> .pgpass')
        run('chmod 0600 .pgpass')

    install_nodejs()

    with cd('/texapi/'):
        run('./install.sh')


@task
def install_nodejs():
    fabtools.require.nodejs.installed_from_source()
    if fabtools.files.is_file('/usr/local/bin/bower') is False:
        sudo("npm install -g bower")
    if fabtools.files.is_file('/usr/local/bin/grunt') is False:
        sudo("npm install -g grunt")
        sudo("npm install -g grunt-cli")


@task
def run_server():
    with cd('/texapi'):
        run('source ./venv/bin/activate && ./manage.py runserver 0.0.0.0:8000')


@task
def test():
    with cd('/texapi'):
        run('source ./venv/bin/activate && ./manage.py test')


@task
def create_superuser():
    with cd('/texapi/'):
        run('source ./venv/bin/activate && ./manage.py createsuperuser')


@task
def deploy_dev():
    with cd('/texapi/'):
        run('source ./venv/bin/activate && fab dev deploy')


@task
def deploy_preprod():
    with cd('/texapi/'):
        run('source ./venv/bin/activate && fab preprod deploy')


@task
def deploy_prod():
    with cd('/texapi/'):
        run('source ./venv/bin/activate && fab prod deploy')
