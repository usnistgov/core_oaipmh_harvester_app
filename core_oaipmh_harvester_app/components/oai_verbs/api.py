"""
    Oai-PMH verbs API.
"""
from core_oaipmh_harvester_app.utils import sickle_operations, transform_operations
from rest_framework import status


def identify(url):
    """ Performs an Oai-Pmh identity request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Serialized Data.
        Status code.

    """
    return sickle_operations.sickle_identify(url)


def identify_as_object(url):
    """ Performs an Oai-Pmh identity request.

    Args:
        url: URL of the Data Provider.

    Returns:
        OaiIdentify instance.
        Status code.

    """
    data, status_code = identify(url)
    if status_code == status.HTTP_200_OK:
        data = transform_operations.transform_dict_identifier_to_oai_identifier(data)

    return data, status_code


def list_metadata_formats(url):
    """ Performs an Oai-Pmh listMetadataFormat request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Serialized Data.
        Status code.

    """
    return sickle_operations.sickle_list_metadata_formats(url)


def list_metadata_formats_as_object(url):
    """ Performs an Oai-Pmh listMetadataFormat request.

    Args:
        url: URL of the Data Provider.

    Returns:
        List of OaiHarvesterMetadataFormat object.
        Status code.

    """
    data, status_code = list_metadata_formats(url)
    if status_code == status.HTTP_200_OK:
        data = transform_operations.transform_dict_metadata_format_to_oai_harvester_metadata_format(data)

    return data, status_code


def list_sets(url):
    """ Performs an Oai-Pmh listSet request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Serialized Data.
        Status code.

    """
    return sickle_operations.sickle_list_sets(url)


def list_sets_as_object(url):
    """ Performs an Oai-Pmh listSet request.

    Args:
        url: URL of the Data Provider.

    Returns:
        List of OaiHarvesterSet object.
        Status code.

    """
    data, status_code = list_sets(url)
    if status_code == status.HTTP_200_OK:
        data = transform_operations.transform_dict_set_to_oai_harvester_set(data)

    return data, status_code
