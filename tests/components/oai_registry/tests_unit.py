""" Unit Test OaiRegistry
"""
import datetime
from unittest.case import TestCase

from bson.objectid import ObjectId
from mock.mock import Mock, patch
from rest_framework import status
from rest_framework.response import Response

import core_oaipmh_harvester_app.components.oai_registry.api as registry_api
from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_oaipmh_common_app.commons import exceptions as oai_pmh_exceptions
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import (
    api as oai_harvester_metadata_format_api,
)
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set import (
    api as oai_harvester_set_api,
)
from core_oaipmh_harvester_app.components.oai_registry import api as oai_registry_api
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.components.oai_verbs import api as oai_verbs_api
from core_oaipmh_harvester_app.utils import transform_operations
from tests.components.oai_registry.fixtures.fixtures import OaiPmhMock


class TestOaiRegistryGetById(TestCase):
    """
    Test OaiRegistry GetById
    """

    @patch.object(OaiRegistry, "get_by_id")
    def test_get_by_id_return_object(self, mock_get_by_id):
        """

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()

        mock_get_by_id.return_value = mock_oai_registry

        # Act
        result = registry_api.get_by_id(mock_oai_registry.id)

        # Assert
        self.assertIsInstance(result, OaiRegistry)

    @patch.object(OaiRegistry, "get_by_id")
    def test_get_by_id_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        """

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            registry_api.get_by_id(mock_absent_id)

    @patch.object(OaiRegistry, "get_by_id")
    def test_get_by_id_raises_exception_if_internal_error(self, mock_get_by_id):
        """

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.ModelError("Error")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            registry_api.get_by_id(mock_absent_id)


class TestOaiRegistryGetByName(TestCase):
    """
    Test OaiRegistry GetByName
    """

    @patch.object(OaiRegistry, "get_by_name")
    def test_get_by_name_return_object(self, mock_get_by_name):
        """

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()

        mock_get_by_name.return_value = mock_oai_registry

        # Act
        result = registry_api.get_by_name(mock_oai_registry.name)

        # Assert
        self.assertIsInstance(result, OaiRegistry)

    @patch.object(OaiRegistry, "get_by_name")
    def test_get_by_name_raises_exception_if_object_does_not_exist(
        self, mock_get_by_name
    ):
        """

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_absent_name = ""

        mock_get_by_name.side_effect = exceptions.DoesNotExist("Error")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            registry_api.get_by_name(mock_absent_name)

    @patch.object(OaiRegistry, "get_by_name")
    def test_get_by_name_raises_exception_if_internal_error(self, mock_get_by_name):
        """

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_absent_name = ""

        mock_get_by_name.side_effect = exceptions.ModelError("Error")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            registry_api.get_by_name(mock_absent_name)


class TestOaiRegistryGetAll(TestCase):
    """
    Test OaiRegistry GetAll
    """

    @patch.object(OaiRegistry, "get_all")
    def test_get_all_contains_only_oai_registry(self, mock_get_all):
        """

        Args:
            mock_get_all:

        Returns:

        """
        _generic_get_all_test(self, mock_get_all, registry_api.get_all())


class TestOaiRegistryGetAllActivatedRegistry(TestCase):
    @patch.object(OaiRegistry, "get_all_by_is_activated")
    def test_get_all_contains_only_oai_registry(self, mock_get_all):
        """

        Args:
            mock_get_all:

        Returns:

        """
        _generic_get_all_test(
            self, mock_get_all, registry_api.get_all_activated_registry()
        )


class TestOaiRegistryUpsert(TestCase):
    """
    Test OaiRegistry Upsert
    """

    def setUp(self):
        """Set up the test"""
        self.oai_registry = _create_oai_registry()

    @patch.object(OaiRegistry, "save")
    def test_upsert_oai_registry_raises_exception_if_save_failed(self, mock_save):
        """

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            registry_api.upsert(self.oai_registry)


class TestCheckRegistryUrlAlreadyExists(TestCase):
    """
    Test CheckRegistryUrlAlreadyExists
    """

    def setUp(self):
        """Set up the test"""
        self.oai_registry = _create_oai_registry()

    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    def test_check_oai_registry_url_already_exists(self, mock_check):
        """

        Args:
            mock_check:

        Returns:

        """
        # Arrange
        mock_url = "http://url.com"
        mock_check.return_value = True

        # Act
        result = registry_api.check_registry_url_already_exists(mock_url)

        # Assert
        self.assertEquals(result, True)

    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    def test_check_oai_registry_url_does_not_already_exist(self, mock_check):
        """

        Args:
            mock_check:

        Returns:

        """
        # Arrange
        mock_url = "http://url.com"
        mock_check.return_value = False

        # Act
        result = registry_api.check_registry_url_already_exists(mock_url)

        # Assert
        self.assertEquals(result, False)


class TestOaiRegistryDelete(TestCase):
    """
    Test OaiRegistry Delete
    """

    @patch.object(OaiRegistry, "delete")
    def test_delete_oai_registry_raises_exception_if_object_does_not_exist(
        self, mock_delete
    ):
        """

        Args:
            mock_delete:

        Returns:

        """
        # Arrange
        oai_registry = _create_oai_registry()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            oai_registry_api.delete(oai_registry)


class TestAddRegistry(TestCase):
    """
    Test OaiRegistry Add
    """

    def setUp(self):
        """Set up the test"""
        self.error_message = "An error occurred: %s"
        self.url = "http://www.server.com"
        self.harvest_rate = 5000
        self.harvest = True

    @patch.object(oai_verbs_api, "identify_as_object")
    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    def test_add_registry_by_url_raises_exception_if_bad_identify(
        self, mock_registry, mock
    ):
        """

        Args:
            mock_registry:
            mock:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_registry.return_value = False
        mock.return_value = (
            OaiPmhMessage.get_message_labelled(self.error_message % "identify"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api.add_registry_by_url(
                self.url, self.harvest_rate, self.harvest, request=mock_request
            )

        self.assertEqual(ex.exception.message, self.error_message % "identify")
        self.assertEqual(
            ex.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(
        oai_verbs_api.transform_operations,
        "transform_dict_identifier_to_oai_identifier",
    )
    @patch.object(oai_verbs_api, "identify")
    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    def test_add_registry_by_url_raises_exception_if_bad_identify_data(
        self, mock_registry, mock_identify, mock_transform
    ):
        """

        Args:
            mock_registry:
            mock_identify:
            mock_transform:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_registry.return_value = False
        mock_identify.return_value = [], status.HTTP_200_OK
        exception_message = "Bad identify"
        mock_transform.side_effect = Exception(exception_message)

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api.add_registry_by_url(
                self.url, self.harvest_rate, self.harvest, request=mock_request
            )

        self.assertTrue(exception_message in ex.exception.message)
        self.assertEqual(ex.exception.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(oai_verbs_api, "identify_as_object")
    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    def test_add_registry_by_url_raises_exception_if_bad_sets(
        self, mock_registry, mock_sets, mock_identify
    ):
        """

        Args:
            mock_registry:
            mock_sets:
            mock_identify:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_identify.return_value = [], status.HTTP_200_OK
        mock_registry.return_value = False
        mock_sets.return_value = (
            OaiPmhMessage.get_message_labelled(self.error_message % "sets"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api.add_registry_by_url(
                self.url, self.harvest_rate, self.harvest, request=mock_request
            )

        self.assertEqual(ex.exception.message, self.error_message % "sets")
        self.assertEqual(
            ex.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(
        oai_verbs_api.transform_operations, "transform_dict_set_to_oai_harvester_set"
    )
    @patch.object(oai_verbs_api, "list_sets")
    @patch.object(oai_verbs_api, "identify_as_object")
    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    def test_add_registry_by_url_raises_exception_if_bad_sets_data(
        self, mock_registry, mock_identify, mock_set, mock_transform
    ):
        """

        Args:
            mock_registry:
            mock_identify:
            mock_set:
            mock_transform:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_registry.return_value = False
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        mock_set.return_value = [], status.HTTP_200_OK
        exception_message = "Bad sets"
        mock_transform.side_effect = Exception(exception_message)

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api.add_registry_by_url(
                self.url, self.harvest_rate, self.harvest, request=mock_request
            )

        self.assertTrue(exception_message in ex.exception.message)
        self.assertEqual(ex.exception.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(oai_verbs_api, "identify_as_object")
    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    def test_add_registry_by_url_raises_exception_if_bad_metadata_formats(
        self, mock_registry, mock_metadata_formats, mock_identify, mock_sets
    ):
        """

        Args:
            mock_registry:
            mock_metadata_formats:
            mock_identify:
            mock_sets:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_sets.return_value = [], status.HTTP_200_OK
        mock_identify.return_value = [], status.HTTP_200_OK
        mock_registry.return_value = False
        mock_metadata_formats.return_value = (
            OaiPmhMessage.get_message_labelled(self.error_message % "metadataFormats"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api.add_registry_by_url(
                self.url, self.harvest_rate, self.harvest, request=mock_request
            )

        self.assertEqual(ex.exception.message, self.error_message % "metadataFormats")
        self.assertEqual(
            ex.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(
        oai_verbs_api.transform_operations,
        "transform_dict_metadata_format_to_oai_harvester_metadata_format",
    )
    @patch.object(oai_verbs_api, "list_metadata_formats")
    @patch.object(oai_verbs_api, "list_sets")
    @patch.object(oai_verbs_api, "identify_as_object")
    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    def test_add_registry_by_url_raises_exception_if_bad_metadata_formats_data(
        self,
        mock_registry,
        mock_identify,
        mock_set,
        mock_metadata_format,
        mock_transform,
    ):
        """

        Args:
            mock_registry:
            mock_identify:
            mock_set:
            mock_metadata_format:
            mock_transform:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_registry.return_value = False
        identify = OaiPmhMock.mock_oai_identify()
        mock_identify.return_value = identify, status.HTTP_200_OK
        mock_set.return_value = [], status.HTTP_200_OK
        mock_metadata_format.return_value = [], status.HTTP_200_OK
        exception_message = "Bad metadata formats"
        mock_transform.side_effect = Exception(exception_message)

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api.add_registry_by_url(
                self.url, self.harvest_rate, self.harvest, request=mock_request
            )

        self.assertTrue(exception_message in ex.exception.message)
        self.assertEqual(ex.exception.status_code, status.HTTP_400_BAD_REQUEST)


class TestUpdateRegistryInfo(TestCase):
    """
    Test OaiRegistry Update Info
    """

    def setUp(self):
        """Set up the test"""
        self.error_message = "An error occurred: %s"

    @patch.object(oai_verbs_api, "identify_as_object")
    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    @patch.object(OaiRegistry, "get_by_id")
    def test_update_registry_info_raises_exception_if_bad_identify(
        self, mock_get, mock_registry, mock
    ):
        """

        Args:
            mock_get:
            mock_registry:
            mock:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_oai_registry = _create_mock_oai_registry()
        mock_get.return_value = mock_oai_registry
        mock_registry.return_value = False
        mock.return_value = (
            OaiPmhMessage.get_message_labelled(self.error_message % "identify"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api.update_registry_info(
                mock_oai_registry, request=mock_request
            )

        self.assertEqual(ex.exception.message, self.error_message % "identify")
        self.assertEqual(
            ex.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(oai_verbs_api, "identify_as_object")
    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    @patch.object(OaiRegistry, "get_by_id")
    def test_update_registry_info_raises_exception_if_bad_sets(
        self, mock_get, mock_registry, mock_sets, mock_identify
    ):
        """

        Args:
            mock_get:
            mock_registry:
            mock_sets:
            mock_identify:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_oai_registry = _create_mock_oai_registry()
        mock_get.return_value = mock_oai_registry
        mock_identify.return_value = [], status.HTTP_200_OK
        mock_registry.return_value = False
        mock_sets.return_value = (
            OaiPmhMessage.get_message_labelled(self.error_message % "sets"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api.update_registry_info(
                mock_oai_registry, request=mock_request
            )

        self.assertEqual(ex.exception.message, self.error_message % "sets")
        self.assertEqual(
            ex.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(oai_verbs_api, "identify_as_object")
    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    @patch.object(OaiRegistry, "get_by_id")
    def test_update_registry_info_raises_exception_if_bad_metadata_formats(
        self, mock_get, mock_registry, mock_metadata_formats, mock_identify, mock_sets
    ):
        """

        Args:
            mock_get:
            mock_registry:
            mock_metadata_formats:
            mock_identify:
            mock_sets:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_oai_registry = _create_mock_oai_registry()
        mock_get.return_value = mock_oai_registry
        mock_sets.return_value = [], status.HTTP_200_OK
        mock_identify.return_value = [], status.HTTP_200_OK
        mock_registry.return_value = False
        mock_metadata_formats.return_value = (
            OaiPmhMessage.get_message_labelled(self.error_message % "metadataFormat"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api.update_registry_info(
                mock_oai_registry, request=mock_request
            )

        self.assertEqual(ex.exception.message, self.error_message % "metadataFormat")
        self.assertEqual(
            ex.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestHarvestRegistry(TestCase):
    """
    Test OaiRegistry Harvest
    """

    @patch.object(oai_registry_api, "_harvest_by_metadata_formats")
    @patch.object(oai_registry_api, "_harvest_by_metadata_formats_and_sets")
    @patch.object(oai_harvester_set_api, "get_all_to_harvest_by_registry_id")
    @patch.object(oai_harvester_set_api, "get_all_by_registry_id")
    @patch.object(
        oai_harvester_metadata_format_api, "get_all_to_harvest_by_registry_id"
    )
    @patch.object(oai_registry_api, "upsert")
    def test_harvest_by_metadata_formats_and_sets(
        self,
        mock_upsert,
        mock_metadata_formats,
        mock_sets_all,
        mock_sets_to_harvest,
        mock_harvest_metadata_formats_and_sets,
        mock_harvest_by_metadata_formats,
    ):
        """

        Args:
            mock_upsert:
            mock_metadata_formats:
            mock_sets_all:
            mock_sets_to_harvest:
            mock_harvest_metadata_formats_and_sets:
            mock_harvest_by_metadata_formats:

        Returns:

        """
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()
        mock_upsert.return_value = mock_oai_registry
        mock_metadata_formats.return_value = []
        mock_sets_all.return_value = [object(), object()]
        # Don't harvest all sets.
        mock_sets_to_harvest.return_value = [object()]

        # Act
        oai_registry_api.harvest_registry(mock_oai_registry)

        # Assert
        self.assertTrue(mock_harvest_metadata_formats_and_sets.called)
        self.assertFalse(mock_harvest_by_metadata_formats.called)

    @patch.object(oai_registry_api, "_harvest_by_metadata_formats")
    @patch.object(oai_registry_api, "_harvest_by_metadata_formats_and_sets")
    @patch.object(oai_harvester_set_api, "get_all_to_harvest_by_registry_id")
    @patch.object(oai_harvester_set_api, "get_all_by_registry_id")
    @patch.object(
        oai_harvester_metadata_format_api, "get_all_to_harvest_by_registry_id"
    )
    @patch.object(oai_registry_api, "upsert")
    def test_harvest_by_metadata_formats(
        self,
        mock_upsert,
        mock_metadata_formats,
        mock_sets_all,
        mock_sets_to_harvest,
        mock_harvest_metadata_formats_and_sets,
        mock_harvest_by_metadata_formats,
    ):
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()
        mock_upsert.return_value = mock_oai_registry
        mock_metadata_formats.return_value = []
        mock_sets_all.return_value = [object(), object()]
        # Harvest all sets.
        mock_sets_to_harvest.return_value = mock_sets_all.return_value

        # Act
        oai_registry_api.harvest_registry(mock_oai_registry)

        # Assert
        self.assertTrue(mock_harvest_by_metadata_formats.called)
        self.assertFalse(mock_harvest_metadata_formats_and_sets.called)

    @patch.object(oai_registry_api, "_harvest_by_metadata_formats_and_sets")
    @patch.object(oai_harvester_set_api, "get_all_to_harvest_by_registry_id")
    @patch.object(oai_harvester_set_api, "get_all_by_registry_id")
    @patch.object(
        oai_harvester_metadata_format_api, "get_all_to_harvest_by_registry_id"
    )
    @patch.object(oai_registry_api, "upsert")
    def test_harvest_by_metadata_formats_and_sets_returns_errors(
        self,
        mock_upsert,
        mock_metadata_formats,
        mock_sets_all,
        mock_sets_to_harvest,
        mock_harvest_metadata_formats_and_sets,
    ):
        """

        Args:
            mock_upsert:
            mock_metadata_formats:
            mock_sets_all:
            mock_sets_to_harvest:
            mock_harvest_metadata_formats_and_sets:

        Returns:

        """
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()
        mock_upsert.return_value = mock_oai_registry
        mock_metadata_formats.return_value = []
        mock_sets_all.return_value = [object(), object()]
        # Don't harvest all sets.
        mock_sets_to_harvest.return_value = [object()]
        errors = [
            {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "error": "Error"}
        ]
        mock_harvest_metadata_formats_and_sets.return_value = errors

        # Act
        result = oai_registry_api.harvest_registry(mock_oai_registry)

        # Assert
        self.assertEquals(result, errors)

    @patch.object(oai_registry_api, "_harvest_by_metadata_formats")
    @patch.object(oai_harvester_set_api, "get_all_to_harvest_by_registry_id")
    @patch.object(oai_harvester_set_api, "get_all_by_registry_id")
    @patch.object(
        oai_harvester_metadata_format_api, "get_all_to_harvest_by_registry_id"
    )
    @patch.object(oai_registry_api, "upsert")
    def test_harvest_by_metadata_formats_returns_errors(
        self,
        mock_upsert,
        mock_metadata_formats,
        mock_sets_all,
        mock_sets_to_harvest,
        mock_harvest_by_metadata_formats,
    ):
        """

        Args:
            mock_upsert:
            mock_metadata_formats:
            mock_sets_all:
            mock_sets_to_harvest:
            mock_harvest_by_metadata_formats:

        Returns:

        """
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()
        mock_upsert.return_value = mock_oai_registry
        mock_metadata_formats.return_value = []
        mock_sets_all.return_value = [object(), object()]
        # Harvest all sets.
        mock_sets_to_harvest.return_value = mock_sets_all.return_value
        errors = [
            {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "error": "Error"}
        ]
        mock_harvest_by_metadata_formats.return_value = errors

        # Act
        result = oai_registry_api.harvest_registry(mock_oai_registry)

        # Assert
        self.assertEquals(result, errors)

    @patch.object(oai_verbs_api, "list_records")
    def test_harvest_records_returns_errors_if_not_HTTP_200_OK(self, mock_list_records):
        """

        Args:
            mock_list_records:

        Returns:

        """
        # Arrange
        resumption_token = None
        content = OaiPmhMessage.get_message_labelled("Error")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_list_records.return_value = (
            Response(content, status=status_code),
            resumption_token,
        )
        expected_error = [{"status_code": status_code, "error": "Error"}]
        registry = Mock(spec=OaiRegistry())
        registry.url = "dummy_url"
        metadata_format = Mock(spec=OaiHarvesterMetadataFormat())
        metadata_format.metadata_prefix = "oai_dummy"
        last_update = registry_all_sets = None

        # Act
        result = oai_registry_api._harvest_records(
            registry, metadata_format, last_update, registry_all_sets
        )

        # Assert
        self.assertEquals(result, expected_error)

    @patch.object(transform_operations, "transform_dict_record_to_oai_record")
    @patch.object(oai_verbs_api, "list_records")
    def test_harvest_records_returns_errors_if_transform_raises(
        self, mock_list_records, mock_transform_operations
    ):
        """

        Args:
            mock_list_records:
            mock_transform_operations:

        Returns:

        """
        # Arrange
        resumption_token = None
        content = []
        status_code = status.HTTP_200_OK
        mock_list_records.return_value = (
            Response(content, status=status_code),
            resumption_token,
        )
        error_message = "Error"
        expected_error = [
            {"status_code": status.HTTP_400_BAD_REQUEST, "error": error_message}
        ]
        registry = Mock(spec=OaiRegistry())
        registry.url = "dummy_url"
        metadata_format = Mock(spec=OaiHarvesterMetadataFormat())
        metadata_format.metadata_prefix = "oai_dummy"
        last_update = registry_all_sets = None
        mock_transform_operations.side_effect = Exception(error_message)

        # Act
        result = oai_registry_api._harvest_records(
            registry, metadata_format, last_update, registry_all_sets
        )

        # Assert
        self.assertEquals(result, expected_error)


class TestGetIdentifyAsObject(TestCase):
    """
    Test Get Identify as object
    """

    def setUp(self):
        """Set up the test"""
        self.error_message = "An error occurred: %s"

    @patch.object(oai_verbs_api, "identify_as_object")
    def test_get_identify_as_object_raises_exception_if_not_200_OK(self, mock):
        """

        Args:
            mock:

        Returns:

        """
        # Arrange
        mock.return_value = (
            OaiPmhMessage.get_message_labelled(self.error_message % "identify"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api._get_identify_as_object("dummy_url")

        self.assertEqual(ex.exception.message, self.error_message % "identify")
        self.assertEqual(
            ex.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestGetSetsAsObject(TestCase):
    """
    Test get sets as object
    """

    def setUp(self):
        self.error_message = "An error occurred: %s"

    @patch.object(oai_verbs_api, "list_sets_as_object")
    def test_get_sets_as_object_raises_exception_if_not_200_OK(self, mock):
        """

        Args:
            mock:

        Returns:

        """
        # Arrange
        mock.return_value = (
            OaiPmhMessage.get_message_labelled(self.error_message % "sets"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api._get_sets_as_object("dummy_url")

        self.assertEqual(ex.exception.message, self.error_message % "sets")
        self.assertEqual(
            ex.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(oai_verbs_api, "list_sets_as_object")
    def test_get_sets_as_object_no_exception_if_204_NO_CONTENT(self, mock):
        """

        Args:
            mock:

        Returns:

        """
        # Arrange
        empty_list = []
        mock.return_value = empty_list, status.HTTP_204_NO_CONTENT

        # Act
        result = oai_registry_api._get_sets_as_object("dummy_url")

        # Assert
        self.assertEqual(result, empty_list)


class TestGetMetadataFormatsAsObject(TestCase):
    """
    Test get metadata formats as object
    """

    def setUp(self):
        self.error_message = "An error occurred: %s"

    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    def test_get_metadata_formats_as_object_raises_exception_if_not_200_OK(self, mock):
        """

        Args:
            mock:

        Returns:

        """
        # Arrange
        mock.return_value = (
            OaiPmhMessage.get_message_labelled(self.error_message % "metadata formats"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as ex:
            oai_registry_api._get_metadata_formats_as_object("dummy_url")

        self.assertEqual(ex.exception.message, self.error_message % "metadata formats")
        self.assertEqual(
            ex.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    def test_get_metadata_formats_as_object_no_exception_if_204_NO_CONTENT(self, mock):
        """

        Args:
            mock:

        Returns:

        """
        # Arrange
        empty_list = []
        mock.return_value = empty_list, status.HTTP_204_NO_CONTENT

        # Act
        result = oai_registry_api._get_metadata_formats_as_object("dummy_url")

        # Assert
        self.assertEqual(result, empty_list)


class TestInitRegistry(TestCase):
    """
    Test OaiRegistry Init
    """

    def test_init_registry_returns_initialized_object(self):
        """

        Returns:

        """
        # Arrange
        url = "http://url.com"
        harvest = True
        harvest_rate = 3000
        repository_name = "Registry"
        description = "This is the registry"

        # Act
        result = oai_registry_api._init_registry(
            url, harvest, harvest_rate, repository_name, description
        )

        # Assert
        self.assertIsInstance(result, OaiRegistry)
        self.assertEquals(result.url, url)
        self.assertEquals(result.harvest, harvest)
        self.assertEquals(result.harvest_rate, harvest_rate)
        self.assertEquals(result.name, repository_name)
        self.assertEquals(result.description, description)
        self.assertEquals(result.is_activated, True)


def _generic_get_all_test(self, mock_get_all, act_function):
    """

    Args:
        self:
        mock_get_all:
        act_function:

    Returns:

    """
    # Arrange
    mock_oai_registry1 = _create_mock_oai_registry()
    mock_oai_registry2 = _create_mock_oai_registry()

    mock_get_all.return_value = [mock_oai_registry1, mock_oai_registry2]

    # Act
    result = act_function

    # Assert
    self.assertTrue(all(isinstance(item, OaiRegistry) for item in result))


def _create_oai_registry():
    """Get an OaiRegistry object.

    Returns:
        OaiRegistry instance.

    """
    oai_registry = OaiRegistry()
    _set_oai_registry_fields(oai_registry)

    return oai_registry


def _create_mock_oai_registry():
    """Mock an OaiRegistry.

    Returns:
        OaiRegistry mock.

    """
    mock_oai_registry = Mock(spec=OaiRegistry)
    _set_oai_registry_fields(mock_oai_registry)

    return mock_oai_registry


def _set_oai_registry_fields(oai_registry):
    """Set OaiRegistry fields.

    Args:
        oai_registry:

    Returns:
        OaiRegistry with assigned fields.

    """
    oai_registry.name = "Registry"
    oai_registry.url = "http://url.com"
    oai_registry.harvest_rate = 3000
    oai_registry.description = "This is the registry"
    oai_registry.harvest = True
    oai_registry.last_update = datetime.datetime.now()
    oai_registry.is_harvesting = False
    oai_registry.is_updating = False
    oai_registry.is_activated = True
    oai_registry.is_queued = True

    return oai_registry
