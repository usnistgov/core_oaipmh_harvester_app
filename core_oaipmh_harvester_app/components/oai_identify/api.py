"""
OaiIdentify API
"""

from core_main_app.commons import exceptions
from core_main_app.utils.xml import raw_xml_to_dict
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify


def upsert(oai_identify):
    """Create or update an OaiIdentify.
    Args:
        oai_identify: OaiIdentify to create or update.

    Returns:
        OaiIdentify instance.

    """
    if oai_identify.raw and isinstance(oai_identify.raw, str):
        try:
            oai_identify.raw = raw_xml_to_dict(oai_identify.raw)
        except exceptions.XMLError:
            oai_identify.raw = {}

    oai_identify.save()
    return oai_identify


def get_by_registry_id(registry_id):
    """Get an OaiIdentify by its registry_id.

    Args:
        registry_id:  The registry id.

    Returns:
        OaiIdentify instance.

    """
    return OaiIdentify.get_by_registry_id(registry_id=registry_id)


def delete(oai_identify):
    """Delete an OaiIdentify

    Args:
        oai_identify: OaiIdentify to delete

    """
    oai_identify.delete()
