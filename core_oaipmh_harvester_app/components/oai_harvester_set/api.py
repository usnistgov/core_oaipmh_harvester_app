"""
OaiHarvesterSet API
"""

from core_oaipmh_harvester_app.components.oai_harvester_set.models import OaiHarvesterSet
from core_main_app.commons import exceptions
from core_main_app.utils.xml import raw_xml_to_dict


def upsert(oai_harvester_set):
    """
    Create or update an OaiHarvesterSet
    :param oai_harvester_set:
    :return:
    """
    try:
        if oai_harvester_set.raw and isinstance(oai_harvester_set.raw, str):
            try:
                oai_harvester_set.raw = raw_xml_to_dict(oai_harvester_set.raw)
            except exceptions.XMLError:
                oai_harvester_set.raw = {}

        return oai_harvester_set.save()
    except:
        raise exceptions.ApiError('Save OaiHarvesterSet failed.')


def delete(oai_harvester_set):
    """
    Delete an OaiHarvesterSet
    :param oai_harvester_set:
    :return:
    """
    try:
        oai_harvester_set.delete()
    except:
        raise exceptions.ApiError('Impossible to delete OaiHarvesterSet.')


def get_by_id(oai_harvester_set_id):
    """
    Get an OaiHarvesterSet by its id
    :param oai_harvester_set_id:
    :return:
    """
    try:
        return OaiHarvesterSet.get_by_id(oai_set_id=oai_harvester_set_id)
    except:
        raise exceptions.ApiError('No OaiHarvesterSet could be found with the given id')


def get_by_set_spec_and_registry(set_spec, registry_id):
    """
    Get an OaiHarvesterSet by its setSpec and registry_id
    :param set_spec:
    :param registry_id:
    :return:
    """
    try:
        return OaiHarvesterSet.get_by_set_spec_and_registry(set_spec=set_spec,
                                                            registry_id=registry_id)
    except:
        raise exceptions.ApiError('No OaiHarvesterSet could be found with the given setSpec and registry')


def get_all():
    """
    List all OaiHarvesterSet
    :return:
    """
    return OaiHarvesterSet.get_all()


def get_all_by_registry(registry, order_by_field=None):
    """
    List all OaiHarvesterSet used by a registry
    :param registry:
    :param order_by_field:
    :return:
    """
    try:
        return OaiHarvesterSet.get_all_by_registry(registry=registry,
                                                   order_by_field=order_by_field)
    except:
        raise exceptions.ApiError('No OaiHarvesterSet could be found with the given registry.')


def get_all_by_list_registry_ids(list_registry_ids, order_by_field=None):
    """
    Return a list of OaiHarvesterSet by a list of registry ids.
    :param list_registry_ids:
    :param order_by_field:
    :return:
    """
    return OaiHarvesterSet.get_all_by_list_registry_ids(list_registry_ids=list_registry_ids,
                                                        order_by_field=order_by_field)


def get_all_to_harvest_by_registry(registry, order_by_field=None):
    """
    List all OaiHarvesterSet to harvest used by a registry
    :param registry:
    :param order_by_field:
    :return:
    """
    try:
        return OaiHarvesterSet.get_all_by_registry_and_harvest(registry=registry,
                                                               harvest=True,
                                                               order_by_field=order_by_field)
    except:
        raise exceptions.ApiError('No OaiHarvesterSet could be found with the given registry.')


def delete_all_by_registry(registry):
    """
    Delete all OaiHarvesterSet used by a registry
    :param registry:
    :return:
    """
    try:
        OaiHarvesterSet.delete_all_by_registry(registry)
    except:
        raise exceptions.ApiError('No OaiHarvesterSet could be found with the given registry.')


def update_for_all_harvest_by_registry(registry, harvest):
    """
    Update the harvest for all OaiHarvesterSet used by the registry
    :param registry:
    :param harvest:
    :return:
    """
    try:
        OaiHarvesterSet.update_for_all_harvest_by_registry(registry=registry, harvest=harvest)
    except:
        raise exceptions.ApiError('No OaiHarvesterSet could be found with the given registry.')


def update_for_all_harvest_by_list_ids(list_oai_set_ids, harvest):
    """
    Update the harvest for all OaiHarvesterSet by a list of ids
    :param list_oai_set_ids:
    :param harvest:
    :return:
    """
    try:
        OaiHarvesterSet.update_for_all_harvest_by_list_ids(list_oai_set_ids, harvest)
    except:
        raise exceptions.ApiError('Something went wrong during the harvest update for the given list of ids.')
