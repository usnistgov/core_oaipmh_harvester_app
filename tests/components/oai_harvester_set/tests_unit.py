from builtins import str
from unittest.case import TestCase

from bson.objectid import ObjectId
from mock.mock import Mock, patch

import core_oaipmh_harvester_app.components.oai_harvester_set.api as harvester_set_api
from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class TestOaiHarvesterSetGetById(TestCase):
    @patch.object(OaiHarvesterSet, "get_by_id")
    def test_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        mock_oai_harvester_set = _create_mock_oai_harvester_set()
        mock_oai_harvester_set.id = ObjectId()

        mock_get_by_id.return_value = mock_oai_harvester_set

        # Act
        result = harvester_set_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)

    @patch.object(OaiHarvesterSet, "get_by_id")
    def test_get_by_id_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            harvester_set_api.get_by_id(mock_absent_id)

    @patch.object(OaiHarvesterSet, "get_by_id")
    def test_get_by_id_raises_exception_if_internal_error(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            harvester_set_api.get_by_id(mock_absent_id)


class TestOaiHarvesterSetGetBySetSpecAndRegistryId(TestCase):
    @patch.object(OaiHarvesterSet, "get_by_set_spec_and_registry_id")
    def test_get_by_set_spec_and_registry_id_return_object(self, mock_get):
        # Arrange
        mock_oai_harvester_set = _create_mock_oai_harvester_set()

        mock_get.return_value = mock_oai_harvester_set

        # Act
        result = harvester_set_api.get_by_set_spec_and_registry_id(
            mock_oai_harvester_set.set_spec, mock_oai_harvester_set.registry.id
        )

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)

    @patch.object(OaiHarvesterSet, "get_by_set_spec_and_registry_id")
    def test_get_by_set_spec_and_registry_id_raises_exception_if_object_does_not_exist(
        self, mock_get
    ):
        # Arrange
        mock_absent_set_spec = ObjectId()
        mock_absent_registry_id = ObjectId()

        mock_get.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            harvester_set_api.get_by_set_spec_and_registry_id(
                mock_absent_set_spec, mock_absent_registry_id
            )

    @patch.object(OaiHarvesterSet, "get_by_set_spec_and_registry_id")
    def test_get_by_set_spec_and_registry_id_raises_exception_if_internal_error(
        self, mock_get
    ):
        # Arrange
        mock_absent_set_spec = ObjectId()
        mock_absent_registry_id = ObjectId()

        mock_get.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            harvester_set_api.get_by_set_spec_and_registry_id(
                mock_absent_set_spec, mock_absent_registry_id
            )


class TestOaiHarvesterSetGetAll(TestCase):
    @patch.object(OaiHarvesterSet, "get_all")
    def test_get_all_contains_only_oai_harvester_set(self, mock_get_all):
        # Arrange
        mock_oai_harvester_set1 = _create_mock_oai_harvester_set()
        mock_oai_harvester_set2 = _create_mock_oai_harvester_set()

        mock_get_all.return_value = [mock_oai_harvester_set1, mock_oai_harvester_set2]

        # Act
        result = harvester_set_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in result))


class TestOaiHarvesterSetGetAllByRegistryId(TestCase):
    @patch.object(OaiHarvesterSet, "get_all_by_registry_id")
    def test_get_all_contains_only_oai_harvester_set(self, mock_get_all_by_registry_id):
        # Arrange
        mock_oai_harvester_set1 = _create_mock_oai_harvester_set()
        mock_oai_harvester_set2 = _create_mock_oai_harvester_set()

        mock_get_all_by_registry_id.return_value = [
            mock_oai_harvester_set1,
            mock_oai_harvester_set2,
        ]

        # Act
        result = harvester_set_api.get_all_by_registry_id(
            registry_id=mock_oai_harvester_set1.registry.id
        )

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in result))


class TestOaiHarvesterSetGetAllToHarvestByRegistryId(TestCase):
    @patch.object(OaiHarvesterSet, "get_all_by_registry_id_and_harvest")
    def test_get_all_contains_only_oai_harvester_set_to_harvest_by_registry_id(
        self, mock_get_all
    ):
        # Arrange
        mock_oai_harvester_set1 = _create_mock_oai_harvester_set()
        mock_oai_harvester_set2 = _create_mock_oai_harvester_set()

        mock_get_all.return_value = [mock_oai_harvester_set1, mock_oai_harvester_set2]

        # Act
        result = harvester_set_api.get_all_to_harvest_by_registry_id(
            mock_oai_harvester_set1.registry.id
        )

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in result))


class TestOaiHarvestSetUpsert(TestCase):
    def setUp(self):
        self.oai_harvester_set = _create_oai_harvester_set()

    @patch.object(OaiHarvesterSet, "save")
    def test_upsert_oai_harvester_raises_exception_if_save_failed(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_set_api.upsert(self.oai_harvester_set)

    @patch.object(OaiHarvesterSet, "save")
    def test_upsert_oai_harvester_return_object(self, mock_create):
        # Arrange
        mock_create.return_value = self.oai_harvester_set

        # Act
        result = harvester_set_api.upsert(self.oai_harvester_set)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)


class TestOaiHarvesterSetDeleteAllByRegistryId(TestCase):
    @patch.object(OaiHarvesterSet, "delete_all_by_registry_id")
    def test_delete_all_by_registry_id_raises_exception_if_object_does_not_exist(
        self, mock_delete_all
    ):
        # Arrange
        mock_absent_registry_id = ObjectId()

        mock_delete_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_set_api.delete_all_by_registry_id(mock_absent_registry_id)


class TestOaiHarvesterSetDelete(TestCase):
    @patch.object(OaiHarvesterSet, "delete")
    def test_delete_oai_harvester_set_raises_exception_if_object_does_not_exist(
        self, mock_delete
    ):
        # Arrange
        oai_harvester_set = _create_oai_harvester_set()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            harvester_set_api.delete(oai_harvester_set)


class TestOaiHarvesterSetUpdateForAllByRegistryId(TestCase):
    @patch.object(OaiHarvesterSet, "update_for_all_harvest_by_registry_id")
    def test_update_for_all_harvest_by_registry_id_raises_exception_if_object_does_not_exist(
        self, mock_update_all
    ):
        # Arrange
        mock_absent_registry_id = ObjectId()

        mock_update_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_set_api.update_for_all_harvest_by_registry_id(
                registry_id=mock_absent_registry_id, harvest=True
            )


class TestOaiSetUpdateForAllByListIds(TestCase):
    @patch.object(OaiHarvesterSet, "update_for_all_harvest_by_list_ids")
    def test_update_for_all_harvest_by_list_ids_raises_exception_if_object_does_not_exist(
        self, mock_update_all
    ):
        # Arrange
        mock_absent_list_ids = [str(ObjectId()), str(ObjectId())]

        mock_update_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            harvester_set_api.update_for_all_harvest_by_list_ids(
                mock_absent_list_ids, True
            )


def _create_oai_harvester_set():
    """Get an OaiHarvesterSet object.

    Returns:
        OaiHarvesterSet instance.

    """
    oai_harvester_set = OaiHarvesterSet()
    _set_oai_harvester_set_fields(oai_harvester_set)

    return oai_harvester_set


def _create_mock_oai_harvester_set():
    """Mock an OaiHarvesterSet.

    Returns:
        OaiHarvesterSet mock.

    """
    mock_oai_harvester_set = Mock(spec=OaiHarvesterSet)
    _set_oai_harvester_set_fields(mock_oai_harvester_set)

    return mock_oai_harvester_set


def _set_oai_harvester_set_fields(oai_harvester_set):
    """Set OaiHarvesterSet fields.

    Args:
        oai_harvester_set:

    Returns:
        OaiHarvesterSet with assigned fields.

    """
    oai_harvester_set.set_spec = "oai_test"
    oai_harvester_set.set_name = "test"
    oai_harvester_set.raw = dict()
    oai_harvester_set.registry = OaiRegistry()
    oai_harvester_set.harvest = True

    return oai_harvester_set
