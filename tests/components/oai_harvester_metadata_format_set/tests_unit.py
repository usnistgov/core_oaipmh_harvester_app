import datetime
from unittest.case import TestCase

from bson.objectid import ObjectId
from mock.mock import Mock, patch

import core_oaipmh_harvester_app.components.oai_harvester_metadata_format_set.api as harvester_metadata_format_set_api
from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format_set.models import (
    OaiHarvesterMetadataFormatSet,
)


class TestOaiHarvesterMetadataFormatSetGetByMetadataAndSet(TestCase):
    @patch.object(OaiHarvesterMetadataFormatSet, "get_by_metadata_format_and_set")
    def test_get_by_metadata_format_and_set_return_object(
        self, get_by_metadata_format_and_set
    ):
        # Arrange
        mock_oai_harvester_metadata_format_set = (
            _create_mock_oai_harvester_metadata_format_set()
        )

        get_by_metadata_format_and_set.return_value = (
            mock_oai_harvester_metadata_format_set
        )

        # Act
        result = harvester_metadata_format_set_api.get_by_metadata_format_and_set(
            mock_oai_harvester_metadata_format_set.harvester_metadata_format,
            mock_oai_harvester_metadata_format_set.harvester_set,
        )

        # Assert
        self.assertIsInstance(result, OaiHarvesterMetadataFormatSet)

    @patch.object(OaiHarvesterMetadataFormatSet, "get_by_metadata_format_and_set")
    def test_get_by_metadata_format_and_set_raises_exception_if_object_does_not_exist(
        self, get_by_metadata_format_and_set
    ):
        # Arrange
        mock_absent_metadata_format = ObjectId()
        mock_absent_set = ObjectId()

        get_by_metadata_format_and_set.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            harvester_metadata_format_set_api.get_by_metadata_format_and_set(
                mock_absent_metadata_format, mock_absent_set
            )

    @patch.object(OaiHarvesterMetadataFormatSet, "get_by_metadata_format_and_set")
    def test_get_by_metadata_format_and_set_raises_exception_if_internal_error(
        self, get_by_metadata_format_and_set
    ):
        # Arrange
        mock_absent_metadata_format = ObjectId()
        mock_absent_set = ObjectId()

        get_by_metadata_format_and_set.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            harvester_metadata_format_set_api.get_by_metadata_format_and_set(
                mock_absent_metadata_format, mock_absent_set
            )


class TestOaiHarvestMetadataFormatSetUpsert(TestCase):
    def setUp(self):
        self.oai_harvester_metadata_format_set = (
            _create_oai_harvester_metadata_format_set()
        )

    @patch.object(OaiHarvesterMetadataFormatSet, "save")
    def test_upsert_oai_harvester_metadata_format_set_raises_exception_if_save_failed(
        self, mock_save
    ):
        # Arrange
        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_set_api.upsert(
                self.oai_harvester_metadata_format_set
            )

    @patch.object(OaiHarvesterMetadataFormatSet, "save")
    def test_upsert_oai_harvester_metadata_format_set_return_object(self, mock_create):
        # Arrange
        mock_create.return_value = self.oai_harvester_metadata_format_set

        # Act
        result = harvester_metadata_format_set_api.upsert(
            self.oai_harvester_metadata_format_set
        )

        # Assert
        self.assertIsInstance(result, OaiHarvesterMetadataFormatSet)


class TestOaiHarvestMetadataFormatSetUpsertLastUpdate(TestCase):
    def setUp(self):
        self.oai_harvester_metadata_format_set = (
            _create_oai_harvester_metadata_format_set()
        )

    @patch.object(
        OaiHarvesterMetadataFormatSet, "upsert_last_update_by_metadata_format_and_set"
    )
    def test_upsert_last_update_raises_exception_if_save_failed(
        self, mock_upsert_last_update
    ):
        # Arrange
        mock_upsert_last_update.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_metadata_format_set_api.upsert_last_update_by_metadata_format_and_set(
                self.oai_harvester_metadata_format_set.harvester_metadata_format,
                self.oai_harvester_metadata_format_set.harvester_set,
                datetime.datetime.now(),
            )


class TestOaiHarvestMetadataFormatSetGetLastUpdateByMetadataFormatAndSet(TestCase):
    @patch.object(OaiHarvesterMetadataFormatSet, "get_by_metadata_format_and_set")
    def test_get_last_update_by_metadata_format_and_set(
        self, get_by_metadata_format_and_set
    ):
        # Arrange
        oai_harvester_metadata_format_set = _create_oai_harvester_metadata_format_set()
        oai_harvester_metadata_format_set.last_update = datetime.datetime(
            year=2016, month=11, day=21, hour=8, minute=40, second=33
        )

        get_by_metadata_format_and_set.return_value = oai_harvester_metadata_format_set

        # Act
        result = harvester_metadata_format_set_api.get_last_update_by_metadata_format_and_set(
            oai_harvester_metadata_format_set.harvester_metadata_format,
            oai_harvester_metadata_format_set.harvester_set,
        )

        # Assert
        self.assertEquals(result, "2016-11-21T08:40:33Z")


def _create_oai_harvester_metadata_format_set():
    """Get an OaiHarvesterMetadataFormatSet object.

    Returns:
        OaiHarvesterMetadataFormatSet instance.

    """
    oai_harvester_metadata_format_set = OaiHarvesterMetadataFormatSet()
    _set_oai_harvester_metadata_format_set_fields(oai_harvester_metadata_format_set)

    return oai_harvester_metadata_format_set


def _create_mock_oai_harvester_metadata_format_set():
    """Mock an OaiHarvesterMetadataFormatSet.

    Returns:
        OaiHarvesterMetadataFormatSet mock.

    """
    mock_oai_harvester_metadata_format = Mock(spec=OaiHarvesterMetadataFormatSet)
    _set_oai_harvester_metadata_format_set_fields(mock_oai_harvester_metadata_format)

    return mock_oai_harvester_metadata_format


def _set_oai_harvester_metadata_format_set_fields(oai_harvester_metadata_format_set):
    """Set OaiHarvesterMetadataFormatSet fields.

    Args:
        oai_harvester_metadata_format_set:

    Returns:
        OaiHarvesterMetadataFormatSet with assigned fields.

    """
    oai_harvester_metadata_format_set.harvester_metadata_format = "test"
    oai_harvester_metadata_format_set.harvester_set = "http://test.com/test.xsd"
    oai_harvester_metadata_format_set.last_update = datetime.datetime.now()

    return oai_harvester_metadata_format_set
