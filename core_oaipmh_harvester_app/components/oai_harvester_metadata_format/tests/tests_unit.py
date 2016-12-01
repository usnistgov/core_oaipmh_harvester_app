from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
import core_oaipmh_harvester_app.components.oai_harvester_metadata_format.api as harvester_metadata_format_api
from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import OaiHarvesterMetadataFormat
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
import datetime


class TestOaiHarvesterMetadataFormatGetById(TestCase):
    @patch.object(OaiHarvesterMetadataFormat, 'get_by_id')
    def test_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        mock_oai_harvester_metadata_format = _create_mock_oai_harvester_metadata_format()

        mock_get_by_id.return_value = mock_oai_harvester_metadata_format

        # Act
        result = harvester_metadata_format_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, OaiHarvesterMetadataFormat)

    @patch.object(OaiHarvesterMetadataFormat, 'get_by_id')
    def test_get_by_id_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            harvester_metadata_format_api.get_by_id(mock_absent_id)

    @patch.object(OaiHarvesterMetadataFormat, 'get_by_id')
    def test_get_by_id_raises_exception_if_internal_error(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            harvester_metadata_format_api.get_by_id(mock_absent_id)


class TestOaiHarvesterMetadataFormatGetByMetadataPrefixAndRegistryId(TestCase):
    @patch.object(OaiHarvesterMetadataFormat, 'get_by_metadata_prefix_and_registry_id')
    def test_get_by_metadata_prefix_and_registry_id_return_object(self, mock_get):
        # Arrange
        mock_oai_harvester_metadata_format = _create_mock_oai_harvester_metadata_format()

        mock_get.return_value = mock_oai_harvester_metadata_format

        # Act
        result = harvester_metadata_format_api.\
            get_by_metadata_prefix_and_registry_id(mock_oai_harvester_metadata_format.metadata_prefix,
                                                   mock_oai_harvester_metadata_format.registry.id)

        # Assert
        self.assertIsInstance(result, OaiHarvesterMetadataFormat)

    @patch.object(OaiHarvesterMetadataFormat, 'get_by_metadata_prefix_and_registry_id')
    def test_get_by_metadata_prefix_and_registry_id_raises_exception_if_object_does_not_exist(self, mock_get):
        # Arrange
        mock_absent_metadata_prefix = 'oai_test'
        mock_absent_registry_id = str(ObjectId())

        mock_get.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            harvester_metadata_format_api.get_by_metadata_prefix_and_registry_id(mock_absent_metadata_prefix,
                                                                                 mock_absent_registry_id)

    @patch.object(OaiHarvesterMetadataFormat, 'get_by_metadata_prefix_and_registry_id')
    def test_get_by_metadata_prefix_and_registry_id_raises_exception_if_internal_error(self, mock_get):
        # Arrange
        mock_absent_metadata_prefix = 'oai_test'
        mock_absent_registry_id = str(ObjectId())

        mock_get.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            harvester_metadata_format_api.get_by_metadata_prefix_and_registry_id(mock_absent_metadata_prefix,
                                                                                 mock_absent_registry_id)


class TestOaiHarvesterMetadataFormatGetAll(TestCase):
    @patch.object(OaiHarvesterMetadataFormat, 'get_all')
    def test_get_all_contains_only_oai_harvester_metadata_format(self, mock_get_all):
        # Arrange
        mock_oai_harvester_metadata_format1 = _create_mock_oai_harvester_metadata_format()
        mock_oai_harvester_metadata_format2 = _create_mock_oai_harvester_metadata_format()

        mock_get_all.return_value = [mock_oai_harvester_metadata_format1, mock_oai_harvester_metadata_format2]

        # Act
        result = harvester_metadata_format_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterMetadataFormat) for item in result))


class TestOaiHarvesterMetadataFormatGetAllByRegistryId(TestCase):
    @patch.object(OaiHarvesterMetadataFormat, 'get_all_by_registry_id')
    def test_get_all_contains_only_oai_harvester_metadata_format(self, mock_get_all_by_registry_id):
        # Arrange
        mock_oai_harvester_metadata_format1 = _create_mock_oai_harvester_metadata_format()
        mock_oai_harvester_metadata_format2 = _create_mock_oai_harvester_metadata_format()

        mock_get_all_by_registry_id.return_value = [mock_oai_harvester_metadata_format1,
                                                    mock_oai_harvester_metadata_format2]

        # Act
        result = harvester_metadata_format_api.get_all_by_registry_id(mock_oai_harvester_metadata_format1.registry.id)

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterMetadataFormat) for item in result))


class TestOaiHarvesterMetadataFormatGetAllToHarvestByRegistryId(TestCase):
    @patch.object(OaiHarvesterMetadataFormat, 'get_all_by_registry_id_and_harvest')
    def test_get_all_contains_only_oai_harvester_metadata_format_to_harvest_by_registry_id(self, mock_get_all):
        # Arrange
        mock_oai_harvester_metadata_format1 = _create_mock_oai_harvester_metadata_format()
        mock_oai_harvester_metadata_format2 = _create_mock_oai_harvester_metadata_format()

        mock_get_all.return_value = [mock_oai_harvester_metadata_format1, mock_oai_harvester_metadata_format2]

        # Act
        result = harvester_metadata_format_api.\
            get_all_to_harvest_by_registry_id(mock_oai_harvester_metadata_format1.registry.id)

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterMetadataFormat) for item in result))


class TestOaiHarvestMetadataFormatUpsert(TestCase):
    def setUp(self):
        self.oai_harvester_metadata_format = _create_oai_harvester_metadata_format()

    @patch.object(OaiHarvesterMetadataFormat, 'save')
    def test_upsert_oai_harvester_raises_exception_if_save_failed(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.upsert(self.oai_harvester_metadata_format)

    @patch.object(OaiHarvesterMetadataFormat, 'save')
    def test_upsert_oai_harvester_metadata_format_return_object(self, mock_create):
        # Arrange
        mock_create.return_value = self.oai_harvester_metadata_format

        # Act
        result = harvester_metadata_format_api.upsert(self.oai_harvester_metadata_format)

        # Assert
        self.assertIsInstance(result, OaiHarvesterMetadataFormat)


class TestOaiHarvesterMetadataFormatDeleteAllByRegistryId(TestCase):
    @patch.object(OaiHarvesterMetadataFormat, 'delete_all_by_registry_id')
    def test_delete_all_by_registry_id_raises_exception_if_object_does_not_exist(self, mock_delete_all):
        # Arrange
        mock_absent_registry = str(ObjectId())

        mock_delete_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.delete_all_by_registry_id(mock_absent_registry)


class TestOaiHarvesterMetadataFormatDelete(TestCase):
    @patch.object(OaiHarvesterMetadataFormat, 'delete')
    def test_delete_oai_harvester_metadata_format_raises_exception_if_object_does_not_exist(self, mock_delete):
        # Arrange
        oai_harvester_metadata_format = _create_oai_harvester_metadata_format()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.delete(oai_harvester_metadata_format)


class TestOaiHarvesterMetadataFormatUpdateForAllByRegistryId(TestCase):
    @patch.object(OaiHarvesterMetadataFormat, 'update_for_all_harvest_by_registry_id')
    def test_update_for_all_harvest_by_registry_id_raises_exception_if_object_does_not_exist(self, mock_update_all):
        # Arrange
        mock_absent_registry = str(ObjectId())

        mock_update_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.update_for_all_harvest_by_registry_id(registry_id=mock_absent_registry,
                                                                                harvest=True)


class TestOaiHarvesterMetadataFormatUpdateForAllByListIds(TestCase):
    @patch.object(OaiHarvesterMetadataFormat, 'update_for_all_harvest_by_list_ids')
    def test_update_for_all_harvest_by_list_ids_raises_exception_if_object_does_not_exist(self, mock_update_all):
        # Arrange
        mock_absent_list_ids = [str(ObjectId()), str(ObjectId())]

        mock_update_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_api.update_for_all_harvest_by_list_ids(mock_absent_list_ids, True)


def _create_oai_harvester_metadata_format():
    """ Get an OaiHarvesterMetadataFormat object.

    Returns:
        OaiHarvesterMetadataFormat instance.

    """
    oai_harvester_metadata_format = OaiHarvesterMetadataFormat()
    _set_oai_harvester_metadata_format_fields(oai_harvester_metadata_format)

    return oai_harvester_metadata_format


def _create_mock_oai_harvester_metadata_format():
    """ Mock an OaiHarvesterMetadataFormat.

    Returns:
        OaiHarvesterMetadataFormat mock.

    """
    mock_oai_harvester_metadata_format = Mock(spec=OaiHarvesterMetadataFormat)
    _set_oai_harvester_metadata_format_fields(mock_oai_harvester_metadata_format)

    return mock_oai_harvester_metadata_format


def _set_oai_harvester_metadata_format_fields(oai_harvester_metadata_format):
    """ Set OaiHarvesterMetadataFormat fields.

    Args:
        oai_harvester_metadata_format:

    Returns:
        OaiHarvesterMetadataFormat with assigned fields.

    """
    oai_harvester_metadata_format.metadata_prefix = "test"
    oai_harvester_metadata_format.schema = "http://test.com/test.xsd"
    oai_harvester_metadata_format.xml_schema = "<root><test>Hello</test></root>"
    oai_harvester_metadata_format.metadata_namespace = 'http://test.com/meta'
    oai_harvester_metadata_format.raw = dict()
    oai_harvester_metadata_format.template = ObjectId()
    oai_harvester_metadata_format.registry = OaiRegistry()
    oai_harvester_metadata_format.hash = 'eaedb2e2d29fffeee628a51284a237e057a38a28'
    oai_harvester_metadata_format.harvest = True
    oai_harvester_metadata_format.lastUpdate = datetime.datetime.now()

    return oai_harvester_metadata_format