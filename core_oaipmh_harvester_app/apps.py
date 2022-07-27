""" Apps file for setting oai-pmh when app is ready
"""
import sys

from django.apps import AppConfig

from core_oaipmh_harvester_app.tasks import init_harvest, revoke_all_scheduled_tasks


class HarvesterAppConfig(AppConfig):
    """Core application settings"""

    name = "core_oaipmh_harvester_app"
    verbose_name = "Core OAI-PMH Harvester App"

    def ready(self):
        """Run when the app is ready

        Returns:

        """
        if "migrate" not in sys.argv and "makemigrations" not in sys.argv:
            # Revoke all scheduled tasks
            revoke_all_scheduled_tasks()
            init_harvest()
