""" Sickle utils provide tool operation for sickle library.
"""
from rest_framework import status
from sickle import Sickle
from sickle.models import Record
from sickle.oaiexceptions import NoSetHierarchy, NoMetadataFormat

from xml_utils.xsd_tree.xsd_tree import XSDTree

from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from core_oaipmh_harvester_app.settings import SSL_CERTIFICATES_DIR
from core_oaipmh_harvester_app.utils import sickle_serializers


def _sickle_init(url):
    """Initialize Sickle object. Allows for proper HTTPS handling, similar to
    core_main_app request_utils.

    Args:
        url: URL of the Data Provider.

    Returns:
        Sickle object
    """
    return Sickle(url, verify=SSL_CERTIFICATES_DIR)


def sickle_identify(url):
    """Performs an Oai-Pmh identity request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Data.
        Status code.

    """
    try:
        sickle = _sickle_init(url)
        identify = sickle.Identify()
        serializer = sickle_serializers.IdentifySerializer(identify)
        return serializer.data, status.HTTP_200_OK
    except Exception as exception:
        content = OaiPmhMessage.get_message_labelled(
            "An error occurred when attempting to identify resource: %s"
            % str(exception)
        )
        return content, status.HTTP_500_INTERNAL_SERVER_ERROR


def sickle_list_sets(url):
    """Performs an Oai-Pmh listSet request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Data.
        Status code.

    """
    try:
        sickle = _sickle_init(url)
        list_sets = sickle.ListSets()
        serializer = sickle_serializers.SetSerializer(list_sets, many=True)
        return serializer.data, status.HTTP_200_OK
    except NoSetHierarchy as exception:
        content = OaiPmhMessage.get_message_labelled("%s" % str(exception))
        return content, status.HTTP_204_NO_CONTENT
    except Exception as exception:
        content = OaiPmhMessage.get_message_labelled(
            "An error occurred when attempting to get the sets: %s" % str(exception)
        )
        return content, status.HTTP_500_INTERNAL_SERVER_ERROR


def sickle_list_metadata_formats(url):
    """Performs an Oai-Pmh listMetadataFormat request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Data.
        Status code.

    """
    try:
        sickle = _sickle_init(url)
        list_metadata_formats = sickle.ListMetadataFormats()
        serializer = sickle_serializers.MetadataFormatSerializer(
            list_metadata_formats, many=True
        )
        return serializer.data, status.HTTP_200_OK
    except NoMetadataFormat as exception:
        # This repository does not support sets
        content = OaiPmhMessage.get_message_labelled("%s" % str(exception))
        return content, status.HTTP_204_NO_CONTENT
    except Exception as exception:
        content = OaiPmhMessage.get_message_labelled(
            "An error occurred when attempting to get the metadata formats: %s"
            % str(exception)
        )
        return content, status.HTTP_500_INTERNAL_SERVER_ERROR


def get_record_elt(xml_elt, metadata_prefix):
    """Init a Record sickle object from a representative xml string.
    Args:
        xml_elt: XML string to convert toward Record sickle object.
        metadata_prefix: Metadata Prefix

    Returns:
        Representation of an Oai-Pmh record object.

    """
    record = Record(xml_elt)
    elt_ = {
        "identifier": record.header.identifier,
        "datestamp": record.header.datestamp,
        "deleted": record.deleted,
        "sets": record.header.setSpecs,
        "metadataPrefix": metadata_prefix,
        "metadata": XSDTree.tostring(
            record.xml.find(
                ".//" + "{http://www.openarchives.org/OAI/2.0/}" + "metadata/"
            )
        )
        if not record.deleted
        else None,
        "raw": record.raw,
    }
    return elt_
