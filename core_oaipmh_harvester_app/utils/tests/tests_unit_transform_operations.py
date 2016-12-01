"""
    Transform operation test class
"""

from core_oaipmh_harvester_app.utils import transform_operations
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify
from core_oaipmh_harvester_app.components.oai_harvester_set.models import OaiHarvesterSet
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import OaiHarvesterMetadataFormat
import core_main_app.commons.exceptions as exceptions
from unittest import TestCase
import os
import json

DUMP_OAI_PMH_TEST_PATH = os.path.join(os.path.dirname(__file__), 'data')


class TestTransformOaiIdentify(TestCase):
    def setUp(self):
        with open(os.path.join(DUMP_OAI_PMH_TEST_PATH, 'OaiIdentify.json')) as f:
            data = f.read()
        self.data = json.loads(data)

    def test_transform_oai_identify_return_object(self):
        # Act
        result = transform_operations.transform_dict_identifier_to_oai_identifier(self.data)

        # Assert
        self.assertIsInstance(result, OaiIdentify)

    def test_transform_oai_identify_raises_key_error(self):
        # Arrange
        del self.data['baseURL']

        # Act + Assert
        with self.assertRaises(Exception):
            transform_operations.transform_dict_identifier_to_oai_identifier(self.data)

    def test_transform_oai_identify_raises_error_bad_raw(self):
        # Arrange
        self.data['raw'] = "<test?Hello</test>"

        # Act + Assert
        with self.assertRaises(exceptions.XMLError):
            transform_operations.transform_dict_identifier_to_oai_identifier(self.data)


class TestTransformOaiHarvesterMetadataFormat(TestCase):
    def setUp(self):
        with open(os.path.join(DUMP_OAI_PMH_TEST_PATH, 'OaiMetadataFormat.json')) as f:
            data = f.read()
        self.data = json.loads(data)

    def test_transform_oai_harvester_metadata_format_return_list_object(self):
        # Act
        result = transform_operations.transform_dict_metadata_format_to_oai_harvester_metadata_format(self.data)

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterMetadataFormat) for item in result))

    def test_transform_oai_harvester_metadata_format_catch_key_error(self):
        # Arrange
        del self.data[0]['metadataPrefix']

        # Act + Assert
        with self.assertRaises(Exception):
            transform_operations.transform_dict_metadata_format_to_oai_harvester_metadata_format(self.data)

    def test_transform_oai_harvester_metadata_format_raises_error_bad_raw(self):
        # Arrange
        self.data[0]['raw'] = "<test?Hello</test>"

        # Act + Assert
        with self.assertRaises(exceptions.XMLError):
            transform_operations.transform_dict_metadata_format_to_oai_harvester_metadata_format(self.data)


class TestTransformOaiHarvesterSet(TestCase):
    def setUp(self):
        with open(os.path.join(DUMP_OAI_PMH_TEST_PATH, 'OaiSet.json')) as f:
            data = f.read()
        self.data = json.loads(data)

    def test_transform_oai_harvester_set_return_list_object(self):
        # Act
        result = transform_operations.transform_dict_set_to_oai_harvester_set(self.data)

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in result))

    def test_transform_oai_harvester_set_catch_key_error(self):
        # Arrange
        del self.data[0]['setSpec']

        # Act + Assert
        with self.assertRaises(Exception):
            transform_operations.transform_dict_set_to_oai_harvester_set(self.data)

    def test_transform_oai_harvester_set_raises_xml_error(self):
        # Arrange
        self.data[0]['raw'] = "<test?Hello</test>"

        # Act + Assert
        with self.assertRaises(exceptions.XMLError):
            transform_operations.transform_dict_set_to_oai_harvester_set(self.data)
