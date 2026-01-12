""" Auto discovery of OAI harvester app.
"""

import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from core_main_app.utils.databases.mongo.pymongo_database import (
    init_text_index,
)
from core_oaipmh_harvester_app.components.oai_record.models import (
    OaiRecord,
)
from core_oaipmh_harvester_app.settings import WATCH_REGISTRY_HARVEST_RATE
from core_oaipmh_harvester_app.tasks import harvest_registries

logger = logging.getLogger(__name__)


def init_harvest():
    """Manage the task that will trigger the harvesting of OAI-PMH registries"""

    try:
        # Retrieve the harvesting task schedule (every `WATCH_REGISTRY_HARVEST_RATE / 60`
        # minutes).
        scheduled_minute = max(round(WATCH_REGISTRY_HARVEST_RATE / 60), 1)
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=f"*/{int(scheduled_minute)}",
        )

        try:  # Try to retrieve the task by name if it exists and perform sanity checks.
            harvest_registries_periodic_task = PeriodicTask.objects.get(
                name=harvest_registries.__name__,
            )

            # Ensure the schedule is the same as expected
            if harvest_registries_periodic_task.crontab != schedule:
                harvest_registries_periodic_task.crontab = schedule
                harvest_registries_periodic_task.save()
        except ObjectDoesNotExist:  # Create the task if it does not exist
            PeriodicTask.objects.create(
                crontab=schedule,
                name=harvest_registries.__name__,
                task="core_oaipmh_harvester_app.tasks.harvest_registries",
            )
    except Exception as exc:
        logger.error("Impossible to initialize harvesting: %s", str(exc))


def init_mongo_indexing():
    """Enables auto-indexing of OAI records in MongoDB"""
    try:
        # Only necessary when `MONGODB_INDEXING` is set to `True`.
        if not settings.MONGODB_INDEXING:
            return

        from core_oaipmh_harvester_app.components.mongo.models import (
            MongoOaiRecord,
        )

        # Initialize text index
        init_text_index(MongoOaiRecord)

        # Connect MongoOaiRecord sync methods to OaiRecord signals
        post_save.connect(MongoOaiRecord.post_save_data, sender=OaiRecord)
        post_delete.connect(MongoOaiRecord.post_delete_data, sender=OaiRecord)
    except Exception as exc:
        logger.error("Impossible to initialize MongoDB indexing: %s", str(exc))
