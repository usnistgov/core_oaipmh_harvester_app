""" Unit Test Data
"""
from core_main_app.utils.integration_tests.integration_base_test_case import MongoIntegrationBaseTestCase
from mock.mock import patch
from rest_framework import status
from unittest import skip
from core_oaipmh_common_app.commons import exceptions as oai_pmh_exceptions
from core_oaipmh_harvester_app.components.oai_registry import api as oai_registry_api
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.components.oai_verbs import api as oai_verbs_api
import requests
from core_oaipmh_harvester_app.components.oai_registry.tests.fixtures.fixtures import OaiPmhFixtures
from core_oaipmh_harvester_app.components.oai_registry.tests.fixtures.fixtures import OaiPmhMock
from unittest import skip

fixture_data = OaiPmhFixtures()


class TestAddRegistry(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    @skip("Need to figure out the insert_data")
    @patch.object(requests, 'get')
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    def test_add_registry(self, mock_identify, mock_metadata_formats, mock_sets, mock_get):
        # Arrange
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        mock_metadata_formats.return_value = OaiPmhMock.mock_oai_metadata_format(), status.HTTP_200_OK
        mock_sets.return_value = OaiPmhMock.mock_oai_set(), status.HTTP_200_OK
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(self.fixture.url, self.fixture.harvest_rate,
                                                      self.fixture.harvest)

        # Assert
        self.assertIsInstance(result, OaiRegistry)

    def test_add_registry_raises_exception_if_url_already_exists(self):
        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPINotUniqueError):
            oai_registry_api.add_registry_by_url(self.fixture.url, self.fixture.harvest_rate,
                                                 self.fixture.harvest)


class TestUpdateRegistryInfo(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    @skip("Have to resolve cleanDatabase() issue before. Unique constraint fails.")
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    def test_update_registry(self, mock_identify, mock_metadata_formats, mock_sets):
        # Arrange
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        mock_metadata_formats.return_value = OaiPmhMock.mock_oai_metadata_format(), status.HTTP_200_OK
        mock_sets.return_value = OaiPmhMock.mock_oai_set(), status.HTTP_200_OK

        # Act
        result = oai_registry_api.update_registry_info(self.fixture.registry)

        # Assert
        self.assertIsInstance(result, OaiRegistry)
