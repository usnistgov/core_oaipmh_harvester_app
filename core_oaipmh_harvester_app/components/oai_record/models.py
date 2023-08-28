"""
OaiRecord model
"""
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.abstract_data.models import AbstractData
from core_main_app.settings import (
    SEARCHABLE_DATA_OCCURRENCES_LIMIT,
    XML_POST_PROCESSOR,
    XML_FORCE_LIST,
)
from core_main_app.utils import xml as xml_utils
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)
from core_oaipmh_harvester_app.components.oai_registry.models import (
    OaiRegistry,
)


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

    class Meta:
        """Meta"""

        indexes = [
            GinIndex(fields=["vector_column"]),
        ]

    def get_dict_content(self):
        """Get dict_content from object or from MongoDB

        Returns:

        """
        if settings.MONGODB_INDEXING:
            from core_oaipmh_harvester_app.components.mongo.models import (
                MongoOaiRecord,
            )

            return MongoOaiRecord.objects.get(pk=self.id).dict_content
        return self.dict_content

    def convert_to_dict(self):
        """Convert data object to dict."""
        # if data stored in mongo, don't store dict_content
        if settings.MONGODB_INDEXING:
            return

        # transform xml content into a dictionary
        self.dict_content = xml_utils.raw_xml_to_dict(
            self.xml_content,
            postprocessor=XML_POST_PROCESSOR,
            force_list=XML_FORCE_LIST,
            list_limit=SEARCHABLE_DATA_OCCURRENCES_LIMIT,
        )

    def convert_to_file(self):
        """Convert data to file."""
        try:
            content = self.content.encode("utf-8")
        except UnicodeEncodeError:
            content = self.content

        self.file = SimpleUploadedFile(
            name=self.title,
            content=content,
            content_type="application/xml",
        )

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
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_by_identifier_and_metadata_format(
        identifier, harvester_metadata_format
    ):
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
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

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
            queryset.order_by(
                *[field.replace("+", "") for field in order_by_field]
            )

        return queryset.all()
