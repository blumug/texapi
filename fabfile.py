import os.path
from fabric.api import *
from fabric.utils import puts
from fabric.contrib.files import sed, uncomment, append, exists


def prod():
    global WEBSITE_PATH
    global APP_PATH
    global GIT_PATH
    global BRANCH
    global DJANGO_MODE
    global VENV

    env.forward_agent = 'True'
    env.hosts = [
        'textapi.rechord.net',
    ]
    env.user = "texapi"

    WEBSITE_PATH = "/var/www/texapi/root/"
    GIT_PATH = "git@github.com:meeloo/textapi.git"
    BRANCH = "master"
    DJANGO_MODE = 'production'
    VENV = 'source /var/www/texapi/root/venv/bin/activate'


def deploy():
    """[DISTANT] Update distant django env
    """
    with cd(WEBSITE_PATH):
        run("git checkout %s" % (BRANCH))
        run("git pull")

    if DJANGO_MODE in ['development', 'production']:
        with cd("%s" % (WEBSITE_PATH)):
            run("source ~/vars.sh %s && ./update_env_production.sh" % (VENV))
            run("source ~/vars.sh && %s && ./manage.py collectstatic --noinput" % (VENV))
            run("source ~/vars.sh && %s && ./manage.py syncdb" % (VENV))
            run("source ~/vars.sh && %s && ./manage.py migrate" % (VENV))
            run("source ~/vars.sh && %s && ./manage.py thumbnail cleanup" % (VENV))
            run("source ~/vars.sh && %s && ./manage.py thumbnail clear" % (VENV))
            run("supervisorctl restart texapi")
