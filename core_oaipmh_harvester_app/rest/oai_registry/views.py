""" OaiRegistry rest api
"""

from core_main_app.commons import exceptions
from core_main_app.utils.permissions import api_staff_member_required, api_permission_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import core_oaipmh_harvester_app.components.oai_registry.api as oai_registry_api
from core_oaipmh_harvester_app.commons import exceptions as exceptions_oai
from core_oaipmh_harvester_app.commons.messages import OaiPmhMessage
from core_oaipmh_harvester_app.rest import serializers
from core_oaipmh_harvester_app.commons import rights


@api_view(['GET'])
@api_permission_required(rights.oai_pmh_content_type, rights.oai_pmh_access)
def select_registry(request):
    """ Get a registry (Data provider) by its name.

    GET http://<server_ip>:<server_port>/oai_pmh/api/select/registry

    Params:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"registry_name":"value"}

    Raises:
        OAIAPISerializeLabelledException: Serialization error.

    """
    try:
        serializer = serializers.SelectRegistrySerializer(data=request.query_params)
        if serializer.is_valid():
            registry_name = serializer.data.get('registry_name')
            registry = oai_registry_api.get_by_name(registry_name)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.RegistrySerializer(registry)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No registry found with the given name.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@api_permission_required(rights.oai_pmh_content_type, rights.oai_pmh_access)
def select_all_registries(request):
    """ Return all registries (Data provider).

    GET http://<server_ip>:<server_port>/oai_pmh/api/select/all/registries

    Returns:
        Response object.

    """
    try:
        registry = oai_registry_api.get_all()
        serializer = serializers.RegistrySerializer(registry, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def add_registry(request):
    """ Add a new registry (Data provider).

    POST http://<server_ip>:<server_port>/oai_pmh/api/add/registry

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"url":"value","harvest_rate":"number", "harvest":"True or False"}

    Raises:
        OAIAPISerializeLabelledException: Serialization error.

    """
    try:
        serializer = serializers.AddRegistrySerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.data.get('url')
            harvest_rate = serializer.data.get('harvest_rate')
            harvest = serializer.data.get('harvest')
            registry = oai_registry_api.add_registry_by_url(url, harvest_rate, harvest)
            content = OaiPmhMessage.get_message_labelled('Registry {0} added with success.'.format(registry.name))

            return Response(content, status=status.HTTP_201_CREATED)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def update_registry_info(request):
    """ Update oai-pmh information for a given registry (Data provider).

    POST http://<server_ip>:<server_port>/oai_pmh/api/update/registry/info

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"registry_id":"value"}

    """
    try:
        serializer = serializers.RegistryIdSerializer(data=request.data)
        if serializer.is_valid():
            registry_id = serializer.data.get('registry_id')
            registry = oai_registry_api.get_by_id(registry_id)
            registry = oai_registry_api.update_registry_info(registry)
            content = OaiPmhMessage.get_message_labelled('Registry {0} information updated with success.'.
                                                         format(registry.name))

            return Response(content, status=status.HTTP_200_OK)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
    except exceptions.DoesNotExist as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@api_staff_member_required()
def update_registry_conf(request):
    """ Update oai-pmh configuration for a given registry (Data provider).

    PUT http://<server_ip>:<server_port>/oai_pmh/api/update/registry/conf

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"registry_id":"value", "harvest_rate":"value", "harvest":"True or False"}

    """
    try:
        serializer = serializers.UpdateRegistrySerializer(data=request.data)
        if serializer.is_valid():
            registry = oai_registry_api.get_by_id(serializer.data.get('registry_id'))
            registry.harvest_rate = serializer.data.get('harvest_rate')
            registry.harvest = serializer.data.get('harvest')
            oai_registry_api.upsert(registry)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        content = OaiPmhMessage.get_message_labelled('Registry {0} updated with success.'.format(registry.name))

        return Response(content, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No registry found with the given id.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def deactivate_registry(request):
    """ Deactivate a given registry (Data provider).

    POST http://<server_ip>:<server_port>/oai_pmh/api/deactivate/registry

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"registry_id":"value"}

    """
    try:
        serializer = serializers.RegistryIdSerializer(data=request.data)
        if serializer.is_valid():
            registry = oai_registry_api.get_by_id(serializer.data.get('registry_id'))
            registry.is_activated = False
            oai_registry_api.upsert(registry)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        content = OaiPmhMessage.get_message_labelled('Registry {0} deactivated with success.'.format(registry.name))

        return Response(content, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No registry found with the given id.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def activate_registry(request):
    """ Activate a given registry (Data provider).

    POST http://<server_ip>:<server_port>/oai_pmh/api/activate/registry

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"registry_id":"value"}

    """
    try:
        serializer = serializers.RegistryIdSerializer(data=request.data)
        if serializer.is_valid():
            registry = oai_registry_api.get_by_id(serializer.data.get('registry_id'))
            registry.is_activated = True
            oai_registry_api.upsert(registry)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        content = OaiPmhMessage.get_message_labelled('Registry {0} activated with success.'.format(registry.name))

        return Response(content, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No registry found with the given id.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def delete_registry(request):
    """ Delete a given registry (Data provider).

    POST http://<server_ip>:<server_port>/oai_pmh/api/delete/registry

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"registry_id":"value"}

    """
    try:
        serializer = serializers.RegistryIdSerializer(data=request.data)
        if serializer.is_valid():
            registry = oai_registry_api.get_by_id(serializer.data.get('registry_id'))
            oai_registry_api.delete(registry)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        content = OaiPmhMessage.get_message_labelled('Registry {0} deleted with success.'.format(registry.name))

        return Response(content, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No registry found with the given id.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def harvest_registry(request):
    """ Harvest a given registry (Data provider).

    POST http://<server_ip>:<server_port>/oai_pmh/api/harvest/registry

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"registry_id":"value"}

    """
    try:
        serializer = serializers.RegistryIdSerializer(data=request.data)
        if serializer.is_valid():
            registry_id = serializer.data.get('registry_id')
            registry = oai_registry_api.get_by_id(registry_id)
            all_errors = oai_registry_api.harvest_registry(registry)
            if len(all_errors) > 0:
                raise exceptions_oai.OAIAPISerializeLabelledException(errors=all_errors,
                                                                      status_code=status.HTTP_400_BAD_REQUEST)
            else:
                content = OaiPmhMessage.get_message_labelled('Registry {0} harvested with success.'.
                                                             format(registry.name))
                return Response(content, status=status.HTTP_200_OK)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
    except exceptions.DoesNotExist as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
