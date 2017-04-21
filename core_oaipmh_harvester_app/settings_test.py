from django.conf import settings
from os.path import join, dirname, realpath, abspath

if not settings.configured:
    settings.configure()

OAI_HARVESTER_ROOT = dirname(realpath(__file__))

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

SECRET_KEY = "dummy_secret_key"
