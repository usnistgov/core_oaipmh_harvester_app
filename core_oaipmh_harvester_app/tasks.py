""" OAI-PMH Harvester tasks
"""
import logging
from itertools import chain

from celery import current_app
from celery import shared_task

from core_main_app.commons.exceptions import DoesNotExist
from core_oaipmh_harvester_app.components.oai_registry import api as oai_registry_api
from core_oaipmh_harvester_app.settings import WATCH_REGISTRY_HARVEST_RATE

logger = logging.getLogger(__name__)


def init_harvest():
    """ Init harvest process.
    """
    # Revoke all scheduled tasks
    _revoke_all_scheduled_tasks()

    # Init all registry is_queued to False in case of a server reboot after an issue.
    registries = oai_registry_api.get_all_activated_registry()
    for registry in registries:
        registry.is_queued = False
        oai_registry_api.upsert(registry)

    # Watch Registries
    watch_registry_harvest_task.apply_async()


@shared_task(name='watch_registry_harvest_task')
def watch_registry_harvest_task():
    """ Check each WATCH_REGISTRY_HARVEST_RATE seconds if new registries need to be harvested.
    """
    try:
        logger.info('START watching registries.')
        registries = oai_registry_api.get_all_activated_registry()
        # We launch the background task for each registry
        for registry in registries:
            # If we need to harvest and a task doesn't already exist for this registry.
            if registry.harvest and not registry.is_queued:
                harvest_task.apply_async((str(registry.id),))
                registry.is_queued = True
                oai_registry_api.upsert(registry)
                logger.info('Registry {0} has been queued and will be harvested.'.
                            format(registry.name))
        logger.info('FINISH watching registries.')
    except Exception as e:
        logger.error('ERROR : Error while watching new registries to harvest: {0}'.format(
            str(e)))
    finally:
        # Periodic call every WATCH_REGISTRY_HARVEST_RATE seconds
        watch_registry_harvest_task.apply_async(countdown=WATCH_REGISTRY_HARVEST_RATE)


@shared_task(name='harvest_task')
def harvest_task(registry_id):
    """ Manage the harvest process of the given registry. Check if the harvest should continue.
    Args:
        registry_id: Registry id.

    """
    try:
        registry = oai_registry_api.get_by_id(registry_id)
        # Check if the registry is activated and has to be harvested.
        if registry.is_activated and registry.harvest:
            _harvest_registry(registry)
        else:
            _stop_harvest_registry(registry)
    except DoesNotExist:
        logger.error('ERROR: Registry {0} does not exist anymore. '
                     'Harvesting stopped.'.format(registry_id))


def _harvest_registry(registry):
    """ Harvest the given registry and schedule the next run based on the registry configuration.
    1st: Update the registry information (Name, metadata formats, sets ..).
    2nd: Harvest records.

    Args:
        registry: Registry to harvest.

    """
    try:
        logger.info('START harvesting registry: {0}'.format(registry.name))
        if not registry.is_updating:
            oai_registry_api.update_registry_info(registry)
        if not registry.is_harvesting:
            oai_registry_api.harvest_registry(registry)
        logger.info('FINISH harvesting registry: {0}'.format(registry.name))
    except Exception as e:
        logger.error('ERROR : Impossible to harvest the registry {0}: '
                     '{1}.'.format(registry.name, str(e)))
    finally:
        # Harvest again in harvest_rate seconds.
        harvest_task.apply_async((str(registry.id),), countdown=registry.harvest_rate)


def _stop_harvest_registry(registry):
    """ Stop the harvest process for the given registry.
    Args:
        registry: Registry to stop harvest process.

    """
    try:
        registry.is_queued = False
        oai_registry_api.upsert(registry)
        logger.info('Harvesting for Registry {0} has been deactivated.'.format(registry.name))
    except Exception as e:
        logger.error('ERROR : Error while stopping the harvest process for the registry {0}: '
                     '{1}.'.format(registry.name, str(e)))


def _revoke_all_scheduled_tasks():
    """ Revoke all OAI-PMH scheduled tasks. Avoid having duplicate tasks when the server reboot.
    """
    try:
        logger.info('START revoking OAI-PMH scheduled tasks.')
        if current_app.control.inspect().scheduled() is not None:
            list_tasks = _get_all_oai_tasks_full_name()
            current_app.control.revoke(
                [scheduled["request"]["id"] for scheduled in
                 chain.from_iterable(iter(list(current_app.control.inspect().scheduled().values())))
                 if scheduled["request"]["name"] in list_tasks])
        else:
            logger.warning('Impossible to retrieve scheduled tasks. Is Celery started?')
        logger.info('FINISH revoking OAI-PMH scheduled tasks.')
    except Exception as e:
        logger.error('ERROR : Error while revoking the scheduled tasks: {0}'
                     .format(str(e)))


def _get_all_oai_tasks_full_name():
    """ Get all OAI-PMH tasks name.

    Returns:
        List of OAI-PMH tasks name.

    """
    return [watch_registry_harvest_task.__name__, harvest_task.__name__]
