"""
    Transform operation test class
"""
import json
import os
from unittest import TestCase

from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.utils import transform_operations

DUMP_OAI_PMH_TEST_PATH = os.path.join(os.path.dirname(__file__), "data")


class TestTransformOaiIdentify(TestCase):
    def setUp(self):
        with open(os.path.join(DUMP_OAI_PMH_TEST_PATH, "oai_identify_v1.json")) as f:
            data = f.read()
        self.data = json.loads(data)

    def test_transform_oai_identify_return_object(self):
        # Act
        result = transform_operations.transform_dict_identifier_to_oai_identifier(
            self.data
        )

        # Assert
        self.assertIsInstance(result, OaiIdentify)

    def test_transform_oai_identify_raises_key_error(self):
        # Arrange
        del self.data["baseURL"]

        # Act + Assert
        with self.assertRaises(Exception):
            transform_operations.transform_dict_identifier_to_oai_identifier(self.data)


class TestTransformOaiHarvesterMetadataFormat(TestCase):
    def setUp(self):
        with open(
            os.path.join(DUMP_OAI_PMH_TEST_PATH, "oai_metadata_format_v1.json")
        ) as f:
            data = f.read()
        self.data = json.loads(data)

    def test_transform_oai_harvester_metadata_format_return_list_object(self):
        # Act
        result = transform_operations.transform_dict_metadata_format_to_oai_harvester_metadata_format(
            self.data
        )

        # Assert
        self.assertTrue(
            all(isinstance(item, OaiHarvesterMetadataFormat) for item in result)
        )

    def test_transform_oai_harvester_metadata_format_catch_key_error(self):
        # Arrange
        del self.data[0]["metadataPrefix"]

        # Act + Assert
        with self.assertRaises(Exception):
            transform_operations.transform_dict_metadata_format_to_oai_harvester_metadata_format(
                self.data
            )


class TestTransformOaiHarvesterSet(TestCase):
    def setUp(self):
        with open(os.path.join(DUMP_OAI_PMH_TEST_PATH, "oai_set_v1.json")) as f:
            data = f.read()
        self.data = json.loads(data)

    def test_transform_oai_harvester_set_return_list_object(self):
        # Act
        result = transform_operations.transform_dict_set_to_oai_harvester_set(self.data)

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in result))

    def test_transform_oai_harvester_set_catch_key_error(self):
        # Arrange
        del self.data[0]["setSpec"]

        # Act + Assert
        with self.assertRaises(Exception):
            transform_operations.transform_dict_set_to_oai_harvester_set(self.data)


class TestTransformOaiRecord(TestCase):
    def setUp(self):
        with open(os.path.join(DUMP_OAI_PMH_TEST_PATH, "oai_record_v1.json")) as f:
            data = f.read()
        self.data = json.loads(data)

    def test_transform_oai_record_return_list_object(self):
        # Act
        result = transform_operations.transform_dict_record_to_oai_record(self.data)

        # Assert
        self.assertTrue(all(isinstance(item, OaiRecord) for item in result))

    def test_transform_oai_record_catch_key_error(self):
        # Arrange
        del self.data[0]["identifier"]

        # Act + Assert
        with self.assertRaises(Exception):
            transform_operations.transform_dict_record_to_oai_record(self.data)
