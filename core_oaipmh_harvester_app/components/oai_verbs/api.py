"""
    Oai-PMH verbs API.
"""

import requests
from rest_framework import status
from rest_framework.response import Response

from xml_utils.xsd_tree.xsd_tree import XSDTree
from core_main_app.utils.requests_utils.requests_utils import send_get_request
from core_oaipmh_common_app.commons import exceptions as oai_pmh_exceptions
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from core_oaipmh_harvester_app.utils import sickle_operations, transform_operations


def identify(url):
    """Performs an Oai-Pmh identity request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Serialized Data.
        Status code.

    """
    return sickle_operations.sickle_identify(url)


def identify_as_object(url):
    """Performs an Oai-Pmh identity request.

    Args:
        url: URL of the Data Provider.

    Returns:
        OaiIdentify instance.
        Status code.

    """
    data, status_code = identify(url)
    if status_code == status.HTTP_200_OK:
        try:
            data = transform_operations.transform_dict_identifier_to_oai_identifier(
                data
            )
        except Exception as exception:
            data = OaiPmhMessage.get_message_labelled(
                "An error occurred when attempting to identify resource: %s"
                % str(exception)
            )
            status_code = status.HTTP_400_BAD_REQUEST

    return data, status_code


def list_metadata_formats(url):
    """Performs an Oai-Pmh listMetadataFormat request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Serialized Data.
        Status code.

    """
    return sickle_operations.sickle_list_metadata_formats(url)


def list_metadata_formats_as_object(url):
    """Performs an Oai-Pmh listMetadataFormat request.

    Args:
        url: URL of the Data Provider.

    Returns:
        List of OaiHarvesterMetadataFormat object.
        Status code.

    """
    data, status_code = list_metadata_formats(url)
    if status_code == status.HTTP_200_OK:
        try:
            data = transform_operations.transform_dict_metadata_format_to_oai_harvester_metadata_format(
                data
            )
        except Exception as exception:
            data = OaiPmhMessage.get_message_labelled(
                "An error occurred when attempting to get the metadata "
                "formats: %s" % str(exception)
            )
            status_code = status.HTTP_400_BAD_REQUEST

    return data, status_code


def list_sets(url):
    """Performs an Oai-Pmh listSet request.

    Args:
        url: URL of the Data Provider.

    Returns:
        Serialized Data.
        Status code.

    """
    return sickle_operations.sickle_list_sets(url)


def list_sets_as_object(url):
    """Performs an Oai-Pmh listSet request.

    Args:
        url: URL of the Data Provider.

    Returns:
        List of OaiHarvesterSet object.
        Status code.

    """
    data, status_code = list_sets(url)
    if status_code == status.HTTP_200_OK:
        try:
            data = transform_operations.transform_dict_set_to_oai_harvester_set(data)
        except Exception as exception:
            data = OaiPmhMessage.get_message_labelled(
                "An error occurred when attempting to get the sets: %s" % str(exception)
            )
            status_code = status.HTTP_400_BAD_REQUEST

    return data, status_code


def list_records(
    url,
    metadata_prefix=None,
    resumption_token=None,
    set_h=None,
    from_date=None,
    until_date=None,
):
    """Performs an Oai-Pmh ListRecords request.
    Args:
        url: URL of the Data Provider.
        metadata_prefix: Metadata Prefix to use for the request.
        resumption_token: Resumption Token to use for the request.
        set_h: Set to use for the request.
        from_date: From Date to use for the request.
        until_date: Until Date to use for the request.

    Returns:
        Response.
        Resumption Token.

    """
    try:
        params = {"verb": "ListRecords"}
        if resumption_token is not None:
            params["resumptionToken"] = resumption_token
        else:
            params["metadataPrefix"] = metadata_prefix
            params["set"] = set_h
            params["from"] = from_date
            params["until"] = until_date
        rtn = []
        http_response = send_get_request(url, params=params)
        resumption_token = None
        if http_response.status_code == status.HTTP_200_OK:
            xml = http_response.text
            elements = XSDTree.iterfind(
                xml, ".//{http://www.openarchives.org/OAI/2.0/}record"
            )
            for elt in elements:
                record = sickle_operations.get_record_elt(elt, metadata_prefix)
                rtn.append(record)
            resumption_token_elt = XSDTree.iterfind(
                xml, ".//{http://www.openarchives.org/OAI/2.0/}resumptionToken"
            )
            resumption_token = next(iter(resumption_token_elt), None)
            if resumption_token is not None:
                resumption_token = resumption_token.text.strip(" \t\r\n")
        elif http_response.status_code == status.HTTP_404_NOT_FOUND:
            raise oai_pmh_exceptions.OAIAPILabelledException(
                message="Impossible to get data from the server. Server not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        else:
            raise oai_pmh_exceptions.OAIAPILabelledException(
                message="An error occurred while trying to get data from the server.",
                status_code=http_response.status_code,
            )

        return Response(rtn, status=status.HTTP_200_OK), resumption_token
    except oai_pmh_exceptions.OAIAPIException as exception:
        return exception.response(), resumption_token
    except Exception as exception:
        content = OaiPmhMessage.get_message_labelled(
            "An error occurred during the list_records process: %s" % str(exception)
        )
        return (
            Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR),
            resumption_token,
        )


def get_data(url, request=None):
    """Performs the Oai-Pmh request.
    Args:
        url: URL with Oai-Pmh request
        request:

    Returns:
        Response.

    Raises:
        OAIAPIException: An error occurred during the process.
        OAIAPILabelledException: An error occurred during the process.

    """
    try:
        if not str(url).__contains__("?"):
            raise oai_pmh_exceptions.OAIAPIException(
                message="An error occurred, url malformed.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        registry_url = str(url).split("?")[0]
        data, status_code = identify(registry_url)
        if status_code == status.HTTP_200_OK:
            # TODO: refactor send request with cookies (same code in other apps)
            try:
                session_id = request.session.session_key
            except:
                session_id = None
            http_response = send_get_request(url, cookies={"sessionid": session_id})
            if http_response.status_code == status.HTTP_200_OK:
                return Response(http_response.text, status=status.HTTP_200_OK)
            else:
                raise oai_pmh_exceptions.OAIAPIException(
                    message="An error occurred.",
                    status_code=http_response.status_code,
                )
        else:
            content = (
                "An error occurred when attempting to identify resource: %s" % data
            )
            raise oai_pmh_exceptions.OAIAPILabelledException(
                message=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except requests.HTTPError as err:
        raise oai_pmh_exceptions.OAIAPILabelledException(
            message=str(err), status_code=err.response.status_code
        )
    except oai_pmh_exceptions.OAIAPIException as exception:
        raise exception
    except Exception as exception:
        content = "An error occurred when attempting to retrieve data: %s" % str(
            exception
        )
        raise oai_pmh_exceptions.OAIAPILabelledException(
            message=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
