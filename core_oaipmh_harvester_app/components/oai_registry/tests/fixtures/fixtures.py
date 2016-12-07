""" fixtures files for Data
"""
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify
import json
from core_oaipmh_harvester_app.utils import transform_operations
import os
from core_oaipmh_harvester_app.settings import OAI_HARVESTER_ROOT

DUMP_OAI_PMH_TEST_PATH = os.path.join(OAI_HARVESTER_ROOT, 'utils', 'tests', 'data')


class OaiPmhFixtures(FixtureInterface):
    """
        Represent OaiPmh Integration Fixture
    """

    url = "http://www.server.com"
    harvest_rate = 5000
    harvest = True
    registry = None
    oai_identify = None

    """
        Registry's methods
    """
    def insert_data(self):
        self.registry = OaiRegistry(name="Registry", url=self.url, harvest_rate=self.harvest_rate,
                                    harvest=self.harvest).save()
        self.insert_oai_identify(self.url, self.registry)

    """
        OaiIdentify's methods
    """
    def insert_oai_identify(self, base_url, registry):
        self.oai_identify = OaiIdentify(base_url=base_url, registry=registry).save()


class OaiPmhMock(object):
    @staticmethod
    def mock_oai_identify():
        with open(os.path.join(DUMP_OAI_PMH_TEST_PATH, 'OaiIdentify.json')) as f:
            data = f.read()
        data_json = json.loads(data)
        oai_identifier = transform_operations.transform_dict_identifier_to_oai_identifier(data_json)
        return oai_identifier

    @staticmethod
    def mock_oai_metadata_format():
        with open(os.path.join(DUMP_OAI_PMH_TEST_PATH, 'OaiMetadataFormat.json')) as f:
            data = f.read()
        data_json = json.loads(data)
        list_oai_metadata_formats = transform_operations.\
            transform_dict_metadata_format_to_oai_harvester_metadata_format(data_json)
        return list_oai_metadata_formats

    @staticmethod
    def mock_oai_set():
        with open(os.path.join(DUMP_OAI_PMH_TEST_PATH, 'OaiSet.json')) as f:
            data = f.read()
        data_json = json.loads(data)
        list_oai_metadata_formats = transform_operations.transform_dict_set_to_oai_harvester_set(data_json)
        return list_oai_metadata_formats
