from django.conf import settings
from os.path import join, dirname, realpath

if not settings.configured:
    settings.configure()

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

OAI_HARVESTER_ROOT = dirname(realpath(__file__))