"""
WSGI config for stranke4 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
from os.path import abspath, dirname
import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stranke4.settings")
project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
sys.path.insert(0,abspath(dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'stranke4.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
