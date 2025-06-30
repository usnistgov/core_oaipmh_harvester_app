""" OaiRegistry rest api
"""

from django.utils.decorators import method_decorator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions
from core_main_app.utils.decorators import (
    api_staff_member_required,
    api_permission_required,
)
from core_oaipmh_common_app.commons import exceptions as exceptions_oai
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from core_oaipmh_harvester_app.commons import rights
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import (
    api as oai_metadata_format_api,
)
from core_oaipmh_harvester_app.components.oai_harvester_set import (
    api as oai_set_api,
)
from core_oaipmh_harvester_app.components.oai_registry import (
    api as oai_registry_api,
)
from core_oaipmh_harvester_app.rest import serializers


@extend_schema(
    tags=["OAI Harvester Registry"],
    description="Registry List",
)
class RegistryList(APIView):
    """Registry List"""

    @extend_schema(
        summary="Get all registries",
        description="Get all Registries (Data provider)",
        responses={
            200: serializers.RegistrySerializer(many=True),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    @method_decorator(
        api_permission_required(
            rights.OAI_PMH_CONTENT_TYPE, rights.OAI_PMH_ACCESS
        )
    )
    def get(self, request):
        """Get all Registries (Data provider)
        Args:
            request: HTTP request
        Returns:
            - code: 200
              content: List of Registries
            - code: 500
              content: Internal server error
        """
        try:
            registry = oai_registry_api.get_all()
            serializer = serializers.RegistrySerializer(
                registry, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Create a registry",
        description="Create a Registry (Data provider)",
        request=serializers.RegistrySerializer,
        responses={
            201: serializers.RegistrySerializer,
            400: OpenApiResponse(description="Validation error"),
            500: OpenApiResponse(description="Internal server error"),
        },
        examples=[
            OpenApiExample(
                "Example request",
                summary="Example request body",
                description="Example request body for creating a registry",
                value={
                    "url": "value",
                    "harvest_rate": "number",
                    "harvest": "True or False",
                },
            ),
        ],
    )
    @method_decorator(api_staff_member_required())
    def post(self, request):
        """Create a Registry (Data provider)
        Parameters:
            {
              "url" : "value",
              "harvest_rate" : "number",
              "harvest" : "True or False"
            }
        Args:
            request: HTTP request
        Returns:
            - code: 201
              content: Created Registry
            - code: 400
              content: Validation error
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            serializer = serializers.RegistrySerializer(
                data=request.data, context={"request": request}
            )
            # Validate data
            serializer.is_valid(raise_exception=True)
            # Save data
            registry = serializer.save()
            content = OaiPmhMessage.get_message_labelled(
                "Registry {0} added.".format(registry.name)
            )
            return Response(content, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = OaiPmhMessage.get_message_labelled(
                validation_exception.detail
            )
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["OAI Harvester Registry"],
    description="Registry Detail",
)
class RegistryDetail(APIView):
    """Registry Detail"""

    @extend_schema(
        summary="Retrieve a registry",
        description="Retrieve a Registry (Data provider)",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Registry ID",
            ),
        ],
        responses={
            200: serializers.RegistrySerializer,
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    @method_decorator(
        api_permission_required(
            rights.OAI_PMH_CONTENT_TYPE, rights.OAI_PMH_ACCESS
        )
    )
    def get(self, request, registry_id):
        """Retrieve a Registry (Data provider)
        Args:
            request: HTTP request
            registry_id: ObjectId
        Returns:
            - code: 200
              content: Registry
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            registry = oai_registry_api.get_by_id(registry_id)
            serializer = serializers.RegistrySerializer(
                registry, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except exceptions.DoesNotExist:
            content = OaiPmhMessage.get_message_labelled(
                "No registry found with the given id."
            )
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Delete a registry",
        description="Delete a Registry (Data provider)",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Registry ID",
            ),
        ],
        responses={
            204: None,
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def delete(self, request, registry_id):
        """Delete a Registry (Data provider)
        Args:
            request: HTTP request
            registry_id: ObjectId
        Returns:
            - code: 204
              content: Deletion succeed
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            registry = oai_registry_api.get_by_id(registry_id)
            oai_registry_api.delete(registry)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.DoesNotExist:
            content = OaiPmhMessage.get_message_labelled(
                "No registry found with the given id."
            )
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Update a registry",
        description="Update oai-pmh configuration for a given registry (Data provider)",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Registry ID",
            ),
        ],
        request=serializers.UpdateRegistrySerializer,
        responses={
            200: OpenApiResponse(description="Success message"),
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
        examples=[
            OpenApiExample(
                "Example request",
                summary="Example request body",
                description="Example request body for updating a registry",
                value={"harvest_rate": "value", "harvest": "True or False"},
            ),
        ],
    )
    @method_decorator(api_staff_member_required())
    def patch(self, request, registry_id):
        """Update oai-pmh configuration for a given registry (Data provider)
        Parameters:
            {
              "harvest_rate" : "value",
              "harvest" : "True or False"
            }
        Args:
            request: HTTP request
            registry_id: ObjectId
        Returns:
            - code: 200
              content: Success message
            - code: 400
              content: Validation error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            registry = oai_registry_api.get_by_id(registry_id)
            # Build serializer
            serializer = serializers.UpdateRegistrySerializer(
                instance=registry, data=request.data
            )
            # Validate data
            serializer.is_valid(raise_exception=True)
            # Save data
            serializer.save()
            content = OaiPmhMessage.get_message_labelled(
                "Registry {0} updated.".format(registry.name)
            )
            return Response(content, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = OaiPmhMessage.get_message_labelled(
                validation_exception.detail
            )
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = OaiPmhMessage.get_message_labelled(
                "No registry found with the given id."
            )
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["OAI Harvester Registry"],
    description="Activate Registry",
)
class ActivateRegistry(APIView):
    """Activate Registry"""

    @extend_schema(
        summary="Activate a registry",
        description="Activate a given registry (Data provider)",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Registry ID",
            ),
        ],
        responses={
            200: OpenApiResponse(description="Success message"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def patch(self, request, registry_id):
        """Activate a given registry (Data provider)
        Args:
            request: HTTP request
            registry_id: ObjectId
        Returns:
            - code: 200
              content: Success message
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            registry = oai_registry_api.get_by_id(registry_id)
            registry.is_activated = True
            oai_registry_api.upsert(registry)
            content = OaiPmhMessage.get_message_labelled(
                "Registry {0} activated.".format(registry.name)
            )
            return Response(content, status=status.HTTP_200_OK)
        except exceptions.DoesNotExist:
            content = OaiPmhMessage.get_message_labelled(
                "No registry found with the given id."
            )
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["OAI Harvester Registry"],
    description="Deactivate Registry",
)
class DeactivateRegistry(APIView):
    """Deactivate Registry"""

    @extend_schema(
        summary="Deactivate a registry",
        description="Deactivate a given registry (Data provider)",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Registry ID",
            ),
        ],
        responses={
            200: OpenApiResponse(description="Success message"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def patch(self, request, registry_id):
        """Deactivate a given registry (Data provider)
        Args:
            request: HTTP request
            registry_id: ObjectId
        Returns:
            - code: 200
              content: Success message
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            registry = oai_registry_api.get_by_id(registry_id)
            registry.is_activated = False
            oai_registry_api.upsert(registry)
            content = OaiPmhMessage.get_message_labelled(
                "Registry {0} deactivated.".format(registry.name)
            )
            return Response(content, status=status.HTTP_200_OK)
        except exceptions.DoesNotExist:
            content = OaiPmhMessage.get_message_labelled(
                "No registry found with the given id."
            )
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["OAI Harvester Registry"],
    description="Info Registry",
)
class InfoRegistry(APIView):
    """Info Registry"""

    @extend_schema(
        summary="Update oai-pmh information for a registry",
        description="Update oai-pmh information for a given registry (Data provider)",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Registry ID",
            ),
        ],
        responses={
            200: OpenApiResponse(description="Success message"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def patch(self, request, registry_id):
        """Update oai-pmh information for a given registry (Data provider)
        Args:
            request: HTTP request
            registry_id: ObjectId
        Returns:
            - code: 200
              content: Success message
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            registry = oai_registry_api.get_by_id(registry_id)
            registry = oai_registry_api.update_registry_info(
                registry, request=request
            )
            content = OaiPmhMessage.get_message_labelled(
                "Registry {0} information updated.".format(registry.name)
            )
            return Response(content, status=status.HTTP_200_OK)
        except exceptions.DoesNotExist as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["OAI Harvester Registry"],
    description="Harvest",
)
class Harvest(APIView):
    """Harvest"""

    @extend_schema(
        summary="Harvest a registry",
        description="Harvest a given registry (Data provider)",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Registry ID",
            ),
        ],
        responses={
            200: OpenApiResponse(description="Success message"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def patch(self, request, registry_id):
        """Harvest a given registry (Data provider)
        Args:
            request: HTTP request
            registry_id: ObjectId
        Returns:
            - code: 200
              content: Success message
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            registry = oai_registry_api.get_by_id(registry_id)
            all_errors = oai_registry_api.harvest_registry(registry)
            if len(all_errors) > 0:
                raise exceptions_oai.OAIAPISerializeLabelledException(
                    errors=all_errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            content = OaiPmhMessage.get_message_labelled(
                "Registry {0} harvested.".format(registry.name)
            )
            return Response(content, status=status.HTTP_200_OK)
        except exceptions.DoesNotExist as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Update harvesting configuration",
        description="Edit the harvesting configuration of a registry (Data Provider). Configure metadata_formats and sets to harvest.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Registry ID",
            ),
        ],
        request=serializers.HarvestSerializer,
        responses={
            200: OpenApiResponse(description="Success message"),
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
        examples=[
            OpenApiExample(
                "Example request",
                summary="Example request body",
                description="Example request body for updating harvesting configuration",
                value={
                    "metadata_formats": ["id1", "id2"],
                    "sets": ["id1", "id2"],
                },
            ),
        ],
    )
    @method_decorator(api_staff_member_required())
    def put(self, request, registry_id):
        """Edit the harvesting configuration of a registry (Data Provider)
        Configure metadata_formats and sets to harvest
        Parameters:
            {
              "metadata_formats": ["id1", "id2"..],
              "sets": ["id1", "id2"..]
            }
        Args:
            request: HTTP request
            registry_id: ObjectId
        Returns:
            - code: 200
              content: Success message
            - code: 400
              content: Validation error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            serializer = serializers.HarvestSerializer(data=request.data)
            # Validate data
            serializer.is_valid(raise_exception=True)
            # Harvest
            metadata_formats = serializer.data.get("metadata_formats")
            sets = serializer.data.get("sets")
            # Get metadata formats ids and sets ids related to the registry.
            registry_metadata_formats = (
                oai_metadata_format_api.get_all_by_registry_id(
                    registry_id
                ).values_list("id", flat=True)
            )
            registry_sets = oai_set_api.get_all_by_registry_id(
                registry_id
            ).values_list("id", flat=True)
            # Set all metadata_formats to false (Do not harvest)
            oai_metadata_format_api.update_for_all_harvest_by_list_ids(
                registry_metadata_formats, False
            )
            # Set given metadata_formats to True (Harvest)
            oai_metadata_format_api.update_for_all_harvest_by_list_ids(
                metadata_formats, True
            )
            # Set all sets to false (Do not harvest)
            oai_set_api.update_for_all_harvest_by_list_ids(
                registry_sets, False
            )
            # Set given sets to True (Harvest)
            oai_set_api.update_for_all_harvest_by_list_ids(sets, True)
            content = OaiPmhMessage.get_message_labelled(
                "Registry harvesting configuration updated."
            )
            return Response(content, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = OaiPmhMessage.get_message_labelled(
                validation_exception.detail
            )
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
