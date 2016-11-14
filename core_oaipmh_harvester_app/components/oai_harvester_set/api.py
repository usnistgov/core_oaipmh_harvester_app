"""
OaiHarvesterSet API
"""

from core_oaipmh_harvester_app.components.oai_harvester_set.models import OaiHarvesterSet
from core_main_app.commons import exceptions
from core_main_app.utils.xml import raw_xml_to_dict


def save_or_update(set_spec, registry, set_name, raw, harvest=None):
    """
    Create or update an OaiHarvesterSet
    :param set_spec:
    :param set_name:
    :param raw:
    :param registry:
    :param harvest:
    :return:
    """
    try:
        oai_harvester_set = get_by_set_spec_and_registry(set_spec=set_spec, registry=registry)
        oai_harvester_set = _update(oai_harvester_set, set_name=set_name, raw=raw, harvest=harvest)
    except exceptions.ApiError:
        oai_harvester_set = _save(set_spec=set_spec, registry=registry, set_name=set_name, raw=raw, harvest=True)

    return oai_harvester_set


def get_by_id(oai_harvester_set_id):
    """
    Get an OaiHarvesterSet
    :param oai_harvester_set_id:
    :return:
    """
    try:
        return OaiHarvesterSet.get_by_id(oai_set_id=oai_harvester_set_id)
    except:
        raise exceptions.ApiError('No OaiHarvesterSet could be found with the given id')


def get_by_set_spec_and_registry(set_spec, registry):
    """
    Get an OaiHarvesterSet by setSpec and registry
    :param set_spec:
    :param registry:
    :return:
    """
    try:
        return OaiHarvesterSet.get_by_set_spec_and_registry(set_spec=set_spec,
                                                            registry=registry)
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


def _save(set_spec, set_name, raw, registry, harvest):
    """
    Create an OaiHarvesterSet
    :param set_spec:
    :param set_name:
    :param raw:
    :param registry:
    :param harvest:
    :return:
    """
    dict_raw = raw_xml_to_dict(raw)
    new_oai_harvester_set = OaiHarvesterSet.create_oai_harvester_set(set_spec=set_spec,
                                                                     set_name=set_name,
                                                                     raw=dict_raw,
                                                                     registry=registry,
                                                                     harvest=harvest)
    return new_oai_harvester_set


def _update(oai_harvester_set, set_name, raw, harvest=None):
    """
    Update an OaiHarvesterSet
    :param oai_harvester_set:
    :param set_name:
    :param raw:
    :param harvest:
    :return:
    """
    oai_harvester_set.raw = raw_xml_to_dict(raw)
    oai_harvester_set.setName = set_name
    if harvest is not None:
        oai_harvester_set.harvest = harvest

    oai_harvester_set.update_object()
    return oai_harvester_set
