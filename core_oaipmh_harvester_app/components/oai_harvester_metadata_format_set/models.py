"""
OaiHarvesterMetadataFormatSet model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)


class OaiHarvesterMetadataFormatSet(models.Model):
    """Association table between OaiHarvesterMetadataFormat and OaiHarvesterSet"""

    harvester_set = models.ForeignKey(
        OaiHarvesterSet, on_delete=models.CASCADE
    )
    harvester_metadata_format = models.ForeignKey(
        OaiHarvesterMetadataFormat,
        on_delete=models.CASCADE,
    )
    last_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        """Meta"""

        unique_together = ("harvester_metadata_format", "harvester_set")

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
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

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
            OaiHarvesterMetadataFormatSet.objects.update_or_create(
                harvester_metadata_format=harvester_metadata_format,
                harvester_set=harvester_set,
                defaults={"last_update": last_update},
            )
        except Exception as exception:
            raise exceptions.ModelError(str(exception))
