""" System APIs
"""
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord


def upsert_oai_record(oai_record):
    """Create or update an OaiRecord.

    Args:
        oai_record: OaiRecord to create or update.

        Returns:
            OaiRecord instance.

    """
    # Set the title with the OAI identifier.
    oai_record.title = oai_record.identifier
    oai_record.convert_and_save()
    return oai_record


def get_oai_record_by_identifier_and_metadata_format(
    identifier, harvester_metadata_format
):
    """Get an OaiRecord by its identifier and metadata format.

    Args:
        identifier: Identifier of the OaiRecord.
        harvester_metadata_format: harvester_metadata_format of the OaiRecord.

    Returns: The OaiRecord instance.

    """
    return OaiRecord.get_by_identifier_and_metadata_format(
        identifier, harvester_metadata_format
    )
