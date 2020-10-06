"""
OaiRecord API
"""
from core_main_app.access_control import api as main_access_control_api
from core_main_app.access_control.decorators import access_control
from core_main_app.settings import DATA_SORTING_FIELDS
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord


@access_control(main_access_control_api.can_anonymous_access_public_data)
def get_by_id(oai_record_id, user):
    """Get an OaiRecord by its id.

    Args:
        oai_record_id: Id of the OaiRecord.
        user: user retrieving the ID

    Returns: The OaiRecord instance.

    """
    return OaiRecord.get_by_id(oai_record_id)


def get_all():
    """Return all OaiRecord.

    Returns: List of OaiRecord.

    """
    return OaiRecord.get_all()


def get_all_by_registry_id(registry_id, order_by_field=DATA_SORTING_FIELDS):
    """Return a list of OaiRecord by registry id. Possibility to order_by the list.

    Args:
        registry_id: The registry id.
        order_by_field: Order field.

    Returns:
        List of OaiRecord.

    """
    return OaiRecord.get_all_by_registry_id(registry_id, order_by_field)


@access_control(main_access_control_api.can_anonymous_access_public_data)
def get_count_by_registry_id(registry_id, user):
    """Return the number of OaiRecord by registry id.

    Args:
        registry_id: The registry id.

    Returns:
        Number of OaiRecord (int).

    """
    return OaiRecord.get_count_by_registry_id(registry_id)


def delete_all_by_registry_id(registry_id):
    """Delete all OaiRecord of a registry

    Args:
        registry_id: The registry id.

    """
    OaiRecord.delete_all_by_registry_id(registry_id)


def delete(oai_record):
    """Delete an OaiHarvesterMetadataFormat.

    Args:
        oai_record: OaiRecord to delete.

    """
    oai_record.delete()


@access_control(main_access_control_api.can_anonymous_access_public_data)
def execute_full_text_query(text, list_metadata_format_id, user):
    """Execute full text query on OaiRecord data collection.

    Args:
        text: Keywords.
        list_metadata_format_id: List of metadata format id to search on.

    Returns: List of OaiRecord.

    """
    return OaiRecord.execute_full_text_query(text, list_metadata_format_id)


@access_control(main_access_control_api.can_anonymous_access_public_data)
def execute_query(query, user, order_by_field=DATA_SORTING_FIELDS):
    """Executes a query on the OaiRecord collection.

    Args:
        query: Query to execute.
        user: User executing the query
        order_by_field: Order by Data field

    Returns:
        Results of the query.

    """
    return OaiRecord.execute_query(query, order_by_field)


@access_control(main_access_control_api.can_anonymous_access_public_data)
def aggregate(pipeline, user):
    """Execute an aggregate on the OaiRecord collection.

    Args:
        pipeline:

    Returns:

    """
    return OaiRecord.aggregate(pipeline)
