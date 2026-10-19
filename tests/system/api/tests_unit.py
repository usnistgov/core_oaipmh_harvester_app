"""Unit tests on system APIs"""

from unittest.case import TestCase
from unittest.mock import Mock, patch

from core_main_app.utils.datetime import datetime_now
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_registry.models import (
    OaiRegistry,
)
from core_oaipmh_harvester_app.system import api as oai_harvester_system_api


class TestOaiRecordUpsert(TestCase):
    """Test Oai Record Upsert"""

    def test_upsert_oai_record_returns_object(self):
        """test_upsert_oai_record_returns_object"""

        # Act
        result = oai_harvester_system_api.upsert_oai_record(MockOaiRecord())

        # Assert
        self.assertIsInstance(result, MockOaiRecord)

    def test_upsert_oai_record_raises_exception_if_save_failed(self):
        """test_upsert_oai_record_raises_exception_if_save_failed"""

        # Act + Assert
        with self.assertRaises(Exception):
            oai_harvester_system_api.upsert_oai_record(
                MockOaiRecord(save_failed=True)
            )


class TestGetOaiRecordByIdentifierAndMetadataFormat(TestCase):
    """Test get_oai_record_by_identifier_and_metadata_format"""

    @patch.object(OaiRecord, "get_by_identifier_and_metadata_format")
    def test_get_oai_record_by_identifier_and_metadata_format_returns_object(
        self, mock_get_by_identifier_and_metadata_format
    ):
        """test_get_oai_record_by_identifier_and_metadata_format_returns_object"""
        # Arrange
        mock_get_by_identifier_and_metadata_format.return_value = (
            MockOaiRecord()
        )

        # Act
        result = oai_harvester_system_api.get_oai_record_by_identifier_and_metadata_format(
            "identifier", OaiHarvesterMetadataFormat()
        )

        # Assert
        self.assertIsInstance(result, MockOaiRecord)

    @patch.object(OaiRecord, "get_by_identifier_and_metadata_format")
    def test_get_oai_record_by_identifier_and_metadata_format_propagates_exception(
        self, mock_get_by_identifier_and_metadata_format
    ):
        """test_get_oai_record_by_identifier_and_metadata_format_propagates_exception"""
        # Arrange
        mock_get_by_identifier_and_metadata_format.side_effect = Exception(
            "error"
        )

        # Act + Assert
        with self.assertRaises(Exception):
            oai_harvester_system_api.get_oai_record_by_identifier_and_metadata_format(
                "identifier", OaiHarvesterMetadataFormat()
            )


class MockOaiRecord(Mock):
    """Mock Oai Record"""

    identifier = "oai:test/id.0006"
    last_modification_date = datetime_now()
    deleted = False
    harvester_sets = [OaiHarvesterSet(), OaiHarvesterSet()]
    harvester_metadata_format = OaiHarvesterMetadataFormat()
    registry = OaiRegistry()
    xml_content = "<test><message>Hello</message></test>"

    def __init__(self, save_failed=False):
        super().__init__()
        self.save_failed = save_failed

    def convert_and_save(self):
        """convert_and_save

        Returns:
        """
        if self.save_failed:
            raise Exception()

        return None
