"""
OaiRecord model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.abstract_data.models import AbstractData
from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class OaiRecord(AbstractData):
    """
    A record object
    """

    identifier = models.CharField(blank=False, max_length=200)
    deleted = models.BooleanField()
    harvester_sets = models.ManyToManyField(OaiHarvesterSet, blank=True)
    harvester_metadata_format = models.ForeignKey(
        OaiHarvesterMetadataFormat, on_delete=models.CASCADE
    )
    registry = models.ForeignKey(OaiRegistry, on_delete=models.CASCADE)

    @staticmethod
    def get_by_id(oai_record_id):
        """Get an OaiRecord by its id.

        Args:
            oai_record_id: Id of the OaiRecord.

        Returns: The OaiRecord instance.

        Raises:
            DoesNotExist: The OaiRecord doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiRecord.objects.get(pk=str(oai_record_id))
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_by_identifier_and_metadata_format(identifier, harvester_metadata_format):
        """Get an OaiRecord by its identifier and metadata format.

        Args:
            identifier: Identifier of the OaiRecord.
            harvester_metadata_format: harvester_metadata_format of the OaiRecord.

        Returns: The OaiRecord instance.

        Raises:
            DoesNotExist: The OaiRecord doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiRecord.objects.get(
                identifier=identifier,
                harvester_metadata_format=harvester_metadata_format,
            )
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_all():
        """Return all OaiRecord.

        Returns: List of OaiRecord.

        """
        return OaiRecord.objects.all()

    @staticmethod
    def get_all_by_registry_id(registry_id, order_by_field):
        """Return a list of OaiRecord by registry id. Possibility to order_by the list.

        Args:
            registry_id: The registry id.
            order_by_field: Order field.

        Returns:
            List of OaiRecord.

        """
        return OaiRecord.objects.filter(registry=str(registry_id)).order_by(
            *[field.replace("+", "") for field in order_by_field]
        )

    @staticmethod
    def get_count_by_registry_id(registry_id):
        """Return the number of OaiRecord by registry id.

        Args:
            registry_id: The registry id.

        Returns:
            Number of OaiRecord (int).

        """
        return OaiRecord.objects.filter(registry=str(registry_id)).count()

    @staticmethod
    def delete_all_by_registry_id(registry_id):
        """Delete all OaiRecord of a registry.

        Args:
            registry_id: The registry id.

        """
        OaiRecord.get_all_by_registry_id(registry_id, []).delete()

    @staticmethod
    def execute_full_text_query(text, list_metadata_format_id):
        """Execute full text query on OaiRecord data collection.

        Args:
            text: Keywords.
            list_metadata_format_id: List of metadata format id to search on.

        Returns: List of OaiRecord.

        """
        full_text_query = get_full_text_query(text)
        # only no deleted records, add harvester_metadata_format criteria
        full_text_query.update(
            {"deleted": False},
            {"harvester_metadata_format__id": {"$in": list_metadata_format_id}},
        )

        return OaiRecord.objects.find(full_text_query)

    @staticmethod
    def execute_query(query, order_by_field):
        """Executes a query on the OaiRecord collection.

        Args:
            query: Query to execute.
            order_by_field: Order by Data field

        Returns:
            Results of the query.

        """
        queryset = OaiRecord.objects.filter(query)

        if order_by_field:
            queryset.order_by(*[field.replace("+", "") for field in order_by_field])

        return queryset.all()

    @staticmethod
    def aggregate(pipeline):
        """Execute an aggregate on the Data collection.

        Args:
            pipeline:

        Returns:

        """
        return OaiRecord.objects.aggregate(*pipeline)
