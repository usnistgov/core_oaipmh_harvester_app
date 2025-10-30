""" Apps file for setting oai-pmh when app is ready
"""

import sys
from django.apps import AppConfig


class HarvesterAppConfig(AppConfig):
    """Core application settings"""

    name = "core_oaipmh_harvester_app"
    verbose_name = "Core OAI-PMH Harvester App"

    def ready(self):
        """Run when the app is ready

        Returns:

        """

        if "migrate" not in sys.argv and "makemigrations" not in sys.argv:
            from core_oaipmh_harvester_app.discover import (
                init_harvest,
                init_mongo_indexing,
            )

            init_harvest()
            init_mongo_indexing()
