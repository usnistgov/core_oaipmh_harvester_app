""" Unit tests on system APIs
"""
import datetime
from unittest.case import TestCase
from unittest.mock import Mock

from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.system import api as oai_harvester_system_api


class TestOaiRecordUpsert(TestCase):
    """Test Oai Record Upsert"""

    def test_upsert_oai_record_return_object(self):
        """test_upsert_oai_record_return_object"""

        # Act
        result = oai_harvester_system_api.upsert_oai_record(MockOaiRecord())

        # Assert
        self.assertIsInstance(result, MockOaiRecord)

    def test_upsert_oai_harvester_raises_exception_if_save_failed(self):
        """test_upsert_oai_harvester_raises_exception_if_save_failed"""

        # Act + Assert
        with self.assertRaises(Exception):
            oai_harvester_system_api.upsert_oai_record(MockOaiRecord(save_failed=True))


class MockOaiRecord(Mock):
    """Mock Oai Record"""

    identifier = "oai:test/id.0006"
    last_modification_date = datetime.datetime.now()
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
