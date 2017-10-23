from django.conf import settings
from os.path import dirname, realpath

if not settings.configured:
    settings.configure()

OAI_HARVESTER_ROOT = dirname(realpath(__file__))

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

# Rate in seconds
WATCH_REGISTRY_HARVEST_RATE = 60
