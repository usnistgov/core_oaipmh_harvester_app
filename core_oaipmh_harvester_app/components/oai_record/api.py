"""
OaiRecord API
"""

from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord


def upsert(oai_record):
    """ Create or update an OaiRecord.

    Args:
        oai_record: OaiRecord to create or update.

        Returns:
            OaiRecord instance.

    """
    if oai_record.deleted:
        oai_record.metadata = {}

    return oai_record.save(metadata=oai_record.metadata)


def get_by_id(oai_record_id):
    """Get an OaiRecord by its id.

    Args:
        oai_record_id: Id of the OaiRecord.

    Returns: The OaiRecord instance.

    """
    return OaiRecord.get_by_id(oai_record_id)


def get_all():
    """ Return all OaiRecord.

    Returns: List of OaiRecord.

    """
    return OaiRecord.get_all()


def get_all_by_registry_id(registry_id, order_by_field=None):
    """ Return a list of OaiRecord by registry id. Possibility to order_by the list.

    Args:
        registry_id: The registry id.
        order_by_field: Order field.

    Returns:
        List of OaiRecord.

    """
    return OaiRecord.get_all_by_registry_id(registry_id, order_by_field)


def get_count_by_registry_id(registry_id):
    """ Return the number of OaiRecord by registry id.

    Args:
        registry_id: The registry id.

    Returns:
        Number of OaiRecord (int).

    """
    return OaiRecord.get_count_by_registry_id(registry_id)


def delete_all_by_registry_id(registry_id):
    """ Delete all OaiRecord of a registry

    Args:
        registry_id: The registry id.

    """
    OaiRecord.delete_all_by_registry_id(registry_id)


def delete(oai_record):
    """ Delete an OaiHarvesterMetadataFormat.

    Args:
        oai_record: OaiRecord to delete.

    """
    oai_record.delete()


def execute_full_text_query(text, list_metadata_format_id):
    """ Execute full text query on OaiRecord data collection.

    Args:
        text: Keywords.
        list_metadata_format_id: List of metadata format id to search on.

    Returns: List of OaiRecord.

    """
    return OaiRecord.execute_full_text_query(text, list_metadata_format_id)
