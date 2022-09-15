""" Tests unit
"""

import datetime
from unittest.case import TestCase
from unittest.mock import Mock, patch

import requests
from rest_framework import status

from core_main_app.commons import exceptions
from core_main_app.components.template import api as api_template
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
import core_oaipmh_harvester_app.components.oai_harvester_metadata_format.api as harvester_metadata_format_api
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class TestOaiHarvesterMetadataFormatGetById(TestCase):
    """Test Oai Harvester Metadata Format Get By Id"""

    @patch.object(OaiHarvesterMetadataFormat, "get_by_id")
    def test_get_by_id_return_object(self, mock_get_by_id):
        """test_get_by_id_return_object"""

        # Arrange
        mock_oai_harvester_metadata_format = (
            _create_mock_oai_harvester_metadata_format()
        )

        mock_get_by_id.return_value = mock_oai_harvester_metadata_format

        # Act
        result = harvester_metadata_format_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, OaiHarvesterMetadataFormat)

    @patch.object(OaiHarvesterMetadataFormat, "get_by_id")
    def test_get_by_id_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        """test_get_by_id_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_id = 1

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            harvester_metadata_format_api.get_by_id(mock_absent_id)

    @patch.object(OaiHarvesterMetadataFormat, "get_by_id")
    def test_get_by_id_raises_exception_if_internal_error(self, mock_get_by_id):
        """test_get_by_id_raises_exception_if_internal_error"""

        # Arrange
        mock_absent_id = 1

        mock_get_by_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            harvester_metadata_format_api.get_by_id(mock_absent_id)


class TestOaiHarvesterMetadataFormatGetByMetadataPrefixAndRegistryId(TestCase):
    """Test Oai Harvester Metadata Format Get By Metadata Prefix And Registry Id"""

    @patch.object(OaiHarvesterMetadataFormat, "get_by_metadata_prefix_and_registry_id")
    def test_get_by_metadata_prefix_and_registry_id_return_object(self, mock_get):
        """test_get_by_metadata_prefix_and_registry_id_return_object"""

        # Arrange
        mock_oai_harvester_metadata_format = (
            _create_mock_oai_harvester_metadata_format()
        )

        mock_get.return_value = mock_oai_harvester_metadata_format

        # Act
        result = harvester_metadata_format_api.get_by_metadata_prefix_and_registry_id(
            mock_oai_harvester_metadata_format.metadata_prefix,
            mock_oai_harvester_metadata_format.registry.id,
        )

        # Assert
        self.assertIsInstance(result, OaiHarvesterMetadataFormat)

    @patch.object(OaiHarvesterMetadataFormat, "get_by_metadata_prefix_and_registry_id")
    def test_get_by_metadata_prefix_and_registry_id_raises_exception_if_object_does_not_exist(
        self, mock_get
    ):
        """test_get_by_metadata_prefix_and_registry_id_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_metadata_prefix = "oai_test"
        mock_absent_registry_id = str(1)

        mock_get.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            harvester_metadata_format_api.get_by_metadata_prefix_and_registry_id(
                mock_absent_metadata_prefix, mock_absent_registry_id
            )

    @patch.object(OaiHarvesterMetadataFormat, "get_by_metadata_prefix_and_registry_id")
    def test_get_by_metadata_prefix_and_registry_id_raises_exception_if_internal_error(
        self, mock_get
    ):
        """test_get_by_metadata_prefix_and_registry_id_raises_exception_if_internal_error"""

        # Arrange
        mock_absent_metadata_prefix = "oai_test"
        mock_absent_registry_id = str(1)

        mock_get.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            harvester_metadata_format_api.get_by_metadata_prefix_and_registry_id(
                mock_absent_metadata_prefix, mock_absent_registry_id
            )


class TestOaiHarvesterMetadataFormatGetAll(TestCase):
    """Test Oai Harvester Metadata Format Get All"""

    @patch.object(OaiHarvesterMetadataFormat, "get_all")
    def test_get_all_contains_only_oai_harvester_metadata_format(self, mock_get_all):
        """test_get_all_contains_only_oai_harvester_metadata_format"""

        # Arrange
        mock_oai_harvester_metadata_format1 = (
            _create_mock_oai_harvester_metadata_format()
        )
        mock_oai_harvester_metadata_format2 = (
            _create_mock_oai_harvester_metadata_format()
        )

        mock_get_all.return_value = [
            mock_oai_harvester_metadata_format1,
            mock_oai_harvester_metadata_format2,
        ]

        # Act
        result = harvester_metadata_format_api.get_all()

        # Assert
        self.assertTrue(
            all(isinstance(item, OaiHarvesterMetadataFormat) for item in result)
        )


class TestOaiHarvesterMetadataFormatGetAllByRegistryId(TestCase):
    """Test Oai Harvester Metadata Format Get All By Registry Id"""

    @patch.object(OaiHarvesterMetadataFormat, "get_all_by_registry_id")
    def test_get_all_contains_only_oai_harvester_metadata_format(
        self, mock_get_all_by_registry_id
    ):
        """test_get_all_contains_only_oai_harvester_metadata_format"""

        # Arrange
        mock_oai_harvester_metadata_format1 = (
            _create_mock_oai_harvester_metadata_format()
        )
        mock_oai_harvester_metadata_format2 = (
            _create_mock_oai_harvester_metadata_format()
        )

        mock_get_all_by_registry_id.return_value = [
            mock_oai_harvester_metadata_format1,
            mock_oai_harvester_metadata_format2,
        ]

        # Act
        result = harvester_metadata_format_api.get_all_by_registry_id(
            mock_oai_harvester_metadata_format1.registry.id
        )

        # Assert
        self.assertTrue(
            all(isinstance(item, OaiHarvesterMetadataFormat) for item in result)
        )


class TestOaiHarvesterMetadataFormatGetAllToHarvestByRegistryId(TestCase):
    """Test Oai Harvester Metadata Format Get All To Harvest By Registry Id"""

    @patch.object(OaiHarvesterMetadataFormat, "get_all_by_registry_id_and_harvest")
    def test_get_all_contains_only_oai_harvester_metadata_format_to_harvest_by_registry_id(
        self, mock_get_all
    ):
        """test_get_all_contains_only_oai_harvester_metadata_format_to_harvest_by_registry_id"""

        # Arrange
        mock_oai_harvester_metadata_format1 = (
            _create_mock_oai_harvester_metadata_format()
        )
        mock_oai_harvester_metadata_format2 = (
            _create_mock_oai_harvester_metadata_format()
        )

        mock_get_all.return_value = [
            mock_oai_harvester_metadata_format1,
            mock_oai_harvester_metadata_format2,
        ]

        # Act
        result = harvester_metadata_format_api.get_all_to_harvest_by_registry_id(
            mock_oai_harvester_metadata_format1.registry.id
        )

        # Assert
        self.assertTrue(
            all(isinstance(item, OaiHarvesterMetadataFormat) for item in result)
        )


class TestOaiHarvestMetadataFormatUpsert(TestCase):
    """Test Oai Harvester Metadata Format Upsert"""

    def setUp(self):
        self.oai_harvester_metadata_format = _create_oai_harvester_metadata_format()

    @patch.object(OaiHarvesterMetadataFormat, "save")
    def test_upsert_oai_harvester_raises_exception_if_save_failed(self, mock_save):
        """test_upsert_oai_harvester_raises_exception_if_save_failed"""

        # Arrange
        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.upsert(self.oai_harvester_metadata_format)

    @patch.object(OaiHarvesterMetadataFormat, "save")
    def test_upsert_oai_harvester_metadata_format_return_object(self, mock_create):
        """test_upsert_oai_harvester_metadata_format_return_object"""

        # Arrange
        mock_create.return_value = self.oai_harvester_metadata_format

        # Act
        result = harvester_metadata_format_api.upsert(
            self.oai_harvester_metadata_format
        )

        # Assert
        self.assertIsInstance(result, OaiHarvesterMetadataFormat)


class TestOaiHarvesterMetadataFormatDeleteAllByRegistryId(TestCase):
    """Test Oai Harvester Metadata Format Delete All By Registry Id"""

    @patch.object(OaiHarvesterMetadataFormat, "delete_all_by_registry_id")
    def test_delete_all_by_registry_id_raises_exception_if_object_does_not_exist(
        self, mock_delete_all
    ):
        """test_delete_all_by_registry_id_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_registry = str(1)

        mock_delete_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.delete_all_by_registry_id(
                mock_absent_registry
            )


class TestOaiHarvesterMetadataFormatDelete(TestCase):
    """Test Oai Harvester Metadata Format Delete"""

    @patch.object(OaiHarvesterMetadataFormat, "delete")
    def test_delete_oai_harvester_metadata_format_raises_exception_if_object_does_not_exist(
        self, mock_delete
    ):
        """test_delete_oai_harvester_metadata_format_raises_exception_if_object_does_not_exist"""

        # Arrange
        oai_harvester_metadata_format = _create_oai_harvester_metadata_format()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.delete(oai_harvester_metadata_format)


class TestOaiHarvesterMetadataFormatUpdateForAllByRegistryId(TestCase):
    """Test Oai Harvester Metadata Format Update For All By Registry Id"""

    @patch.object(OaiHarvesterMetadataFormat, "update_for_all_harvest_by_registry_id")
    def test_update_for_all_harvest_by_registry_id_raises_exception_if_object_does_not_exist(
        self, mock_update_all
    ):
        """test_update_for_all_harvest_by_registry_id_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_registry = str(1)

        mock_update_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.update_for_all_harvest_by_registry_id(
                registry_id=mock_absent_registry, harvest=True
            )


class TestOaiHarvesterMetadataFormatUpdateForAllByListIds(TestCase):
    """Test Oai Harvester Metadata Format Update For All By List Ids"""

    @patch.object(OaiHarvesterMetadataFormat, "update_for_all_harvest_by_list_ids")
    def test_update_for_all_harvest_by_list_ids_raises_exception_if_object_does_not_exist(
        self, mock_update_all
    ):
        """test_update_for_all_harvest_by_list_ids_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_list_ids = [str(1), str(1)]

        mock_update_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.update_for_all_harvest_by_list_ids(
                mock_absent_list_ids, True
            )


class TestInitSchemaInfo(TestCase):
    """Test Init Schema Info"""

    @patch.object(api_template, "get_all_accessible_by_hash")
    @patch.object(requests, "get")
    def test_init_schema_info_return_object(self, mock_get, mock_get_all_by_hash):
        """test_init_schema_info_return_object"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_oai_harvester_metadata_format = (
            _create_mock_oai_harvester_metadata_format()
        )

        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = "<test>Hello</test>"
        mock_get_all_by_hash.return_value = [Template()]

        # Act
        result = harvester_metadata_format_api.init_schema_info(
            mock_oai_harvester_metadata_format, request=mock_request
        )

        # Assert
        self.assertIsInstance(result, OaiHarvesterMetadataFormat)

    @patch.object(api_template, "get_all_accessible_by_hash")
    @patch.object(requests, "get")
    def test_init_schema_info_return_object_with_xml_schema(
        self, mock_get, mock_get_all_by_hash
    ):
        """test_init_schema_info_return_object_with_xml_schema"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        text = "<test>Hello</test>"
        mock_oai_harvester_metadata_format = (
            _create_mock_oai_harvester_metadata_format()
        )

        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text
        mock_get_all_by_hash.return_value = [Template()]

        # Act
        result = harvester_metadata_format_api.init_schema_info(
            mock_oai_harvester_metadata_format, request=mock_request
        )

        # Assert
        self.assertEqual(result.xml_schema, text)

    @patch.object(harvester_metadata_format_api, "get_hash")
    @patch.object(api_template, "get_all_accessible_by_hash")
    @patch.object(requests, "get")
    def test_init_schema_info_return_object_with_hash(
        self, mock_get, mock_get_all_by_hash, mock_get_hash
    ):
        """test_init_schema_info_return_object_with_hash"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_oai_harvester_metadata_format = (
            _create_mock_oai_harvester_metadata_format()
        )
        hash_ = "eaedb2e2d29fffeee628a51284a237e057a38a28"

        mock_get_hash.return_value = hash_
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = "<test>Hello</test>"
        mock_get_all_by_hash.return_value = [Template()]

        # Act
        result = harvester_metadata_format_api.init_schema_info(
            mock_oai_harvester_metadata_format, request=mock_request
        )

        # Assert
        self.assertEqual(result.hash, hash_)

    @patch.object(api_template, "get_all_accessible_by_hash")
    @patch.object(requests, "get")
    def test_init_schema_info_return_object_with_template(
        self, mock_get, mock_get_all_by_hash
    ):
        """test_init_schema_info_return_object_with_template"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_oai_harvester_metadata_format = (
            _create_mock_oai_harvester_metadata_format()
        )
        list_template = [Template()]

        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = "<test>Hello</test>"
        mock_get_all_by_hash.return_value = list_template

        # Act
        result = harvester_metadata_format_api.init_schema_info(
            mock_oai_harvester_metadata_format, request=mock_request
        )

        # Assert
        self.assertEqual(result.template, list_template[0])

    @patch.object(requests, "get")
    def test_init_schema_info_raises_api_error_if_bad_status_code(self, mock_get):
        """test_init_schema_info_raises_api_error_if_bad_status_code"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_oai_harvester_metadata_format = (
            _create_mock_oai_harvester_metadata_format()
        )
        text = "<test>Hello</test>"

        mock_get.return_value.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_get.return_value.text = text

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.init_schema_info(
                mock_oai_harvester_metadata_format, request=mock_request
            )


def _create_oai_harvester_metadata_format():
    """Get an OaiHarvesterMetadataFormat object.

    Returns:
        OaiHarvesterMetadataFormat instance.

    """
    oai_harvester_metadata_format = OaiHarvesterMetadataFormat()
    _set_oai_harvester_metadata_format_fields(oai_harvester_metadata_format)

    return oai_harvester_metadata_format


def _create_mock_oai_harvester_metadata_format():
    """Mock an OaiHarvesterMetadataFormat.

    Returns:
        OaiHarvesterMetadataFormat mock.

    """
    mock_oai_harvester_metadata_format = Mock(spec=OaiHarvesterMetadataFormat)
    _set_oai_harvester_metadata_format_fields(mock_oai_harvester_metadata_format)

    return mock_oai_harvester_metadata_format


def _set_oai_harvester_metadata_format_fields(oai_harvester_metadata_format):
    """Set OaiHarvesterMetadataFormat fields.

    Args:
        oai_harvester_metadata_format:

    Returns:
        OaiHarvesterMetadataFormat with assigned fields.

    """
    oai_harvester_metadata_format.metadata_prefix = "test"
    oai_harvester_metadata_format.schema = "http://test.com/test.xsd"
    oai_harvester_metadata_format.metadataNamespace = "http://test.com/meta"
    oai_harvester_metadata_format.raw = dict()
    oai_harvester_metadata_format.registry = OaiRegistry()
    oai_harvester_metadata_format.harvest = True
    oai_harvester_metadata_format.last_update = datetime.datetime.now()

    return oai_harvester_metadata_format
