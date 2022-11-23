"""
    Transform operation test class
"""
from unittest import TestCase

import json
import os

from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)
from core_oaipmh_harvester_app.components.oai_identify.models import (
    OaiIdentify,
)
from core_oaipmh_harvester_app.utils import transform_operations

DUMP_OAI_PMH_TEST_PATH = os.path.join(os.path.dirname(__file__), "data")


class TestTransformOaiIdentify(TestCase):
    """Test Transform Oai Identify"""

    def setUp(self):
        """setUp"""

        with open(
            os.path.join(DUMP_OAI_PMH_TEST_PATH, "oai_identify_v1.json")
        ) as file:
            data = file.read()
        self.data = json.loads(data)

    def test_transform_oai_identify_return_object(self):
        """test_transform_oai_identify_return_object"""

        # Act
        result = (
            transform_operations.transform_dict_identifier_to_oai_identifier(
                self.data
            )
        )

        # Assert
        self.assertIsInstance(result, OaiIdentify)

    def test_transform_oai_identify_raises_key_error(self):
        """test_transform_oai_identify_raises_key_error"""

        # Arrange
        del self.data["baseURL"]

        # Act + Assert
        with self.assertRaises(Exception):
            transform_operations.transform_dict_identifier_to_oai_identifier(
                self.data
            )


class TestTransformOaiHarvesterMetadataFormat(TestCase):
    """Test Transform Oai Harvester Metadata Format"""

    def setUp(self):
        """setUp"""

        with open(
            os.path.join(DUMP_OAI_PMH_TEST_PATH, "oai_metadata_format_v1.json")
        ) as file:
            data = file.read()
        self.data = json.loads(data)

    def test_transform_oai_harvester_metadata_format_return_list_object(self):
        """test_transform_oai_harvester_metadata_format_return_list_object"""

        # Act
        result = transform_operations.transform_dict_metadata_format_to_oai_harvester_metadata_format(
            self.data
        )

        # Assert
        self.assertTrue(
            all(
                isinstance(item, OaiHarvesterMetadataFormat) for item in result
            )
        )

    def test_transform_oai_harvester_metadata_format_catch_key_error(self):
        """test_transform_oai_harvester_metadata_format_catch_key_error"""

        # Arrange
        del self.data[0]["metadataPrefix"]

        # Act + Assert
        with self.assertRaises(Exception):
            transform_operations.transform_dict_metadata_format_to_oai_harvester_metadata_format(
                self.data
            )


class TestTransformOaiHarvesterSet(TestCase):
    """TestTransformOaiHarvesterSet"""

    def setUp(self):
        """setUp"""

        with open(
            os.path.join(DUMP_OAI_PMH_TEST_PATH, "oai_set_v1.json")
        ) as file:
            data = file.read()
        self.data = json.loads(data)

    def test_transform_oai_harvester_set_return_list_object(self):
        """test_transform_oai_harvester_set_return_list_object"""

        # Act
        result = transform_operations.transform_dict_set_to_oai_harvester_set(
            self.data
        )

        # Assert
        self.assertTrue(
            all(isinstance(item, OaiHarvesterSet) for item in result)
        )

    def test_transform_oai_harvester_set_catch_key_error(self):
        """test_transform_oai_harvester_set_catch_key_error"""

        # Arrange
        del self.data[0]["setSpec"]

        # Act + Assert
        with self.assertRaises(Exception):
            transform_operations.transform_dict_set_to_oai_harvester_set(
                self.data
            )
