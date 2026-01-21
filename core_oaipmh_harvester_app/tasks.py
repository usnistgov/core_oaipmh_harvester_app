""" OAI-PMH Harvester tasks
"""

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def harvest_registries():
    """Check each WATCH_REGISTRY_HARVEST_RATE seconds if new registries need
    to be harvested."""
    from core_oaipmh_harvester_app.components.oai_registry import (
        api as oai_registry_api,
    )
    from core_main_app.utils.datetime import datetime_now, datetime_timedelta

    try:
        registries = oai_registry_api.get_all_activated_registry()
        logger.info("Retrieved %d registries to watch", len(registries))

        # Loop over the registries to update and harvest
        for registry in registries:
            if not registry.harvest:
                logger.info(
                    "Registry %s is not set to be harvested", registry.name
                )
                continue

            if registry.is_harvesting:
                logger.warning(
                    "Registry %s is already being harvested", registry.name
                )
                continue

            next_update_in_seconds = (
                int(
                    (
                        registry.last_update
                        + datetime_timedelta(seconds=registry.harvest_rate)
                        - datetime_now()
                    ).total_seconds()
                )
                if registry.last_update
                else 0
            )

            if next_update_in_seconds > 0:
                logger.warning(
                    "Registry %s cannot be harvested. Next possible update in %d seconds",
                    registry.name,
                    next_update_in_seconds,
                )
                continue

            # Harvest registry
            oai_registry_api.update_registry_info(registry)
            oai_registry_api.harvest_registry(registry)
            logger.info("Registry %s harvested", registry.name)
    except Exception as exception:
        logger.error(
            "ERROR : Error while watching new registries to harvest: %s",
            str(exception),
        )


@shared_task
def index_mongo_oai_record(oai_record_id):
    """Index OaiRecord in MongoDB"""
    try:
        from core_oaipmh_harvester_app.components.oai_record.models import (
            OaiRecord,
        )

        oai_record = OaiRecord.objects.get(pk=oai_record_id)
        try:
            from core_oaipmh_harvester_app.components.mongo.models import (
                MongoOaiRecord,
            )

            mongo_oai_record = MongoOaiRecord.init_mongo_oai_record(oai_record)
            mongo_oai_record.save()
        except Exception as exception:
            logger.error(
                "ERROR : An error occurred while indexing oai record : %s",
                str(exception),
            )
    except Exception as exception:
        logger.error(
            "ERROR : An error occurred while indexing oai record : %s",
            str(exception),
        )


@shared_task
def delete_mongo_oai_record(oai_record_id):
    """Delete Oai Record in MongoDB"""
    try:
        try:
            from core_oaipmh_harvester_app.components.mongo.models import (
                MongoOaiRecord,
            )

            mongo_oai_record = MongoOaiRecord.objects.get(id=oai_record_id)
            mongo_oai_record.delete()
        except Exception as exception:
            logger.error(
                "ERROR : An error occurred while deleting oai record : %s",
                str(exception),
            )
    except Exception as exception:
        logger.error(
            "ERROR : An error occurred while deleting oai record : %s",
            str(exception),
        )
