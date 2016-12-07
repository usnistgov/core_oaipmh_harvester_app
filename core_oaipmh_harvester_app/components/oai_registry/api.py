"""
OaiRegistry API
"""


from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.commons import exceptions as oai_pmh_exceptions
from core_oaipmh_harvester_app.commons.messages import OaiPmhMessage
from core_oaipmh_harvester_app.components.oai_verbs import api as oai_verbs_api
from rest_framework import status
from core_oaipmh_harvester_app.components.oai_identify import api as api_oai_identify
from core_oaipmh_harvester_app.components.oai_identify import api as oai_identify_api
from core_oaipmh_harvester_app.components.oai_harvester_set import api as oai_harvester_set_api
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import api as oai_harvester_metadata_format_api
from core_main_app.commons import exceptions


def upsert(oai_registry):
    """ Create or update an OaiRegistry.

    Args:
        oai_registry: The OaiRegistry to create or update

    Returns: The OaiRegistry instance.

    """
    return oai_registry.save()


def get_by_id(oai_registry_id):
    """ Get an OaiRegistry by its id

    Args:
        oai_registry_id: OaiRegistry id.

    Returns: The OaiRegistry instance.

    Raises:
        DoesNotExist: The registry doesn't exist
        ModelError: Internal error during the process

    """
    return OaiRegistry.get_by_id(oai_registry_id)


def get_by_name(oai_registry_name):
    """ Get an OaiRegistry by its name.

    Args:
        oai_registry_name: OaiRegistry name.

    Returns: The OaiRegistry instance.

    Raises:
        DoesNotExist: The registry doesn't exist
        ModelError: Internal error during the process

    """
    return OaiRegistry.get_by_name(oai_registry_name=oai_registry_name)


def get_all():
    """ Return all OaiRegistry

    Returns:
        List of OaiRegistry

    """
    return OaiRegistry.get_all()


def get_all_activated_registry(order_by_field=None):
    """ Return all activated OaiRegistry.

        Returns:
            List of OaiRegistry

        """
    return OaiRegistry.get_all_by_is_activated(is_activated=True, order_by_field=order_by_field)


def check_registry_url_already_exists(oai_registry_url):
    """ Check if an OaiRegistry with the given url already exists.

    Returns:
        Yes or No (bool).

    """
    return OaiRegistry.check_registry_url_already_exists(oai_registry_url=oai_registry_url)


def delete(oai_registry):
    """ Delete an OaiRegistry

    Args:
        oai_registry: OaiRegistry to delete

    """
    oai_registry.delete()


def add_registry_by_url(url, harvest_rate, harvest):
    """ Add a registry in database. Take care of all surrounding objects. Use OAI-PMH verbs to gather information.

    Args:
        url: Url of the registry to add.
        harvest_rate: Harvest rate. Use to harvest data every harvest_rate seconds.
        harvest: True or False.

    Returns:
        The OaiRegistry instance.

    """
    registry = None
    if check_registry_url_already_exists(url):
        raise oai_pmh_exceptions.OAIAPINotUniqueError(message='Unable to create the data provider.'
                                                              ' The data provider already exists.')
    identify_response = _get_identify_as_object(url)
    sets_response = _get_sets_as_object(url)
    metadata_formats_response = _get_metadata_formats_as_object(url)

    try:
        registry = _init_registry(url, harvest, harvest_rate, identify_response.repository_name,
                                  identify_response.description)
        registry = upsert(registry)
        _upsert_identify_for_registry(identify_response, registry)
        for set_ in sets_response:
            _upsert_set_for_registry(set_, registry)
        for metadata_format in metadata_formats_response:
            _upsert_metadata_format_for_registry(metadata_format, registry)

        return registry
    except Exception as e:
        # Manual Rollback
        if registry is not None:
            registry.delete()
        raise oai_pmh_exceptions.OAIAPILabelledException(message=e.message,
                                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_registry_info(registry):
    """ Update information of a registry in database by its id.

        Args:
            registry: OaiRegistry to update.

        Returns:
            The OaiRegistry instance.

        """
    registry.isUpdating = True
    upsert(registry)
    identify_response = _get_identify_as_object(registry.url)
    sets_response = _get_sets_as_object(registry.url)
    metadata_formats_response = _get_metadata_formats_as_object(registry.url)

    try:
        _upsert_identify_for_registry(identify_response, registry)
        registry.name = identify_response.repository_name
        registry.description = identify_response.description
        upsert(registry)
        for set_ in sets_response:
            _upsert_set_for_registry(set_, registry)
        for metadata_format in metadata_formats_response:
            _upsert_metadata_format_for_registry(metadata_format, registry)
        registry.isUpdating = False
        upsert(registry)

        return registry
    except Exception as e:
        registry.isUpdating = False
        upsert(registry)
        raise oai_pmh_exceptions.OAIAPILabelledException(message=e.message,
                                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_identify_as_object(url):
    """ Get the identify information for the given URL.

    Args:
        url: URL.

    Returns:
        identify_response: identify response.

    """
    identify_response, status_code = oai_verbs_api.identify_as_object(url)
    if status_code != status.HTTP_200_OK:
        raise oai_pmh_exceptions.OAIAPILabelledException(message=identify_response[OaiPmhMessage.label],
                                                         status_code=status_code)
    return identify_response


def _get_sets_as_object(url):
    """ Get the sets information for the given URL.

    Args:
        url: URL.

    Returns:
        sets_response: ListSet response.

    """
    sets_response, status_code = oai_verbs_api.list_sets_as_object(url)
    if status_code not in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT):
        raise oai_pmh_exceptions.OAIAPILabelledException(message=sets_response[OaiPmhMessage.label],
                                                         status_code=status_code)
    return sets_response


def _get_metadata_formats_as_object(url):
    """ Get the metadata formats information for the given URL.

    Args:
        url: URL.

    Returns:
        metadata_formats_response: ListMetadataFormat response.

    """
    metadata_formats_response, status_code = oai_verbs_api.list_metadata_formats_as_object(url)
    if status_code not in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT):
        raise oai_pmh_exceptions.OAIAPILabelledException(
            message=metadata_formats_response[OaiPmhMessage.label],
            status_code=status_code)
    return metadata_formats_response


def _init_registry(url, harvest, harvest_rate, repository_name, description):
    """ Return an init OaiRegistry object.

    Args:
        url: url of the registry.
        harvest: True or False
        harvest_rate: Harvest rate. Use to harvest data every harvest_rate seconds.
        repository_name: Repository name.
        description: Description.

    Returns:
        The OaiRegistry instance.

    """
    registry = OaiRegistry()
    registry.name = repository_name
    registry.url = url
    registry.harvest_rate = harvest_rate
    registry.description = description
    registry.harvest = harvest
    registry.is_activated = True

    return registry


def _upsert_identify_for_registry(identify, registry):
    """ Add or update an identify object for a registry.

    Args:
        identify: OaiIdentify instance.
        registry: OaiRegistry instance.

    """
    try:
        identify_db = oai_identify_api.get_by_registry_id(registry.id)
        identify.id = identify_db.id
    except exceptions.DoesNotExist:
        identify.registry = registry

    api_oai_identify.upsert(identify)


def _upsert_metadata_format_for_registry(metadata_format, registry):
    """ Add or update an OaiHarvesterMetadataFormat object for a registry.

    Args:
        metadata_format: OaiHarvesterMetadataFormat instance.
        registry: OaiRegistry instance.

    """
    try:
        metadata_format_to_save = oai_harvester_metadata_format_api.\
            get_by_metadata_prefix_and_registry_id(metadata_format.metadata_prefix, registry.id)
        # Update current OaiHarvesterMetadataFormat
        metadata_format_to_save.metadata_namespace = metadata_format.metadata_namespace
        metadata_format_to_save.schema = metadata_format.metadata_namespace.schema
        metadata_format_to_save.raw = metadata_format.metadata_namespace.raw
    except exceptions.DoesNotExist:
        # Creation OaiHarvesterMetadataFormat
        metadata_format_to_save = metadata_format
        metadata_format_to_save.registry = registry
        metadata_format_to_save.harvest = True

    try:
        metadata_format_to_save = oai_harvester_metadata_format_api.init_schema_info(metadata_format_to_save)
        oai_harvester_metadata_format_api.upsert(metadata_format_to_save)
    except exceptions.ApiError as e:
        # Log exception. Do not save the metadata format.
        pass


def _upsert_set_for_registry(set_, registry):
    """ Add or update an OaiHarvesterSet object for a registry.

    Args:
        set_: OaiHarvesterSet instance.
        registry: OaiRegistry instance.

    """
    try:
        set_to_save = oai_harvester_set_api.get_by_set_spec_and_registry_id(set_.set_spec, registry.id)
        # Update current OaiHarvesterSet
        set_to_save.set_name = set_.set_name
        set_to_save.raw = set_.raw
    except exceptions.DoesNotExist:
        # Creation OaiHarvesterSet
        set_to_save = set_
        set_to_save.registry = registry
        set_to_save.harvest = True

    oai_harvester_set_api.upsert(set_to_save)
