"""
OaiHarvesterMetadataFormatSet model
"""

from django_mongoengine import fields, Document
from mongoengine.queryset.base import CASCADE
from mongoengine import errors as mongoengine_errors
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import OaiHarvesterMetadataFormat
from core_oaipmh_harvester_app.components.oai_harvester_set.models import OaiHarvesterSet
from core_main_app.commons import exceptions


class OaiHarvesterMetadataFormatSet(Document):
    """Association table between OaiHarvesterMetadataFormat and OaiHarvesterSet"""
    harvester_set = fields.ReferenceField(OaiHarvesterSet, reverse_delete_rull=CASCADE)
    harvester_metadata_format = fields.ReferenceField(OaiHarvesterMetadataFormat, reverse_delete_rull=CASCADE)
    lastUpdate = fields.DateTimeField(blank=True)

    @staticmethod
    def get_by_metadata_format_and_set(oai_harvester_metadata_format, oai_harvester_set):
        """ Get an OaiHarvesterMetadataFormatSet by its OaiHarvesterMetadataFormat and OaiHarvesterSet.

            Args:
                oai_harvester_metadata_format:
                oai_harvester_set:

            Returns:
                OaiHarvesterMetadataFormatSet instance.

        """
        try:
            return OaiHarvesterMetadataFormatSet.objects.get(harvester_metadata_format=oai_harvester_metadata_format,
                                                             harvester_set=oai_harvester_set)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as e:
            raise exceptions.ModelError(e.message)
