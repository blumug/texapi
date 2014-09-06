import os.path
from fabric.api import *
from fabric.utils import puts
from fabric.contrib.files import sed, uncomment, append, exists


def dev():
    global WEBSITE_PATH
    global APP_PATH
    global GIT_PATH
    global BRANCH
    global DJANGO_MODE
    global ALLOW_VTENV
    global ES_INDEX_PATH
    

    env.forward_agent = 'True'
    env.hosts = [
        'texapi.jbl2024.com',
    ]
    env.user = "texapi"
    WEBSITE_PATH = "/var/www/texapi/root/"
    GIT_PATH = "git@git.adx.org:blumug/texapi.git"
    BRANCH = "master"
    DJANGO_MODE = 'development'
    ALLOW_VTENV = True
    ES_INDEX_PATH = '/var/www/texapi/root/search/mapping/'


def preprod():
    global WEBSITE_PATH
    global APP_PATH
    global GIT_PATH
    global BRANCH
    global DJANGO_MODE
    global ALLOW_VTENV
    global ES_INDEX_PATH
    

    env.forward_agent = 'True'
    env.hosts = [
        'host1.jbl2024.com',
    ]
    env.user = "texapipreprod"
    
    WEBSITE_PATH = "/var/www/texapipreprod/root/"
    GIT_PATH = "git@git.adx.org:blumug/texapi.git"
    BRANCH = "master"
    DJANGO_MODE = 'preproduction'
    ALLOW_VTENV = True
    ES_INDEX_PATH = '/var/www/texapipreprod/root/search/mapping/'


def prod():
    global WEBSITE_PATH
    global APP_PATH
    global GIT_PATH
    global BRANCH
    global DJANGO_MODE
    global ALLOW_VTENV
    global ES_INDEX_PATH

    env.forward_agent = 'True'
    env.hosts = [
        'vps85036.ovh.net',
    ]
    env.user = "texapi"

    WEBSITE_PATH = "/var/www/texapi/root/"
    GIT_PATH = "git@git.adx.org:blumug/texapi.git"
    BRANCH = "master"
    DJANGO_MODE = 'production'
    ALLOW_VTENV = True
    ES_INDEX_PATH = '/var/www/texapi/root/search/mapping/'


def deploy():
    """[DISTANT] Update distant django env
    """
    with cd(WEBSITE_PATH):
        run("git checkout %s" % (BRANCH))
        run("git pull")

    if DJANGO_MODE in ['development', 'production']:
        with cd("%s" % (WEBSITE_PATH)):
            run("source /home/texapi/Envs/texapi/bin/activate && ./update_env_production.sh")
        with cd("%s" % (WEBSITE_PATH)):
            run("source ~/vars.sh && source /home/texapi/Envs/texapi/bin/activate && ./manage.py collectstatic --noinput")
            run("source ~/vars.sh && source /home/texapi/Envs/texapi/bin/activate && ./manage.py syncdb")
            run("source ~/vars.sh && source /home/texapi/Envs/texapi/bin/activate && ./manage.py migrate")
            run("source ~/vars.sh && source /home/texapi/Envs/texapi/bin/activate && ./manage.py thumbnail cleanup")
            run("source ~/vars.sh && source /home/texapi/Envs/texapi/bin/activate && ./manage.py thumbnail clear")
            run("supervisorctl restart texapi")
    elif DJANGO_MODE == 'preproduction':
        with cd("%s" % (WEBSITE_PATH)):
            run("source /home/texapipreprod/Envs/texapipreprod/bin/activate && ./update_env_production.sh")
        with cd("%s" % (WEBSITE_PATH)):
            run("source ~/vars.sh && source /home/texapipreprod/Envs/texapipreprod/bin/activate && ./manage.py collectstatic --noinput")
            run("source ~/vars.sh && source /home/texapipreprod/Envs/texapipreprod/bin/activate && ./manage.py syncdb")
            run("source ~/vars.sh && source /home/texapipreprod/Envs/texapipreprod/bin/activate && ./manage.py migrate")
            run("source ~/vars.sh && source /home/texapipreprod/Envs/texapipreprod/bin/activate && ./manage.py thumbnail cleanup")
            run("source ~/vars.sh && source /home/texapipreprod/Envs/texapipreprod/bin/activate && ./manage.py thumbnail clear")
            run("supervisorctl restart texapipreprod")
