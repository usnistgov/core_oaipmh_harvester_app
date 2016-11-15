"""
OaiHarvesterMetadataFormat API
"""

from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import OaiHarvesterMetadataFormat
from core_main_app.commons import exceptions
from core_main_app.utils.xml import raw_xml_to_dict


def upsert(oai_harvester_metadata_format):
    """
    Create or update an OaiHarvesterMetadataFormat
    :param oai_harvester_metadata_format:
    :return:
    """
    try:
        if oai_harvester_metadata_format.raw and isinstance(oai_harvester_metadata_format.raw, str):
            try:
                oai_harvester_metadata_format.raw = raw_xml_to_dict(oai_harvester_metadata_format.raw)
            except exceptions.XMLError:
                oai_harvester_metadata_format.raw = {}

        return oai_harvester_metadata_format.save()
    except:
        raise exceptions.ApiError('Save OaiHarvesterMetadataFormat failed.')


def delete(oai_harvester_metadata_format):
    """
    Delete an OaiHarvesterMetadataFormat
    :param oai_harvester_metadata_format:
    :return:
    """
    try:
        oai_harvester_metadata_format.delete()
    except:
        raise exceptions.ApiError('Impossible to delete OaiHarvesterMetadataFormat.')


def get_by_id(oai_harvester_metadata_format_id):
    """
    Get an OaiHarvesterMetadataFormat by its id
    :param oai_harvester_metadata_format_id:
    :return:
    """
    try:
        return OaiHarvesterMetadataFormat.get_by_id(oai_metadata_format_id=oai_harvester_metadata_format_id)
    except:
        raise exceptions.ApiError('No OaiHarvesterMetadataFormat could be found with the given id')


def get_by_metadata_prefix_and_registry_id(metadata_prefix, registry_id):
    """
    Get an OaiHarvesterMetadataFormat by its metadata_prefix and registry_id
    :param metadata_prefix:
    :param registry_id:
    :return:
    """
    try:
        return OaiHarvesterMetadataFormat.get_by_metadata_prefix_and_registry_id(metadata_prefix=metadata_prefix,
                                                                                 registry_id=registry_id)
    except:
        raise exceptions.ApiError('No OaiHarvesterMetadataFormat could be found with the given metadata_prefix'
                                  ' and registry id')


def get_all():
    """
    List all OaiHarvesterMetadataFormat
    :return:
    """
    return OaiHarvesterMetadataFormat.get_all()


def get_all_by_registry_id(registry_id, order_by_field=None):
    """
    List all OaiHarvesterMetadataFormat used by a registry
    :param registry_id:
    :param order_by_field:
    :return:
    """
    try:
        return OaiHarvesterMetadataFormat.get_all_by_registry_id(registry_id=registry_id, order_by_field=order_by_field)
    except:
        raise exceptions.ApiError('No OaiHarvesterMetadataFormat could be found with the given registry id.')


def get_all_by_list_registry_ids(list_registry_ids, order_by_field=None):
    """
    Return a list of OaiHarvesterMetadataFormat by a list of registry ids.
    :param list_registry_ids:
    :param order_by_field:
    :return:
    """
    return OaiHarvesterMetadataFormat.get_all_by_list_registry_ids(list_registry_ids=list_registry_ids,
                                                                   order_by_field=order_by_field)


def get_all_to_harvest_by_registry_id(registry_id, order_by_field=None):
    """
    List all OaiHarvesterMetadataFormat to harvest used by a registry
    :param registry_id:
    :param order_by_field:
    :return:
    """
    try:
        return OaiHarvesterMetadataFormat.get_all_by_registry_id_and_harvest(registry_id=registry_id,
                                                                             harvest=True,
                                                                             order_by_field=order_by_field)
    except:
        raise exceptions.ApiError('No OaiHarvesterMetadataFormat could be found with the given registry id.')


def delete_all_by_registry_id(registry_id):
    """
    Delete all OaiHarvesterMetadataFormat used by a registry
    :param registry_id:
    :return:
    """
    try:
        OaiHarvesterMetadataFormat.delete_all_by_registry_id(registry_id)
    except:
        raise exceptions.ApiError('No OaiHarvesterMetadataFormat could be found with the given registry id.')


def update_for_all_harvest_by_registry_id(registry_id, harvest):
    """
    Update the harvest for all OaiHarvesterMetadataFormat used by the registry
    :param registry_id:
    :param harvest:
    :return:
    """
    try:
        OaiHarvesterMetadataFormat.update_for_all_harvest_by_registry_id(registry_id=registry_id, harvest=harvest)
    except:
        raise exceptions.ApiError('No OaiHarvesterMetadataFormat could be found with the given registry id.')


def update_for_all_harvest_by_list_ids(list_oai_metadata_format_ids, harvest):
    """
    Update the harvest for all OaiHarvesterMetadataFormat by a list of ids
    :param list_oai_metadata_format_ids:
    :param harvest:
    :return:
    """
    try:
        OaiHarvesterMetadataFormat.update_for_all_harvest_by_list_ids(list_oai_metadata_format_ids, harvest)
    except:
        raise exceptions.ApiError('Something went wrong during the harvest update for the given list of ids.')
