"""
OaiHarvesterMetadataFormat API
"""

from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import OaiHarvesterMetadataFormat


def upsert(oai_harvester_metadata_format):
    """ Create or update an OaiHarvesterMetadataFormat.

    Args:
        oai_harvester_metadata_format: OaiHarvesterMetadataFormat to create or update.

    Returns: OaiHarvesterMetadataFormat instance.

    """
    return oai_harvester_metadata_format.save()


def delete(oai_harvester_metadata_format):
    """ Delete an OaiHarvesterMetadataFormat.

    Args:
        oai_harvester_metadata_format: OaiHarvesterMetadataFormat to delete.

    """
    oai_harvester_metadata_format.delete()


def get_by_id(oai_harvester_metadata_format_id):
    """ Get an OaiHarvesterMetadataFormat by its id.

    Args:
        oai_harvester_metadata_format_id: The OaiHarvesterMetadataFormat id.

    Returns: OaiHarvesterMetadataFormat instance.

    """
    return OaiHarvesterMetadataFormat.get_by_id(oai_metadata_format_id=oai_harvester_metadata_format_id)


def get_by_metadata_prefix_and_registry_id(metadata_prefix, registry_id):
    """ Get an OaiHarvesterMetadataFormat by its metadata_prefix and registry_id.

    Args:
        metadata_prefix: The metadata prefix.
        registry_id:  The registry id.

    Returns:
        OaiHarvesterMetadataFormat instance.

    """
    return OaiHarvesterMetadataFormat.get_by_metadata_prefix_and_registry_id(metadata_prefix=metadata_prefix,
                                                                             registry_id=registry_id)


def get_all():
    """ Get all OaiHarvesterMetadataFormat.

    Returns:
        List of OaiHarvesterMetadataFormat.

    """
    return OaiHarvesterMetadataFormat.get_all()


def get_all_by_registry_id(registry_id, order_by_field=None):
    """ Get all OaiHarvesterMetadataFormat used by a registry.

    Args:
        registry_id: The registry id.
        order_by_field: Order by field.

    Returns:
        List of OaiHarvesterMetadataFormat.

    """
    return OaiHarvesterMetadataFormat.get_all_by_registry_id(registry_id=registry_id, order_by_field=order_by_field)


def get_all_by_list_registry_ids(list_registry_ids, order_by_field=None):
    """ Return a list of OaiHarvesterMetadataFormat by a list of registry ids. Possibility to order_by the list

    Args:
        list_registry_ids: List of registry ids.
        order_by_field: Order by field.

    Returns:
        List of OaiHarvesterMetadataFormat.

    """
    return OaiHarvesterMetadataFormat.get_all_by_list_registry_ids(list_registry_ids=list_registry_ids,
                                                                   order_by_field=order_by_field)


def get_all_to_harvest_by_registry_id(registry_id, order_by_field=None):
    """ List all OaiHarvesterMetadataFormat to harvest used by a registry

    Args:
        registry_id: The registry id.
        order_by_field: Order by field.

    Returns:
        List of OaiHarvesterMetadataFormat.

    """
    return OaiHarvesterMetadataFormat.get_all_by_registry_id_and_harvest(registry_id=registry_id,
                                                                         harvest=True,
                                                                         order_by_field=order_by_field)


def delete_all_by_registry_id(registry_id):
    """ Delete all OaiHarvesterMetadataFormat used by a registry.

    Args:
        registry_id: The registry id.

    """
    OaiHarvesterMetadataFormat.delete_all_by_registry_id(registry_id)


def update_for_all_harvest_by_registry_id(registry_id, harvest):
    """ Update the harvest for all OaiHarvesterMetadataFormat used by the registry.

    Args:
        registry_id: The registry id.
        harvest: Harvest (True/False).

    """
    OaiHarvesterMetadataFormat.update_for_all_harvest_by_registry_id(registry_id=registry_id, harvest=harvest)


def update_for_all_harvest_by_list_ids(list_oai_metadata_format_ids, harvest):
    """ Update the harvest for all OaiHarvesterMetadataFormat by a list of ids.

    Args:
        list_oai_metadata_format_ids: List of OaiHarvesterMetadataFormat ids.
        harvest: Harvest (True/False)

    """
    OaiHarvesterMetadataFormat.update_for_all_harvest_by_list_ids(list_oai_metadata_format_ids, harvest)
