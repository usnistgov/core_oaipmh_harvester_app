from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
import core_oaipmh_harvester_app.components.oai_registry.api as registry_api
from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
import datetime
from core_oaipmh_harvester_app.components.oai_verbs import api as oai_verbs_api
from rest_framework import status
from core_oaipmh_harvester_app.components.oai_registry import api as oai_registry_api
from core_oaipmh_harvester_app.commons import exceptions as oai_pmh_exceptions
from core_oaipmh_harvester_app.commons.messages import OaiPmhMessage


class TestOaiRegistryGetById(TestCase):
    @patch.object(OaiRegistry, 'get_by_id')
    def test_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()

        mock_get_by_id.return_value = mock_oai_registry

        # Act
        result = registry_api.get_by_id(mock_oai_registry.id)

        # Assert
        self.assertIsInstance(result, OaiRegistry)

    @patch.object(OaiRegistry, 'get_by_id')
    def test_get_by_id_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            registry_api.get_by_id(mock_absent_id)

    @patch.object(OaiRegistry, 'get_by_id')
    def test_get_by_id_raises_exception_if_internal_error(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.ModelError("Error")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            registry_api.get_by_id(mock_absent_id)


class TestOaiRegistryGetByName(TestCase):
    @patch.object(OaiRegistry, 'get_by_name')
    def test_get_by_name_return_object(self, mock_get_by_name):
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()

        mock_get_by_name.return_value = mock_oai_registry

        # Act
        result = registry_api.get_by_name(mock_oai_registry.name)

        # Assert
        self.assertIsInstance(result, OaiRegistry)

    @patch.object(OaiRegistry, 'get_by_name')
    def test_get_by_name_raises_exception_if_object_does_not_exist(self, mock_get_by_name):
        # Arrange
        mock_absent_name = ""

        mock_get_by_name.side_effect = exceptions.DoesNotExist("Error")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            registry_api.get_by_name(mock_absent_name)

    @patch.object(OaiRegistry, 'get_by_name')
    def test_get_by_name_raises_exception_if_internal_error(self, mock_get_by_name):
        # Arrange
        mock_absent_name = ""

        mock_get_by_name.side_effect = exceptions.ModelError("Error")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            registry_api.get_by_name(mock_absent_name)


class TestOaiRegistryGetAll(TestCase):
    @patch.object(OaiRegistry, 'get_all')
    def test_get_all_contains_only_oai_registry(self, mock_get_all):
        _generic_get_all_test(self, mock_get_all, registry_api.get_all())


class TestOaiRegistryGetAllActivatedRegistry(TestCase):
    @patch.object(OaiRegistry, 'get_all_by_is_activated')
    def test_get_all_contains_only_oai_registry(self, mock_get_all):
        _generic_get_all_test(self, mock_get_all, registry_api.get_all_activated_registry())


class TestOaiRegistryUpsert(TestCase):
    @patch.object(OaiRegistry, 'save')
    def test_upsert_oai_registry_raises_exception_if_save_failed(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            registry_api.upsert(self.oai_registry)


class TestCheckRegistryUrlAlreadyExists(TestCase):
    def setUp(self):
        self.oai_registry = _create_oai_registry()

    @patch.object(OaiRegistry, 'check_registry_url_already_exists')
    def test_check_oai_registry_url_already_exists(self, mock_check):
        # Arrange
        mock_url = "http://url.com"
        mock_check.return_value = True

        # Act
        result = registry_api.check_registry_url_already_exists(mock_url)

        # Assert
        self.assertEquals(result, True)

    @patch.object(OaiRegistry, 'check_registry_url_already_exists')
    def test_check_oai_registry_url_does_not_already_exist(self, mock_check):
        # Arrange
        mock_url = "http://url.com"
        mock_check.return_value = False

        # Act
        result = registry_api.check_registry_url_already_exists(mock_url)

        # Assert
        self.assertEquals(result, False)


class TestOaiRegistryDelete(TestCase):
    @patch.object(OaiRegistry, 'delete')
    def test_delete_oai_registry_raises_exception_if_object_does_not_exist(self, mock_delete):
        # Arrange
        oai_registry = _create_oai_registry()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            oai_registry_api.delete(oai_registry)


class TestAddRegistry(TestCase):
    def setUp(self):
        self.error_message = 'An error occurred: %s'
        self.url = "http://www.server.com"
        self.harvest_rate = 5000
        self.harvest = True

    @patch.object(oai_verbs_api, 'identify_as_object')
    @patch.object(OaiRegistry, 'check_registry_url_already_exists')
    def test_add_registry_by_url_raises_exception_if_bad_identify(self, mock_registry, mock):
        # Arrange
        mock_registry.return_value = False
        mock.return_value = OaiPmhMessage.get_message_labelled(self.error_message % "identify"), status.\
            HTTP_500_INTERNAL_SERVER_ERROR

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as e:
            oai_registry_api.add_registry_by_url(self.url, self.harvest_rate, self.harvest)

        self.assertEqual(e.exception.message, self.error_message % "identify")
        self.assertEqual(e.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch.object(oai_verbs_api, 'identify_as_object')
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(OaiRegistry, 'check_registry_url_already_exists')
    def test_add_registry_by_url_raises_exception_if_bad_sets(self, mock_registry, mock_sets, mock_identify):
        # Arrange
        mock_identify.return_value = [], status.HTTP_200_OK
        mock_registry.return_value = False
        mock_sets.return_value = OaiPmhMessage.get_message_labelled(self.error_message % "sets"), status.\
            HTTP_500_INTERNAL_SERVER_ERROR

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as e:
            oai_registry_api.add_registry_by_url(self.url, self.harvest_rate, self.harvest)

        self.assertEqual(e.exception.message, self.error_message % "sets")
        self.assertEqual(e.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(OaiRegistry, 'check_registry_url_already_exists')
    def test_add_registry_by_url_raises_exception_if_bad_metadata_formats(self, mock_registry, mock_metadata_formats,
                                                                          mock_identify, mock_sets):
        # Arrange
        mock_sets.return_value = [], status.HTTP_200_OK
        mock_identify.return_value = [], status.HTTP_200_OK
        mock_registry.return_value = False
        mock_metadata_formats.return_value = OaiPmhMessage.get_message_labelled(self.error_message % "metadataFormats"), status.\
            HTTP_500_INTERNAL_SERVER_ERROR

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as e:
            oai_registry_api.add_registry_by_url(self.url, self.harvest_rate, self.harvest)

        self.assertEqual(e.exception.message, self.error_message % "metadataFormats")
        self.assertEqual(e.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestUpdateRegistryInfo(TestCase):
    def setUp(self):
        self.error_message = 'An error occurred: %s'

    @patch.object(oai_verbs_api, 'identify_as_object')
    @patch.object(OaiRegistry, 'check_registry_url_already_exists')
    @patch.object(OaiRegistry, 'get_by_id')
    def test_update_registry_info_raises_exception_if_bad_identify(self, mock_get, mock_registry, mock):
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()
        mock_get.return_value = mock_oai_registry
        mock_registry.return_value = False
        mock.return_value = OaiPmhMessage.get_message_labelled(self.error_message % "identify"), status.\
            HTTP_500_INTERNAL_SERVER_ERROR

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as e:
            oai_registry_api.update_registry_info(mock_oai_registry)

        self.assertEqual(e.exception.message, self.error_message % "identify")
        self.assertEqual(e.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch.object(oai_verbs_api, 'identify_as_object')
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(OaiRegistry, 'check_registry_url_already_exists')
    @patch.object(OaiRegistry, 'get_by_id')
    def test_update_registry_info_raises_exception_if_bad_sets(self, mock_get, mock_registry, mock_sets,
                                                                     mock_identify):
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()
        mock_get.return_value = mock_oai_registry
        mock_identify.return_value = [], status.HTTP_200_OK
        mock_registry.return_value = False
        mock_sets.return_value = OaiPmhMessage.get_message_labelled(self.error_message % "sets"), status.\
            HTTP_500_INTERNAL_SERVER_ERROR

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as e:
            oai_registry_api.update_registry_info(mock_oai_registry)

        self.assertEqual(e.exception.message, self.error_message % "sets")
        self.assertEqual(e.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(OaiRegistry, 'check_registry_url_already_exists')
    @patch.object(OaiRegistry, 'get_by_id')
    def test_update_registry_info_raises_exception_if_bad_metadata_formats(self, mock_get, mock_registry,
                                                                                 mock_metadata_formats,
                                                                                 mock_identify, mock_sets):
        # Arrange
        mock_oai_registry = _create_mock_oai_registry()
        mock_get.return_value = mock_oai_registry
        mock_sets.return_value = [], status.HTTP_200_OK
        mock_identify.return_value = [], status.HTTP_200_OK
        mock_registry.return_value = False
        mock_metadata_formats.return_value = OaiPmhMessage.get_message_labelled(self.error_message % "metadataFormat"),\
            status.HTTP_500_INTERNAL_SERVER_ERROR

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException) as e:
            oai_registry_api.update_registry_info(mock_oai_registry)

        self.assertEqual(e.exception.message, self.error_message % "metadataFormat")
        self.assertEqual(e.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


def _generic_get_all_test(self, mock_get_all, act_function):
    # Arrange
    mock_oai_registry1 = _create_mock_oai_registry()
    mock_oai_registry2 = _create_mock_oai_registry()

    mock_get_all.return_value = [mock_oai_registry1, mock_oai_registry2]

    # Act
    result = act_function

    # Assert
    self.assertTrue(all(isinstance(item, OaiRegistry) for item in result))


def _create_oai_registry():
    """ Get an OaiRegistry object.

        Returns:
            OaiRegistry instance.

    """
    oai_registry = OaiRegistry()
    _set_oai_registry_fields(oai_registry)

    return oai_registry


def _create_mock_oai_registry():
    """ Mock an OaiRegistry.

        Returns:
            OaiRegistry mock.

    """
    mock_oai_registry = Mock(spec=OaiRegistry)
    _set_oai_registry_fields(mock_oai_registry)

    return mock_oai_registry


def _set_oai_registry_fields(oai_registry):
    """ Set OaiRegistry fields.

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
