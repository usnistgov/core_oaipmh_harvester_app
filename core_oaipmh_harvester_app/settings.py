""" Settings for core_oaipmh_harvester_app.

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from os.path import dirname, realpath

from django.conf import settings

if not settings.configured:
    settings.configure()

INSTALLED_APPS = getattr(settings, "INSTALLED_APPS", [])
""" :py:class:`list`: List of apps installed.
"""

OAI_HARVESTER_ROOT = dirname(realpath(__file__))
""" :py:class:`str`:
"""

SSL_CERTIFICATES_DIR = getattr(settings, "SSL_CERTIFICATES_DIR", "certs")
""" :py:class:`str`: SSL certificates directory location.
"""

WATCH_REGISTRY_HARVEST_RATE = 60
""" :py:calss:`int`: Harvesting rate in seconds.
"""

# Can anonymous access public document
CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = getattr(
    settings, "CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT", False
)
""" :py:class:`bool`: Can anonymous user access public document.
"""
