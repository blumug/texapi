#!venv/bin/python
import sys
import os
from os.path import abspath, dirname, join

PROJECT_ROOT = abspath(dirname(__file__))

user = os.environ.get('USER')

if __name__ == "__main__":
    if 'test' in sys.argv or 'jenkins' in sys.argv:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "texapi.settings.test")
    else:
        if user == 'vagrant':
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "texapi.settings.local")
        elif user == 'texapipreprod':
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "texapi.settings.preproduction")
        else:
            if os.environ.get('DJANGO_MODE', 'production') == 'development':
                os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'texapi.settings.development')
            else:
                os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'texapi.settings.production')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
