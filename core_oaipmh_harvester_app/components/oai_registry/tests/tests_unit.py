from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
import core_oaipmh_harvester_app.components.oai_registry.api as registry_api
from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify
import datetime


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
    @patch.object(OaiRegistry, 'get_all_by_is_deactivated')
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
    oai_registry.identify = OaiIdentify()
    oai_registry.description = "This is the registry"
    oai_registry.harvest = True
    oai_registry.last_update = datetime.datetime.now()
    oai_registry.is_harvesting = False
    oai_registry.is_updating = False
    oai_registry.is_deactivated = False
    oai_registry.is_queued = True

    return oai_registry
