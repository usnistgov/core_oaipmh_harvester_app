"""
OaiHarvesterSet API
"""

from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)


def upsert(oai_harvester_set):
    """Create or update an OaiHarvesterSet.

    Args:
        oai_harvester_set: OaiHarvesterSet to create or update.

    Returns: OaiHarvesterSet instance.

    """
    oai_harvester_set.save()
    return oai_harvester_set


def delete(oai_harvester_set):
    """Delete an OaiHarvesterSet.

    Args:
        oai_harvester_set: OaiHarvesterSet to delete.

    """
    oai_harvester_set.delete()


def get_by_id(oai_harvester_set_id):
    """Get an OaiHarvesterSet by its id.

    Args:
        oai_harvester_set_id: The OaiHarvesterSet id.

    Returns: OaiHarvesterSet instance.

    """
    return OaiHarvesterSet.get_by_id(oai_set_id=oai_harvester_set_id)


def get_by_set_spec_and_registry_id(set_spec, registry_id):
    """Get an OaiHarvesterSet by its set_spec and registry_id.

    Args:
        set_spec: The set spec.
        registry_id:  The registry id.

    Returns:
        OaiHarvesterSet instance.

    """
    return OaiHarvesterSet.get_by_set_spec_and_registry_id(
        set_spec=set_spec, registry_id=registry_id
    )


def get_all():
    """Get all OaiHarvesterSet.

    Returns:
        List of OaiHarvesterSet.

    """
    return OaiHarvesterSet.get_all()


def get_all_by_registry_id(registry_id, order_by_field=None):
    """Get all OaiHarvesterSet used by a registry.

    Args:
        registry_id: The registry id.
        order_by_field: Order by field.

    Returns:
        List of OaiHarvesterSet.

    """
    return OaiHarvesterSet.get_all_by_registry_id(
        registry_id=registry_id, order_by_field=order_by_field
    )


def get_all_by_list_registry_ids(list_registry_ids, order_by_field=None):
    """Return a list of OaiHarvesterSet by a list of registry ids. Possibility to order_by the list

    Args:
        list_registry_ids: List of registry ids.
        order_by_field: Order by field.

    Returns:
        List of OaiHarvesterSet.

    """
    return OaiHarvesterSet.get_all_by_list_registry_ids(
        list_registry_ids=list_registry_ids, order_by_field=order_by_field
    )


def get_all_to_harvest_by_registry_id(registry_id, order_by_field=None):
    """List all OaiHarvesterSet to harvest used by a registry

    Args:
        registry_id: The registry id.
        order_by_field: Order by field.

    Returns:
        List of OaiHarvesterSet.

    """
    return OaiHarvesterSet.get_all_by_registry_id_and_harvest(
        registry_id=registry_id, harvest=True, order_by_field=order_by_field
    )


def delete_all_by_registry_id(registry_id):
    """Delete all OaiHarvesterSet used by a registry.

    Args:
        registry_id: The registry id.

    """
    OaiHarvesterSet.delete_all_by_registry_id(registry_id)


def update_for_all_harvest_by_registry_id(registry_id, harvest):
    """Update the harvest for all OaiHarvesterSet used by the registry.

    Args:
        registry_id: The registry id.
        harvest: Harvest (True/False).

    """
    OaiHarvesterSet.update_for_all_harvest_by_registry_id(
        registry_id=registry_id, harvest=harvest
    )


def update_for_all_harvest_by_list_ids(list_oai_set_ids, harvest):
    """Update the harvest for all OaiHarvesterSet by a list of ids.

    Args:
        list_oai_set_ids: List of OaiHarvesterSet ids.
        harvest: Harvest (True/False)

    """
    OaiHarvesterSet.update_for_all_harvest_by_list_ids(list_oai_set_ids, harvest)
