from django.conf import settings

if not settings.configured:
    settings.configure()

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])
