"""
    Oai-PMH verbs API.
"""
from core_oaipmh_harvester_app.utils import sickle_operations, transform_operations
from rest_framework import status
from rest_framework.response import Response
from core_oaipmh_harvester_app.commons import exceptions as oai_pmh_exceptions
import requests


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


def get_data(url):
    try:
        if str(url).__contains__('?'):
            registry_url = str(url).split('?')[0]
            data, status_code = identify(registry_url)
            if status_code == status.HTTP_200_OK:
                http_response = requests.get(url)
                if http_response.status_code == status.HTTP_200_OK:
                    return Response(http_response.text, status=status.HTTP_200_OK)
                else:
                    raise oai_pmh_exceptions.OAIAPIException(message='An error occurred.',
                                                             status_code=http_response.status_code)
            else:
                content = 'An error occurred when attempting to identify resource: %s' % data
                raise oai_pmh_exceptions.OAIAPILabelledException(message=content,
                                                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise oai_pmh_exceptions.OAIAPIException(message='An error occurred, url malformed.',
                                                     status_code=status.HTTP_400_BAD_REQUEST)
    except requests.HTTPError, err:
        raise oai_pmh_exceptions.OAIAPILabelledException(message=err.message, status_code=err.response.status_code)
    except oai_pmh_exceptions.OAIAPIException as e:
        raise e
    except Exception as e:
        content = 'An error occurred when attempting to retrieve data: %s' % e.message
        raise oai_pmh_exceptions.OAIAPILabelledException(message=content,
                                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
