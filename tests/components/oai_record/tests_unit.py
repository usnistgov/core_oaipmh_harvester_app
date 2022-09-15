import datetime
from unittest.case import TestCase
from unittest.mock import Mock, patch


from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
import core_oaipmh_harvester_app.components.oai_record.api as oai_record_api
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class TestOaiRecordGetById(TestCase):
    """Test Oai Record Get By Id"""

    @patch.object(OaiRecord, "get_by_id")
    def test_get_by_id_return_object(self, mock_get_by_id):
        """test_get_by_id_return_object"""

        # Arrange
        mock_oai_record = _create_mock_oai_record()
        mock_user = create_mock_user("1", is_anonymous=False)

        mock_get_by_id.return_value = mock_oai_record

        # Act
        result = oai_record_api.get_by_id(mock_get_by_id.id, mock_user)

        # Assert
        self.assertIsInstance(result, OaiRecord)

    @patch.object(OaiRecord, "get_by_id")
    def test_get_by_id_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        """test_get_by_id_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_id = 1
        mock_user = create_mock_user("1", is_anonymous=False)

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            oai_record_api.get_by_id(mock_absent_id, mock_user)

    @patch.object(OaiRecord, "get_by_id")
    def test_get_by_id_raises_exception_if_internal_error(self, mock_get_by_id):
        """test_get_by_id_raises_exception_if_internal_error"""

        # Arrange
        mock_absent_id = 1
        mock_user = create_mock_user("1", is_anonymous=False)

        mock_get_by_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            oai_record_api.get_by_id(mock_absent_id, mock_user)


class TestOaiRecordGetAllByRegistryId(TestCase):
    """Test Oai Record Get All By Registry Id"""

    @patch.object(OaiRecord, "get_all_by_registry_id")
    def test_get_all_by_registry_id_return_object(self, mock_get_all):
        """test_get_all_by_registry_id_return_object"""

        _generic_get_all_test(
            self, mock_get_all, oai_record_api.get_all_by_registry_id(1)
        )


class TestOaiRecordGetAll(TestCase):
    """Test Oai Record Get All"""

    @patch.object(OaiRecord, "get_all")
    def test_get_all_contains_only_oai_record(self, mock_get_all):
        """test_get_all_contains_only_oai_record"""

        _generic_get_all_test(self, mock_get_all, oai_record_api.get_all())


class TestOaiRecordGetCountByRegistryId(TestCase):
    """Test Oai Record Get Count By Registry Id"""

    @patch.object(OaiRecord, "get_count_by_registry_id")
    def test_get_count_by_registry_id_return_number(self, mock_get):
        """test_get_count_by_registry_id_return_number"""

        # Arrange
        mock_registry_id = 1
        mock_user = create_mock_user("1", is_anonymous=False)

        mock_get.return_value = 2

        # Act
        result = oai_record_api.get_count_by_registry_id(mock_registry_id, mock_user)

        # Assert
        self.assertEqual(result, 2)


class TestOaiRecordDelete(TestCase):
    """Test Oai Record Delete"""

    @patch.object(OaiRecord, "delete")
    def test_delete_oai_record_raises_exception_if_object_does_not_exist(
        self, mock_delete
    ):
        """test_delete_oai_record_raises_exception_if_object_does_not_exist"""

        # Arrange
        oai_record = _create_oai_record()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            oai_record_api.delete(oai_record)


def _generic_get_all_test(self, mock_get_all, act_function):
    """_generic_get_all_test

    Args:
        mock_get_all:
        act_function:

    Returns:

    """
    # Arrange
    mock_oai_record1 = _create_mock_oai_record()
    mock_oai_record2 = _create_mock_oai_record()

    mock_get_all.return_value = [mock_oai_record1, mock_oai_record2]

    # Act
    result = act_function

    # Assert
    self.assertTrue(all(isinstance(item, OaiRecord) for item in result))


def _create_oai_record():
    """Get an OaiRecord object.

    Returns:
        OaiRecord instance.

    """
    oai_record = OaiRecord()
    _set_oai_record_fields(oai_record)

    return oai_record


def _create_mock_oai_record():
    """Mock an OaiRecord.

    Returns:
        OaiRecord mock.

    """
    mock_oai_record = Mock(spec=OaiRecord)
    _set_oai_record_fields(mock_oai_record)

    return mock_oai_record


def _set_oai_record_fields(oai_record):
    """Set OaiRecord fields.

    Args:
        oai_record:

    Returns:
        OaiRecord with assigned fields.

    """
    oai_record.identifier = "oai:test/id.0006"
    oai_record.last_modification_date = datetime.datetime.now()
    oai_record.deleted = False
    # oai_record.harvester_sets = [OaiHarvesterSet(), OaiHarvesterSet()]
    oai_record.harvester_metadata_format = OaiHarvesterMetadataFormat()
    oai_record.registry = OaiRegistry()
    oai_record.xml_content = "<test><message>Hello</message></test>"

    return oai_record
