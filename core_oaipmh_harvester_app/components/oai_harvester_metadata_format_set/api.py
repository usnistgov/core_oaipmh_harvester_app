"""
OaiHarvesterMetadataFormatSet API
"""

from core_oaipmh_harvester_app.components.oai_harvester_metadata_format_set.models import OaiHarvesterMetadataFormatSet
from core_main_app.commons import exceptions
from core_oaipmh_common_app.utils import UTCdatetime


def upsert(oai_harvester_metadata_format_set):
    """ Create or update an OaiHarvesterMetadataFormatSet.

        Args:
            oai_harvester_metadata_format_set: OaiHarvesterMetadataFormatSet to create or update.

        Returns:
            OaiHarvesterMetadataFormatSet instance.

    """
    return oai_harvester_metadata_format_set.save()


def get_by_metadata_format_and_set(oai_harvester_metadata_format, oai_harvester_set):
    """ Get an OaiHarvesterMetadataFormatSet by its OaiHarvesterMetadataFormat and OaiHarvesterSet.

        Args:
            oai_harvester_metadata_format:
            oai_harvester_set:

        Returns:
            OaiHarvesterMetadataFormatSet instance.

    """
    return OaiHarvesterMetadataFormatSet.get_by_metadata_format_and_set(oai_harvester_metadata_format,
                                                                        oai_harvester_set)


def get_last_update_by_metadata_format_and_set(oai_harvester_metadata_format, oai_harvester_set):
    """ Get the last update by OaiHarvesterMetadataFormat and OaiHarvesterSet.

        Args:
            oai_harvester_metadata_format:
            oai_harvester_set:

        Returns:
            OaiHarvesterMetadataFormatSet last update (string).

    """
    return UTCdatetime.datetime_to_utc_datetime_iso8601(get_by_metadata_format_and_set(oai_harvester_metadata_format,
                                                                                       oai_harvester_set).lastUpdate)
