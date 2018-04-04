""" Apps file for setting oai-pmh when app is ready
"""
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from django.apps import AppConfig

from core_main_app.utils.databases.mongoengine_database import init_text_index
from core_oaipmh_harvester_app.tasks import init_harvest


class HarvesterAppConfig(AppConfig):
    """ Core application settings
    """
    name = 'core_oaipmh_harvester_app'

    def ready(self):
        """ Run when the app is ready

        Returns:

        """
        init_text_index(OaiRecord)
        init_harvest()
