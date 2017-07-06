"""
    Transform operations utils provide tool operation to transform oai-pmh dict representation to object
"""

from core_main_app.utils.xml import raw_xml_to_dict
from core_oaipmh_common_app.utils import UTCdatetime

from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import OaiHarvesterMetadataFormat
from core_oaipmh_harvester_app.components.oai_harvester_set.models import OaiHarvesterSet
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord


def transform_dict_identifier_to_oai_identifier(data):
    """ Transforms a dict to an OaiIdentify object.

    Args:
        data: Data to transform.

    Returns:
        OaiIdentify instance.

    """
    return OaiIdentify(admin_email=data['adminEmail'],
                       base_url=data['baseURL'],
                       repository_name=data['repositoryName'],
                       deleted_record=data['deletedRecord'],
                       delimiter=data['delimiter'],
                       description=data['description'],
                       earliest_datestamp=data['earliestDatestamp'],
                       granularity=data['granularity'],
                       oai_identifier=data['oai_identifier'],
                       protocol_version=data['protocolVersion'],
                       repository_identifier=data['repositoryIdentifier'],
                       sample_identifier=data['sampleIdentifier'],
                       scheme=data['scheme'],
                       raw=raw_xml_to_dict(data['raw']))


def transform_dict_set_to_oai_harvester_set(data):
    """ Transforms a dict to a list of OaiHarvesterSet object.

    Args:
        data: Data to transform.

    Returns:
        List of OaiHarvesterSet instances.

    """
    return [OaiHarvesterSet(set_name=obj['setName'], set_spec=obj['setSpec'],
                            raw=raw_xml_to_dict(obj['raw'])) for obj in data]


def transform_dict_metadata_format_to_oai_harvester_metadata_format(data):
    """ Transforms a dict to a list of OaiHarvesterMetadataFormat object.

    Args:
        data: Data to transform.

    Returns:
        List of OaiHarvesterMetadataFormat instances.

    """
    return [OaiHarvesterMetadataFormat(metadata_prefix=obj['metadataPrefix'],
                                       metadata_namespace=obj['metadataNamespace'],
                                       schema=obj['schema'],
                                       raw=raw_xml_to_dict(obj['raw'])) for obj in data]


def transform_dict_record_to_oai_record(data, registry_all_sets=[]):
    """ Transforms a dict to a list of OaiRecord object.

    Args:
        data: Data to transform.
        registry_all_sets: List of all sets.

    Returns:
        List of OaiRecord instances.

    """
    return [OaiRecord(identifier=obj['identifier'],
                      datestamp=UTCdatetime.utc_datetime_iso8601_to_datetime(obj['datestamp']),
                      deleted=obj['deleted'],
                      metadata=raw_xml_to_dict(obj['metadata']) if not obj['deleted'] else None,
                      harvester_sets=[x for x in registry_all_sets if x.set_spec in obj['sets']],
                      raw=raw_xml_to_dict(obj['raw']),
                      xml_content=str(obj['metadata'])) for obj in data]
