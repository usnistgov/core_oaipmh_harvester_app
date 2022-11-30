"""
OaiRecord API
"""
from django.conf import settings

from core_main_app.access_control import api as main_access_control_api
from core_main_app.access_control.decorators import access_control
from core_main_app.settings import DATA_SORTING_FIELDS
from core_main_app.utils.query.mongo.prepare import (
    convert_to_django,
)
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
def execute_json_query(json_query, user, order_by_field=DATA_SORTING_FIELDS):
    """Converts JSON query to ORM syntax and call execute query.

    Args:
        json_query:
        user:
        order_by_field:

    Returns:

    """
    # convert JSON query to Django syntax
    query = convert_to_django(query_dict=json_query)

    if settings.MONGODB_INDEXING:
        from core_oaipmh_harvester_app.components.mongo.api import (
            execute_mongo_query,
        )

        return execute_mongo_query(query, user, order_by_field)

    # execute query and return results
    return execute_query(query, user, order_by_field)
