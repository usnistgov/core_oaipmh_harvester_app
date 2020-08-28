"""
OaiHarvesterMetadataFormatSet model
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors
from mongoengine.queryset.base import CASCADE

from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)


class OaiHarvesterMetadataFormatSet(Document):
    """Association table between OaiHarvesterMetadataFormat and OaiHarvesterSet"""

    harvester_set = fields.ReferenceField(OaiHarvesterSet, reverse_delete_rule=CASCADE)
    harvester_metadata_format = fields.ReferenceField(
        OaiHarvesterMetadataFormat,
        reverse_delete_rule=CASCADE,
        unique_with="harvester_set",
    )
    last_update = fields.DateTimeField(blank=True)

    @staticmethod
    def get_by_metadata_format_and_set(
        oai_harvester_metadata_format, oai_harvester_set
    ):
        """Get an OaiHarvesterMetadataFormatSet by its OaiHarvesterMetadataFormat and OaiHarvesterSet.

        Args:
            oai_harvester_metadata_format:
            oai_harvester_set:

        Returns:
            OaiHarvesterMetadataFormatSet instance.

        """
        try:
            return OaiHarvesterMetadataFormatSet.objects.get(
                harvester_metadata_format=oai_harvester_metadata_format,
                harvester_set=oai_harvester_set,
            )
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def upsert_last_update_by_metadata_format_and_set(
        harvester_metadata_format, harvester_set, last_update
    ):
        """Update the last_update date for a given metadata_format and set. Create an
        OaiHarvesterMetadataFormatSet if doesn't exist.

            Args:
                harvester_metadata_format: Metadata format.
                harvester_set: Set.
                last_update: Last update date.

        """
        try:
            OaiHarvesterMetadataFormatSet.objects(
                harvester_metadata_format=harvester_metadata_format,
                harvester_set=harvester_set,
            ).update_one(last_update=last_update, upsert=True)
        except Exception as e:
            raise exceptions.ModelError(str(e))
