""" Unit Test oai_verbs
"""
from unittest.case import TestCase
from mock.mock import patch
import core_oaipmh_harvester_app.components.oai_verbs.api as oai_verbs_api
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import OaiHarvesterMetadataFormat
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify
from core_oaipmh_harvester_app.components.oai_harvester_set.models import OaiHarvesterSet
from rest_framework import status


class TestIdentifyAsObject(TestCase):
    @patch.object(oai_verbs_api.transform_operations, 'transform_dict_identifier_to_oai_identifier')
    @patch.object(oai_verbs_api, 'identify')
    def test_identify_as_object_return_object_and_ok_status(self, mock_identify, mock_transform):
        # Arrange
        mock_identify.return_value = [], status.HTTP_200_OK
        mock_transform.return_value = OaiIdentify()

        # Act
        data, status_code = oai_verbs_api.identify_as_object("")

        # Assert
        self.assertIsInstance(data, OaiIdentify)
        self.assertEquals(status_code, status.HTTP_200_OK)


class TestListMetadataFormatsAsObject(TestCase):
    @patch.object(oai_verbs_api.transform_operations, 'transform_dict_metadata_format_to_oai_harvester_metadata_format')
    @patch.object(oai_verbs_api, 'list_metadata_formats')
    def test_list_metadata_formats_as_object_return_object_and_ok_status(self, mock_metadata_format, mock_transform):
        # Arrange
        mock_metadata_format.return_value = [], status.HTTP_200_OK
        mock_transform.return_value = [OaiHarvesterMetadataFormat(), OaiHarvesterMetadataFormat()]

        # Act
        data, status_code = oai_verbs_api.list_metadata_formats_as_object("")

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterMetadataFormat) for item in data))
        self.assertEquals(status_code, status.HTTP_200_OK)


class TestListSetsAsObject(TestCase):
    @patch.object(oai_verbs_api.transform_operations, 'transform_dict_set_to_oai_harvester_set')
    @patch.object(oai_verbs_api, 'list_sets')
    def test_list_sets_as_object_return_object_and_ok_status(self, mock_set, mock_transform):
        # Arrange
        mock_set.return_value = [], status.HTTP_200_OK
        mock_transform.return_value = [OaiHarvesterSet(), OaiHarvesterSet()]

        # Act
        data, status_code = oai_verbs_api.list_sets_as_object("")

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in data))
        self.assertEquals(status_code, status.HTTP_200_OK)
