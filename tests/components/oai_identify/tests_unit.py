from builtins import str
from unittest.case import TestCase

from bson.objectid import ObjectId
from mock.mock import Mock, patch

import core_oaipmh_harvester_app.components.oai_identify.api as oai_identify_api
from core_main_app.commons import exceptions
from core_main_app.utils.xml import OrderedDict
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class TestOaiIdentifyUpsert(TestCase):
    def setUp(self):
        self.oai_identify = _create_oai_identify()

    @patch.object(OaiIdentify, "save")
    def test_upsert_oai_identifier_raises_exception_if_save_failed(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            oai_identify_api.upsert(self.oai_identify)

    @patch.object(OaiIdentify, "save")
    def test_upsert_oai_identify_with_raw_return_object(self, mock_create):
        # Arrange
        mock_create.return_value = self.oai_identify

        # Act
        result = oai_identify_api.upsert(self.oai_identify)

        # Assert
        self.assertIsInstance(result, OaiIdentify)

    @patch.object(OaiIdentify, "save")
    def test_upsert_oai_identify_without_raw_return_object(self, mock_create):
        # Arrange
        self.oai_identify.raw = {}

        mock_create.return_value = self.oai_identify

        # Act
        result = oai_identify_api.upsert(self.oai_identify)

        # Assert
        self.assertIsInstance(result, OaiIdentify)

    @patch.object(OaiIdentify, "save")
    def test_upsert_oai_identify_invalid_raw_return_object(self, mock_create):
        # Arrange
        self.oai_identify.raw = "<root?</root>"

        mock_create.return_value = self.oai_identify

        # Act
        result = oai_identify_api.upsert(self.oai_identify)

        # Act + Assert
        self.assertIsInstance(result, OaiIdentify)

    @patch.object(OaiIdentify, "save")
    def test_upsert_oai_identify_invalid_raw_return_empty_raw(self, mock_create):
        # Arrange
        self.oai_identify.raw = "<root?</root>"

        mock_create.return_value = self.oai_identify

        # Act
        result = oai_identify_api.upsert(self.oai_identify)

        # Act + Assert
        self.assertEquals(result.raw, {})

    @patch.object(OaiIdentify, "save")
    def test_upsert_oai_identify_no_exception_if_raw_not_string(self, mock_create):
        # Arrange
        self.oai_identify.raw = OrderedDict([("test", "Hello")])

        mock_create.return_value = self.oai_identify

        # Act
        result = oai_identify_api.upsert(self.oai_identify)

        # Assert
        self.assertIsInstance(result, OaiIdentify)


class TestOaiIdentifyGetByRegistryId(TestCase):
    @patch.object(OaiIdentify, "get_by_registry_id")
    def test_get_by_registry_id_return_object(self, mock_get):
        # Arrange
        mock_oai_identify = _create_mock_oai_identify()

        mock_get.return_value = mock_oai_identify

        # Act
        result = oai_identify_api.get_by_registry_id(mock_oai_identify.registry.id)

        # Assert
        self.assertIsInstance(result, OaiIdentify)

    @patch.object(OaiIdentify, "get_by_registry_id")
    def test_get_by_registry_id_raises_exception_if_object_does_not_exist(
        self, mock_get
    ):
        # Arrange
        mock_absent_registry_id = str(ObjectId())

        mock_get.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            oai_identify_api.get_by_registry_id(mock_absent_registry_id)

    @patch.object(OaiIdentify, "get_by_registry_id")
    def test_get_by_registry_id_raises_exception_if_internal_error(self, mock_get):
        # Arrange
        mock_absent_registry_id = str(ObjectId())

        mock_get.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            oai_identify_api.get_by_registry_id(mock_absent_registry_id)


class TestOaiIdentifyDelete(TestCase):
    @patch.object(OaiIdentify, "delete")
    def test_delete_oai_identify_raises_exception_if_object_does_not_exist(
        self, mock_delete
    ):
        # Arrange
        oai_identify = _create_oai_identify()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            oai_identify_api.delete(oai_identify)


def _create_oai_identify():
    """Get an OaiIdentify object.

    Returns:
        OaiIdentify instance.

    """
    return OaiIdentify()


def _create_mock_oai_identify():
    """Mock an OaiIdentify.

    Returns:
        OaiIdentify mock.

    """
    mock_oai_identify = Mock(spec=OaiIdentify)
    mock_oai_identify.registry = OaiRegistry()

    return mock_oai_identify
