"""
OaiRegistry API
"""
import logging
from rest_framework import status
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from core_main_app.commons import exceptions
from core_main_app.utils.datetime import datetime_now
from core_oaipmh_common_app.commons import exceptions as oai_pmh_exceptions
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from core_oaipmh_common_app.utils import UTCdatetime
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import (
    api as oai_harvester_metadata_format_api,
)
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format_set import (
    api as oai_harvester_metadata_format_set_api,
)
from core_oaipmh_harvester_app.components.oai_harvester_set import (
    api as oai_harvester_set_api,
)
from core_oaipmh_harvester_app.components.oai_identify import (
    api as oai_identify_api,
)
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_registry.models import (
    OaiRegistry,
)
from core_oaipmh_harvester_app.components.oai_verbs import api as oai_verbs_api
from core_oaipmh_harvester_app.system import api as oai_harvester_system_api

logger = logging.getLogger(__name__)


def upsert(oai_registry):
    """Creates or updates an OaiRegistry.

    Args:
        oai_registry: The OaiRegistry to create or update

    Returns: The OaiRegistry instance.

    """
    oai_registry.save()
    return oai_registry


def get_by_id(oai_registry_id):
    """Returns an OaiRegistry by its id

    Args:
        oai_registry_id: OaiRegistry id.

    Returns: The OaiRegistry instance.

    Raises:
        DoesNotExist: The registry doesn't exist
        ModelError: Internal error during the process

    """
    return OaiRegistry.get_by_id(oai_registry_id)


def get_by_name(oai_registry_name):
    """Returns an OaiRegistry by its name.

    Args:
        oai_registry_name: OaiRegistry name.

    Returns: The OaiRegistry instance.

    Raises:
        DoesNotExist: The registry doesn't exist
        ModelError: Internal error during the process

    """
    return OaiRegistry.get_by_name(oai_registry_name=oai_registry_name)


def get_all():
    """Returns all OaiRegistry

    Returns:
        List of OaiRegistry

    """
    return OaiRegistry.get_all()


def get_all_activated_registry(order_by_field=None):
    """Returns all activated OaiRegistry.

    Returns:
        List of OaiRegistry

    """
    return OaiRegistry.get_all_by_is_activated(
        is_activated=True,
        order_by_field=order_by_field if order_by_field else [],
    )


def check_registry_url_already_exists(oai_registry_url):
    """Checks if an OaiRegistry with the given url already exists.

    Returns:
        Yes or No (bool).

    """
    return OaiRegistry.check_registry_url_already_exists(
        oai_registry_url=oai_registry_url
    )


def delete(oai_registry):
    """Deletes an OaiRegistry

    Args:
        oai_registry: OaiRegistry to delete

    """
    oai_registry.delete()


def add_registry_by_url(url, harvest_rate, harvest, request=None):
    """Adds a registry in database. Takes care of all surrounding objects. Uses OAI-PMH verbs to gather information.

    Args:
        url: Url of the registry to add.
        harvest_rate: Harvest rate. Use to harvest data every harvest_rate seconds.
        harvest: True or False.
        request:

    Returns:
        The OaiRegistry instance.

    """
    registry = None
    if check_registry_url_already_exists(url):
        raise oai_pmh_exceptions.OAIAPINotUniqueError(
            message="Unable to create the data provider."
            " The data provider already exists."
        )

    identify_response = _get_identify_as_object(url)
    sets_response = _get_sets_as_object(url)
    metadata_formats_response = _get_metadata_formats_as_object(url)

    try:
        registry = _init_registry(
            url,
            harvest,
            harvest_rate,
            identify_response.repository_name,
            identify_response.description,
        )
        upsert(registry)
        _upsert_identify_for_registry(identify_response, registry)
        for set_ in sets_response:
            _upsert_set_for_registry(set_, registry)
        for metadata_format in metadata_formats_response:
            _upsert_metadata_format_for_registry(
                metadata_format, registry, request=request
            )

        return registry
    except Exception as exception:
        # Manual Rollback
        if registry.pk is not None:
            registry.delete()

        raise oai_pmh_exceptions.OAIAPILabelledException(
            message=str(exception), status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )


def update_registry_info(registry, request=None):
    """Updates information of a registry in database by its id.

    Args:
        registry: OaiRegistry to update.
        request:

    Returns:
        The OaiRegistry instance.

    """
    # If registry is already updating, skip for now
    if registry.is_updating:
        return []

    registry.is_updating = True
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
            _upsert_metadata_format_for_registry(
                metadata_format, registry, request=request
            )
        # Check if we have some deleted set
        _handle_deleted_set(registry.id, sets_response)
        # Check if we have some deleted metadata format
        _handle_deleted_metadata_format(registry.id, metadata_formats_response)
        registry.is_updating = False
        upsert(registry)

        return registry
    except Exception as exception:
        registry.is_updating = False
        upsert(registry)
        raise oai_pmh_exceptions.OAIAPILabelledException(
            message=str(exception),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def harvest_registry(registry):
    """Harvests the registry given in parameter.
    Args:
        registry: The registry to harvest.

    Returns:
        all_errors: List of errors.

    """
    # If registry is already harvesting, skip for now
    if registry.is_harvesting:
        return []

    try:
        # We are harvesting
        registry.is_harvesting = True
        upsert(registry)
        # Set the last update date
        harvest_date = datetime_now()
        # Get all metadata formats to harvest
        metadata_formats = oai_harvester_metadata_format_api.get_all_to_harvest_by_registry_id(
            registry.id
        )
        # Get all sets
        registry_all_sets = oai_harvester_set_api.get_all_by_registry_id(
            registry.id, "set_name"
        )
        # Get all available sets
        registry_sets_to_harvest = (
            oai_harvester_set_api.get_all_to_harvest_by_registry_id(
                registry.id, "set_name"
            )
        )
        # Check if we have to retrieve all sets or not. If all sets, no need to
        # provide theset parameter in the harvest request.
        #
        # Avoid to retrieve same records if records are in many sets.
        search_by_sets = len(registry_all_sets) != len(
            registry_sets_to_harvest
        )
        # Search by sets
        if search_by_sets and len(registry_all_sets) != 0:
            all_errors = _harvest_by_metadata_formats_and_sets(
                registry,
                metadata_formats,
                registry_sets_to_harvest,
                registry_all_sets,
            )
        # If we don't have to search by set or the OAI Registry doesn't support sets
        else:
            all_errors = _harvest_by_metadata_formats(
                registry, metadata_formats, registry_all_sets
            )
        # Stop harvesting
        registry.is_harvesting = False
        # Set the last update date
        registry.last_update = harvest_date
        upsert(registry)

        return all_errors
    except Exception as exception:
        registry.is_harvesting = False
        upsert(registry)
        raise oai_pmh_exceptions.OAIAPILabelledException(
            message=str(exception),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def _get_identify_as_object(url):
    """Returns the identify information for the given URL.

    Args:
        url: URL.

    Returns:
        identify_response: identify response.

    """
    identify_response, status_code = oai_verbs_api.identify_as_object(url)
    if status_code != status.HTTP_200_OK:
        raise oai_pmh_exceptions.OAIAPILabelledException(
            message=identify_response[OaiPmhMessage.label],
            status_code=status_code,
        )
    return identify_response


def _get_sets_as_object(url):
    """Returns the sets information for the given URL.

    Args:
        url: URL.

    Returns:
        sets_response: ListSet response.

    """
    sets_response, status_code = oai_verbs_api.list_sets_as_object(url)
    if status_code not in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT):
        raise oai_pmh_exceptions.OAIAPILabelledException(
            message=sets_response[OaiPmhMessage.label], status_code=status_code
        )
    if status_code == status.HTTP_204_NO_CONTENT:
        sets_response = []

    return sets_response


def _get_metadata_formats_as_object(url):
    """Returns the metadata formats information for the given URL.

    Args:
        url: URL.

    Returns:
        metadata_formats_response: ListMetadataFormat response.

    """
    (
        metadata_formats_response,
        status_code,
    ) = oai_verbs_api.list_metadata_formats_as_object(url)
    if status_code not in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT):
        raise oai_pmh_exceptions.OAIAPILabelledException(
            message=metadata_formats_response[OaiPmhMessage.label],
            status_code=status_code,
        )
    if status_code == status.HTTP_204_NO_CONTENT:
        metadata_formats_response = []

    return metadata_formats_response


def _init_registry(url, harvest, harvest_rate, repository_name, description):
    """Returns an init OaiRegistry object.

    Args:
        url: url of the registry.
        harvest: True or False
        harvest_rate: Harvest rate. Use to harvest data every harvest_rate seconds.
        repository_name: Repository name.
        description: Description.

    Returns:
        The OaiRegistry instance.

    """
    registry = OaiRegistry(
        name=repository_name,
        url=url,
        harvest_rate=harvest_rate,
        description=description,
        harvest=harvest,
        is_activated=True,
    )
    return registry


def _upsert_identify_for_registry(identify, registry):
    """Adds or updates an identify object for a registry.

    Args:
        identify: OaiIdentify instance.
        registry: OaiRegistry instance.

    """
    try:
        identify_db = oai_identify_api.get_by_registry_id(registry.id)
        identify.id = identify_db.id
    except exceptions.DoesNotExist:
        pass

    identify.registry = registry
    oai_identify_api.upsert(identify)


def _upsert_metadata_format_for_registry(
    metadata_format, registry, request=None
):
    """Adds or updates an OaiHarvesterMetadataFormat object for a registry.

    Args:
        metadata_format: OaiHarvesterMetadataFormat instance.
        registry: OaiRegistry instance.
        request:

    """
    try:
        metadata_format_to_save = oai_harvester_metadata_format_api.get_by_metadata_prefix_and_registry_id(
            metadata_format.metadata_prefix, registry.id
        )
        # Update current OaiHarvesterMetadataFormat
        metadata_format_to_save.metadata_namespace = (
            metadata_format.metadata_namespace
        )
        metadata_format_to_save.schema = metadata_format.schema
        metadata_format_to_save.raw = metadata_format.raw
    except exceptions.DoesNotExist:
        # Creation OaiHarvesterMetadataFormat
        metadata_format_to_save = metadata_format
        metadata_format_to_save.registry = registry
        metadata_format_to_save.harvest = True

    try:
        metadata_format_to_save = (
            oai_harvester_metadata_format_api.init_schema_info(
                metadata_format_to_save, request=request
            )
        )
        oai_harvester_metadata_format_api.upsert(metadata_format_to_save)
    except exceptions.ApiError as exception:
        # Log exception. Do not save the metadata format.
        logger.warning(
            "_upsert_metadata_format_for_registry threw an exception: %s",
            str(exception),
        )


def _upsert_set_for_registry(set_, registry):
    """Adds or updates an OaiHarvesterSet object for a registry.

    Args:
        set_: OaiHarvesterSet instance.
        registry: OaiRegistry instance.

    """
    try:
        set_to_save = oai_harvester_set_api.get_by_set_spec_and_registry_id(
            set_.set_spec, registry.id
        )
        # Update current OaiHarvesterSet
        set_to_save.set_name = set_.set_name
        set_to_save.raw = set_.raw
    except exceptions.DoesNotExist:
        # Creation OaiHarvesterSet
        set_to_save = set_
        set_to_save.registry = registry
        set_to_save.harvest = True

    oai_harvester_set_api.upsert(set_to_save)


def _harvest_by_metadata_formats_and_sets(
    registry, metadata_formats, registry_sets_to_harvest, registry_all_sets
):
    """Harvests data by metadata formats and sets.

    Args:
        registry: Registry.
        metadata_formats: List of metadata formats to harvest.
        registry_sets_to_harvest: List of sets to harvest.
        registry_all_sets: List of all sets.

    Returns:
        List of potential errors.

    """
    all_errors = []

    for metadata_format in metadata_formats:
        current_update_mf = datetime_now()
        errors_during_harvest = False

        for set_ in registry_sets_to_harvest:
            current_update_mf_set = datetime_now()
            try:
                # Retrieve the last update for this metadata format and this set
                last_update = oai_harvester_metadata_format_set_api.get_last_update_by_metadata_format_and_set(
                    metadata_format, set_
                )
            except Exception:
                last_update = None

            errors = _harvest_records(
                registry, metadata_format, last_update, registry_all_sets, set_
            )
            # If no exceptions was thrown and no errors occurred, we can update the last_update date
            if len(errors) == 0:
                oai_harvester_metadata_format_set_api.upsert_last_update_by_metadata_format_and_set(
                    metadata_format, set_, current_update_mf_set
                )
            else:
                errors_during_harvest = True
                all_errors.append(errors)

        # Set the last update date if no exceptions was thrown
        # Would be useful if we do a _harvest_by_metadata_formats in the
        # future: won't retrieve everything
        if not errors_during_harvest:
            metadata_format.last_update = current_update_mf
            oai_harvester_metadata_format_api.upsert(metadata_format)

    return all_errors


def _harvest_by_metadata_formats(
    registry, metadata_formats, registry_all_sets
):
    """Harvests data by metadata formats.
    Args:
        registry: Registry.
        metadata_formats: List of metadata formats to harvest.
        registry_all_sets: List of all sets.

    Returns:
        List of potential errors.

    """
    all_errors = []
    for metadata_format in metadata_formats:
        try:
            # Retrieve the last update for this metadata format
            last_update = UTCdatetime.datetime_to_utc_datetime_iso8601(
                metadata_format.last_update
            )
        except Exception:
            last_update = None
        # Update the new date for the metadataFormat
        current_update_mf = datetime_now()
        errors = _harvest_records(
            registry, metadata_format, last_update, registry_all_sets
        )
        # If no exceptions was thrown and no errors occurred, we can update the last_update date
        if len(errors) == 0:
            # Update the update date for all sets
            # Would be useful if we do a _harvest_by_metadata_formats_and_sets in the future: won't retrieve everything
            if len(registry_all_sets) != 0:
                for set_ in registry_all_sets:
                    oai_harvester_metadata_format_set_api.upsert_last_update_by_metadata_format_and_set(
                        metadata_format, set_, current_update_mf
                    )
            # Update the update date
            metadata_format.last_update = current_update_mf
            oai_harvester_metadata_format_api.upsert(metadata_format)
        else:
            all_errors.append(errors)
    return all_errors


def _harvest_records(
    registry, metadata_format, last_update, registry_all_sets, set_=None
):
    """Harvests records.
    Args:
        registry: Registry to harvest.
        metadata_format: Metadata Format to harvest.
        last_update: Last update date.
        registry_all_sets: List of all sets.
        set_: Set to harvest

    Returns:
        List of potential errors.

    """
    errors = []
    has_data = True
    resumption_token = None
    # Get all records. Use of the resumption token.
    while has_data:
        # Get the list of records
        set_h = None
        if set_ is not None:
            set_h = set_.set_spec

        http_response, resumption_token = oai_verbs_api.list_records(
            url=registry.url,
            metadata_prefix=metadata_format.metadata_prefix,
            set_h=set_h,
            from_date=last_update,
            resumption_token=resumption_token,
        )

        if http_response.status_code == status.HTTP_200_OK:
            try:
                for record in http_response.data:
                    _upsert_record_for_registry(
                        record, metadata_format, registry, registry_all_sets
                    )
            except Exception as exception:
                errors.append(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "error": str(exception),
                    }
                )
        # Else, we get the status code with the error message provided by the http_response
        else:
            error = {
                "status_code": http_response.status_code,
                "error": http_response.data[
                    oai_pmh_exceptions.OaiPmhMessage.label
                ],
            }
            errors.append(error)

        # There is more records if we have a resumption token.
        has_data = resumption_token is not None and resumption_token != ""

    return errors


def _upsert_record_for_registry(
    record, metadata_format, registry, registry_sets
):
    """Adds or updates an OaiRecord object for a registry.

    Args:
        record: Record to update or create.
        metadata_format: OaiHarvesterMetadataFormat instance.
        registry: OaiRegistry instance.

    """
    try:
        record["pk"] = None
        record["xml_content"] = (
            str(record["metadata"]) if record["metadata"] is not None else None
        )

        saved_record = oai_harvester_system_api.get_oai_record_by_identifier_and_metadata_format(
            record["identifier"], metadata_format
        )

        # No xml_content means that the record has been deleted remotely. Do not change
        # the xml_content already in DB.
        if record["xml_content"] is None:
            record["xml_content"] = saved_record.xml_content

        record["pk"] = saved_record.pk
    except exceptions.DoesNotExist:
        pass

    oai_record = OaiRecord(
        identifier=record["identifier"],
        last_modification_date=UTCdatetime.utc_datetime_iso8601_to_datetime(
            record["datestamp"]
        ),
        deleted=record["deleted"],
        xml_content=record["xml_content"],
        registry=registry,
        harvester_metadata_format=metadata_format,
    )

    if record["pk"] is not None:
        oai_record.pk = record["pk"]

    oai_harvester_system_api.upsert_oai_record(oai_record)

    oai_record.harvester_sets.set(
        [x for x in registry_sets if x.set_spec in record["sets"]]
    )

    return oai_record


def _handle_deleted_set(registry_id, sets_response):
    """Delete previous sets not used anymore.
    Args:
        registry_id:
        sets_response:

    Returns:

    """
    sets_in_database = oai_harvester_set_api.get_all_by_registry_id(
        registry_id
    )
    sets_to_delete = [
        x
        for x in sets_in_database
        if x.set_spec not in [y.set_spec for y in sets_response]
    ]
    for set_ in sets_to_delete:
        oai_harvester_set_api.delete(set_)


def _handle_deleted_metadata_format(registry_id, metadata_formats_response):
    """Delete previous metadata formats not used anymore.
    Args:
        registry_id:
        metadata_formats_response:

    Returns:

    """
    metadata_formats_in_database = (
        oai_harvester_metadata_format_api.get_all_by_registry_id(registry_id)
    )
    metadata_formats_to_delete = [
        x
        for x in metadata_formats_in_database
        if x.metadata_prefix
        not in [y.metadata_prefix for y in metadata_formats_response]
    ]
    for metadata_format in metadata_formats_to_delete:
        oai_harvester_metadata_format_api.delete(metadata_format)
