"""
OaiHarvesterMetadataFormat API
"""
from rest_framework import status

from core_main_app.commons import exceptions
from core_main_app.components.template import api as api_template
from core_main_app.utils.requests_utils.requests_utils import send_get_request
from core_main_app.utils.xml import get_hash
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)


def upsert(oai_harvester_metadata_format):
    """Create or update an OaiHarvesterMetadataFormat.

    Args:
        oai_harvester_metadata_format: OaiHarvesterMetadataFormat to create or update.

    Returns: OaiHarvesterMetadataFormat instance.

    """
    return oai_harvester_metadata_format.save()


def delete(oai_harvester_metadata_format):
    """Delete an OaiHarvesterMetadataFormat.

    Args:
        oai_harvester_metadata_format: OaiHarvesterMetadataFormat to delete.

    """
    oai_harvester_metadata_format.delete()


def get_by_id(oai_harvester_metadata_format_id):
    """Get an OaiHarvesterMetadataFormat by its id.

    Args:
        oai_harvester_metadata_format_id: The OaiHarvesterMetadataFormat id.

    Returns: OaiHarvesterMetadataFormat instance.

    """
    return OaiHarvesterMetadataFormat.get_by_id(
        oai_harvester_metadata_format_id=oai_harvester_metadata_format_id
    )


def get_by_metadata_prefix_and_registry_id(metadata_prefix, registry_id):
    """Get an OaiHarvesterMetadataFormat by its metadata_prefix and registry_id.

    Args:
        metadata_prefix: The metadata prefix.
        registry_id:  The registry id.

    Returns:
        OaiHarvesterMetadataFormat instance.

    """
    return OaiHarvesterMetadataFormat.get_by_metadata_prefix_and_registry_id(
        metadata_prefix=metadata_prefix, registry_id=registry_id
    )


def get_all():
    """Get all OaiHarvesterMetadataFormat.

    Returns:
        List of OaiHarvesterMetadataFormat.

    """
    return OaiHarvesterMetadataFormat.get_all()


def get_all_by_registry_id(registry_id, order_by_field=None):
    """Get all OaiHarvesterMetadataFormat used by a registry.

    Args:
        registry_id: The registry id.
        order_by_field: Order by field.

    Returns:
        List of OaiHarvesterMetadataFormat.

    """
    return OaiHarvesterMetadataFormat.get_all_by_registry_id(
        registry_id=registry_id, order_by_field=order_by_field
    )


def get_all_by_list_registry_ids(list_registry_ids, order_by_field=None):
    """Return a list of OaiHarvesterMetadataFormat by a list of registry ids. Possibility to order_by the list

    Args:
        list_registry_ids: List of registry ids.
        order_by_field: Order by field.

    Returns:
        List of OaiHarvesterMetadataFormat.

    """
    return OaiHarvesterMetadataFormat.get_all_by_list_registry_ids(
        list_registry_ids=list_registry_ids, order_by_field=order_by_field
    )


def get_all_to_harvest_by_registry_id(registry_id, order_by_field=None):
    """List all OaiHarvesterMetadataFormat to harvest used by a registry

    Args:
        registry_id: The registry id.
        order_by_field: Order by field.

    Returns:
        List of OaiHarvesterMetadataFormat.

    """
    return OaiHarvesterMetadataFormat.get_all_by_registry_id_and_harvest(
        registry_id=registry_id, harvest=True, order_by_field=order_by_field
    )


def delete_all_by_registry_id(registry_id):
    """Delete all OaiHarvesterMetadataFormat used by a registry.

    Args:
        registry_id: The registry id.

    """
    OaiHarvesterMetadataFormat.delete_all_by_registry_id(registry_id)


def update_for_all_harvest_by_registry_id(registry_id, harvest):
    """Update the harvest for all OaiHarvesterMetadataFormat used by the registry.

    Args:
        registry_id: The registry id.
        harvest: Harvest (True/False).

    """
    OaiHarvesterMetadataFormat.update_for_all_harvest_by_registry_id(
        registry_id=registry_id, harvest=harvest
    )


def update_for_all_harvest_by_list_ids(list_oai_metadata_format_ids, harvest):
    """Update the harvest for all OaiHarvesterMetadataFormat by a list of ids.

    Args:
        list_oai_metadata_format_ids: List of OaiHarvesterMetadataFormat ids.
        harvest: Harvest (True/False)

    """
    OaiHarvesterMetadataFormat.update_for_all_harvest_by_list_ids(
        list_oai_metadata_format_ids, harvest
    )


def init_schema_info(oai_harvester_metadata_format, request=None):
    """Init schema information for an OaiHarvesterMetadataFormat.

    Args:
        oai_harvester_metadata_format: The OaiHarvesterMetadataFormat to init.
        request:

    Returns:
        Init OaiHarvesterMetadataFormat.

    """
    # TODO: refactor send request with cookies (same code in other apps)
    try:
        session_id = request.session.session_key
    except Exception:
        session_id = None
    http_response = send_get_request(
        oai_harvester_metadata_format.schema, cookies={"sessionid": session_id}
    )
    if http_response.status_code == status.HTTP_200_OK:
        string_xml = http_response.text
        oai_harvester_metadata_format.xml_schema = string_xml
        try:
            oai_harvester_metadata_format.hash = get_hash(string_xml)
        except exceptions.XSDError:
            raise exceptions.ApiError(
                "Impossible to hash the schema for the following "
                "metadata format: {0}."
            )
        list_template = api_template.get_all_accessible_by_hash(
            oai_harvester_metadata_format.hash, request=request
        )
        # FIXME: What to do if several templates with the same hash.
        if len(list_template) == 1:
            oai_harvester_metadata_format.template = list_template[0]
        elif len(list_template) > 1:
            raise exceptions.ApiError(
                "Several templates have the same hash. "
                "Impossible to determine a template for the following "
                "metadata format: {0}.".format(
                    oai_harvester_metadata_format.metadata_prefix
                )
            )
    else:
        raise exceptions.ApiError(
            "Impossible to init schema information for the following "
            "metadata format: {0}.".format(
                oai_harvester_metadata_format.metadata_prefix
            )
        )

    return oai_harvester_metadata_format
