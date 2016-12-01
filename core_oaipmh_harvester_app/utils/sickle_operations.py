"""
    Sickle utils provide tool operation for sickle library
"""

from rest_framework import status
from sickle import Sickle
from sickle.oaiexceptions import NoSetHierarchy, NoMetadataFormat
from core_oaipmh_harvester_app.commons.messages import OaiPmhMessage
from core_oaipmh_harvester_app.utils import sickle_serializers


def sickle_identify(url):
    """ Performs an Oai-Pmh identity request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Data.
        Status code.

    """
    try:
        sickle = Sickle(url)
        identify = sickle.Identify()
        serializer = sickle_serializers.IdentifySerializer(identify)
        return serializer.data, status.HTTP_200_OK
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled('An error occurred when attempting to identify resource: %s'
                                                     % e.message)
        return content, status.HTTP_500_INTERNAL_SERVER_ERROR


def sickle_list_sets(url):
    """ Performs an Oai-Pmh listSet request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Data.
        Status code.

    """
    try:
        sickle = Sickle(url)
        list_sets = sickle.ListSets()
        serializer = sickle_serializers.SetSerializer(list_sets)
        return serializer.data, status.HTTP_200_OK
    except NoSetHierarchy as e:
        content = OaiPmhMessage.get_message_labelled('%s' % e.message)
        return content, status.HTTP_204_NO_CONTENT
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled('An error occurred when attempting to identify resource: %s'
                                                     % e.message)
        return content, status.HTTP_500_INTERNAL_SERVER_ERROR


def sickle_list_metadata_formats(url):
    """ Performs an Oai-Pmh listMetadataFormat request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Data.
        Status code.

    """
    try:
        sickle = Sickle(url)
        list_metadata_formats = sickle.ListMetadataFormats()
        serializer = sickle_serializers.SetSerializer(list_metadata_formats)
        return serializer.data, status.HTTP_200_OK
    except NoMetadataFormat as e:
        # This repository does not support sets
        content = OaiPmhMessage.get_message_labelled('%s' % e.message)
        return content, status.HTTP_204_NO_CONTENT
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled('An error occurred when attempting to identify resource: %s'
                                                     % e.message)
        return content, status.HTTP_500_INTERNAL_SERVER_ERROR
