""" Unit tests on system APIs
"""
import datetime
from unittest.case import TestCase
from unittest.mock import patch

from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.system import api as oai_harvester_system_api


class TestOaiRecordUpsert(TestCase):
    def setUp(self):
        self.oai_record = _create_oai_record()

    @patch.object(OaiRecord, "save")
    @patch.object(OaiRecord, "convert_to_file")
    def test_upsert_oai_record_return_object(self, mock_convert_file, mock_save):
        # Arrange
        mock_save.return_value = self.oai_record
        mock_convert_file.return_value = None

        # Act
        result = oai_harvester_system_api.upsert_oai_record(self.oai_record)

        # Assert
        self.assertIsInstance(result, OaiRecord)

    @patch.object(OaiRecord, "save")
    @patch.object(OaiRecord, "convert_to_file")
    def test_upsert_oai_harvester_raises_exception_if_save_failed(
        self, mock_convert_file, mock_save
    ):
        # Arrange
        mock_save.side_effect = Exception()
        mock_convert_file.return_value = None

        # Act + Assert
        with self.assertRaises(Exception):
            oai_harvester_system_api.upsert_oai_record(self.oai_record)


def _create_oai_record():
    """Get an OaiRecord object.

    Returns:
        OaiRecord instance.

    """
    oai_record = OaiRecord()
    _set_oai_record_fields(oai_record)

    return oai_record


def _set_oai_record_fields(oai_record):
    """Set OaiRecord fields.

    Args:
        oai_record:

    Returns:
        OaiRecord with assigned fields.

    """
    oai_record.identifier = "oai:test/id.0006"
    oai_record.last_modification_date = datetime.datetime.now()
    oai_record.deleted = False
    oai_record.harvester_sets = [OaiHarvesterSet(), OaiHarvesterSet()]
    oai_record.harvester_metadata_format = OaiHarvesterMetadataFormat()
    oai_record.registry = OaiRegistry()
    oai_record.xml_content = "<test><message>Hello</message></test>"

    return oai_record
