""" Apps file for setting oai-pmh when app is ready
"""
from django.apps import AppConfig

from core_oaipmh_harvester_app.tasks import init_harvest


class HarvesterAppConfig(AppConfig):
    """ Core application settings
    """
    name = 'core_oaipmh_harvester_app'

    def ready(self):
        """ Run when the app is ready

        Returns:

        """
        init_harvest()
