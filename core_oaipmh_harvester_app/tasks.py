""" OAI-PMH Harvester tasks
"""
import logging
from itertools import chain

from celery import current_app
from celery import shared_task

from core_main_app.commons.exceptions import DoesNotExist
from core_oaipmh_harvester_app.settings import WATCH_REGISTRY_HARVEST_RATE

logger = logging.getLogger(__name__)


def init_harvest():
    """Init harvest process."""
    from core_oaipmh_harvester_app.components.oai_registry import (
        api as oai_registry_api,
    )

    try:
        # Init all registry is_queued to False in case of a server reboot after an issue.
        registries = oai_registry_api.get_all_activated_registry()
        for registry in registries:
            registry.is_queued = False
            oai_registry_api.upsert(registry)

        # Watch Registries
        watch_registry_harvest_task.apply_async()
    except Exception as exc:
        logger.error("Impossible to start harvesting data: %s", str(exc))


@shared_task(name="watch_registry_harvest_task")
def watch_registry_harvest_task():
    """Check each WATCH_REGISTRY_HARVEST_RATE seconds if new registries need
    to be harvested."""
    from core_oaipmh_harvester_app.components.oai_registry import (
        api as oai_registry_api,
    )

    try:
        logger.info("START watching registries.")
        registries = oai_registry_api.get_all_activated_registry()
        # We launch the background task for each registry
        for registry in registries:
            # If we need to harvest and a task doesn't already exist for this
            # registry.
            if registry.harvest and not registry.is_queued:
                harvest_task.apply_async((str(registry.id),))
                registry.is_queued = True
                oai_registry_api.upsert(registry)
                logger.info(
                    f"Registry {registry.name} has been queued and will be "
                    f"harvested."
                )
        logger.info("FINISH watching registries.")
    except Exception as exception:
        logger.error(
            f"ERROR : Error while watching new registries to harvest: %s",
            str(exception),
        )
    finally:
        # Periodic call every WATCH_REGISTRY_HARVEST_RATE seconds
        watch_registry_harvest_task.apply_async(countdown=WATCH_REGISTRY_HARVEST_RATE)


@shared_task(name="harvest_task")
def harvest_task(registry_id):
    """Manage the harvest process of the given registry. Check if the harvest
    should continue.

    Args:
        registry_id: Registry id.
    """
    from core_oaipmh_harvester_app.components.oai_registry import (
        api as oai_registry_api,
    )

    try:
        registry = oai_registry_api.get_by_id(registry_id)
        # Check if the registry is activated and has to be harvested.
        if registry.is_activated and registry.harvest:
            _harvest_registry(registry)
        else:  # Registry should not be harvested
            _stop_harvest_registry(registry)
    except DoesNotExist:
        logger.error(
            f"ERROR: Registry {registry_id} does not exist anymore. "
            "Harvesting stopped."
        )


def _harvest_registry(registry):
    """Harvest the given registry and schedule the next run based on the registry configuration.
    1st: Update the registry information (Name, metadata formats, sets ..).
    2nd: Harvest records.

    Args:
        registry: Registry to harvest.

    """
    from core_oaipmh_harvester_app.components.oai_registry import (
        api as oai_registry_api,
    )

    try:
        logger.info(f"START harvesting registry: {registry.name}")
        if not registry.is_updating and not registry.is_harvesting:
            oai_registry_api.update_registry_info(registry)
            oai_registry_api.harvest_registry(registry)
        else:
            logger.warning(f"Registry {registry.name} is busy. Skipping harvesting...")
        logger.info(f"FINISH harvesting registry: {registry.name}")
    except Exception as exception:
        logger.error(
            f"ERROR : Impossible to harvest registry {registry.name}: %s",
            str(exception),
        )
    finally:
        # Harvest again in harvest_rate seconds.
        harvest_task.apply_async((str(registry.id),), countdown=registry.harvest_rate)


def _stop_harvest_registry(registry):
    """Stop the harvest process for the given registry.
    Args:
        registry: Registry to stop harvest process.

    """
    from core_oaipmh_harvester_app.components.oai_registry import (
        api as oai_registry_api,
    )

    try:
        registry.is_queued = False
        oai_registry_api.upsert(registry)
        logger.info(f"Harvesting for Registry {registry.name} has been deactivated.")
    except Exception as exception:
        logger.error(
            f"ERROR : Error while stopping the harvest process for the registry "
            f"{registry.name}: %s",
            str(exception),
        )


def revoke_all_scheduled_tasks():
    """Revoke all OAI-PMH scheduled tasks. Avoid having duplicate tasks when the
    server reboot."""
    if not current_app.backend.is_async:
        logger.warning(
            "Task 'revoke_all_scheduled_tasks' has been disabled since broker has no async "
            "capabilities"
        )
        return

    try:
        logger.info("START revoking OAI-PMH scheduled tasks.")
        if current_app.control.inspect().scheduled() is not None:
            list_tasks = _get_all_oai_tasks_full_name()
            current_app.control.revoke(
                [
                    scheduled["request"]["id"]
                    for scheduled in chain.from_iterable(
                        iter(list(current_app.control.inspect().scheduled().values()))
                    )
                    if scheduled["request"]["name"] in list_tasks
                ]
            )
        else:
            logger.warning("Impossible to retrieve scheduled tasks. Is Celery started?")
        logger.info("FINISH revoking OAI-PMH scheduled tasks.")
    except Exception as exception:
        logger.error(
            f"ERROR : Error while revoking the scheduled tasks: %s", str(exception)
        )


def _get_all_oai_tasks_full_name():
    """Get all OAI-PMH tasks name.

    Returns:
        List of OAI-PMH tasks name.

    """
    return [watch_registry_harvest_task.__name__, harvest_task.__name__]


@shared_task
def index_mongo_oai_record(oai_record_id):
    """Index OaiRecord in MongoDB"""
    try:
        from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord

        oai_record = OaiRecord.objects.get(pk=oai_record_id)
        try:
            from core_oaipmh_harvester_app.components.mongo.models import MongoOaiRecord

            mongo_oai_record = MongoOaiRecord.init_mongo_oai_record(oai_record)
            mongo_oai_record.save()
        except Exception as exception:
            logger.error(
                f"ERROR : An error occurred while indexing oai record : %s",
                str(exception),
            )
    except Exception as exception:
        logger.error(
            f"ERROR : An error occurred while indexing oai record : %s", str(exception)
        )


@shared_task
def delete_mongo_oai_record(oai_record_id):
    """Delete Oai Record in MongoDB"""
    try:
        try:
            from core_oaipmh_harvester_app.components.mongo.models import MongoOaiRecord

            mongo_oai_record = MongoOaiRecord.objects.get(id=oai_record_id)
            mongo_oai_record.delete()
        except Exception as exception:
            logger.error(
                f"ERROR : An error occurred while deleting oai record : %s",
                str(exception),
            )
    except Exception as exception:
        logger.error(
            f"ERROR : An error occurred while deleting oai record : %s", str(exception)
        )
