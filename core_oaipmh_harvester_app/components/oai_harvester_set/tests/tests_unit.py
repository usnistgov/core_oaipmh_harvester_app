from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
import core_oaipmh_harvester_app.components.oai_harvester_set.api as harvester_set_api
from core_main_app.commons.exceptions import MDCSError
from core_oaipmh_harvester_app.components.oai_harvester_set.models import OaiHarvesterSet


class TestOaiHarvesterSetGetById(TestCase):

    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_by_id')
    def test_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        mock_oai_harvester_set = _get_oai_harvester_set_mock()

        mock_get_by_id.return_value = mock_oai_harvester_set

        # Act
        result = harvester_set_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)

    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_by_id')
    def test_get_by_id_throws_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            harvester_set_api.get_by_id(mock_absent_id)


class TestOaiHarvesterSetGetBySetSpecAndRegistry(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_by_set_spec_and_registry')
    def test_get_by_set_spec_and_registry_return_object(self, mock_get):
        # Arrange
        mock_oai_harvester_set = _get_oai_harvester_set_mock()

        mock_get.return_value = mock_oai_harvester_set

        # Act
        result = harvester_set_api.get_by_set_spec_and_registry(mock_oai_harvester_set.setSpec,
                                                                mock_oai_harvester_set.registry)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)

    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_by_set_spec_and_registry')
    def test_get_by_set_spec_and_registry_throws_exception_if_object_does_not_exist(self, mock_get):
        # Arrange
        mock_absent_set_spec = ObjectId()
        mock_absent_registry = ObjectId()

        mock_get.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            harvester_set_api.get_by_set_spec_and_registry(mock_absent_set_spec, mock_absent_registry)


class TestOaiHarvesterSetGetAll(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_all')
    def test_get_all_contains_only_oai_harvester_set(self, mock_get_all):
        # Arrange
        mock_oai_harvester_set1 = _get_oai_harvester_set_mock()
        mock_oai_harvester_set2 = _get_oai_harvester_set_mock()

        mock_get_all.return_value = [mock_oai_harvester_set1, mock_oai_harvester_set2]

        # Act
        result = harvester_set_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in result))


class TestOaiHarvesterSetGetAllByRegistry(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_all_by_registry')
    def test_get_all_contains_only_oai_harvester_set(self, mock_get_all_by_registry):
        # Arrange
        mock_oai_harvester_set1 = _get_oai_harvester_set_mock()
        mock_oai_harvester_set2 = _get_oai_harvester_set_mock()

        mock_get_all_by_registry.return_value = [mock_oai_harvester_set1, mock_oai_harvester_set2]

        # Act
        result = harvester_set_api.get_all_by_registry(registry=mock_oai_harvester_set1.registry)

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in result))

    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_all_by_registry')
    def test_get_all_contains_only_oai_harvester_set_throws_exception_if_object_does_not_exist(self, mock_get_all):
        # Arrange
        mock_absent_registry = str(ObjectId())

        mock_get_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            harvester_set_api.get_all_by_registry(mock_absent_registry)


class TestOaiHarvesterSetGetAllToHarvestByRegistry(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.'
           'get_all_by_registry_and_harvest')
    def test_get_all_contains_only_oai_harvester_set_to_harvest_by_registry(self, mock_get_all):
        # Arrange
        mock_oai_harvester_set1 = _get_oai_harvester_set_mock()
        mock_oai_harvester_set2 = _get_oai_harvester_set_mock()

        mock_get_all.return_value = [mock_oai_harvester_set1, mock_oai_harvester_set2]

        # Act
        result = harvester_set_api.get_all_to_harvest_by_registry(mock_oai_harvester_set1.registry)

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in result))

    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.'
           'get_all_by_registry_and_harvest')
    def test_list_contains_only_oai_harvester_set_to_harvest_by_registry_throws_exception_if_object_does_not_exist(
                                                                                                        self,
                                                                                                        mock_get_all):
        # Arrange
        mock_absent_registry = str(ObjectId())

        mock_get_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            harvester_set_api.get_all_to_harvest_by_registry(mock_absent_registry)


class TestOaiHarvestSetSave(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.create_oai_harvester_set')
    def test_save_oai_harvester_set(self, mock_create):
        # Arrange
        mock_oai_harvester_set = _get_oai_harvester_set_mock()

        mock_create.return_value = mock_oai_harvester_set

        # Act
        result = harvester_set_api._save(mock_oai_harvester_set.setSpec, mock_oai_harvester_set.setName,
                                         mock_oai_harvester_set.raw, mock_oai_harvester_set.registry,
                                         mock_oai_harvester_set.harvest)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)


class TestOaiHarvestSetUpdate(TestCase):
    def test_update_oai_harvester_set(self):
        # Arrange
        mock_oai_harvester_set = _get_oai_harvester_set_mock()

        # Act
        result = harvester_set_api._update(mock_oai_harvester_set, mock_oai_harvester_set.setName,
                                           mock_oai_harvester_set.raw, mock_oai_harvester_set.harvest)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)


class TestOaiHarvestSetSaveOrUpdate(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.create_oai_harvester_set')
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_by_set_spec_and_registry')
    def test_save_or_update_oai_harvester_set_without_existing_object(self, mock_get_by_set_spec_and_registry,
                                                                      mock_create):
        # Arrange
        mock_oai_harvester_set = _get_oai_harvester_set_mock()

        mock_create.return_value = mock_oai_harvester_set
        mock_get_by_set_spec_and_registry.side_effect = Exception()

        # Act
        result = harvester_set_api.save_or_update(mock_oai_harvester_set.setSpec, mock_oai_harvester_set.setName,
                                                  mock_oai_harvester_set.raw, mock_oai_harvester_set.registry,
                                                  mock_oai_harvester_set.harvest)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)

    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_by_set_spec_and_registry')
    def test_save_or_update_oai_harvester_set_with_existing_object(self, mock_get_by_set_spec_and_registry):
        # Arrange
        mock_oai_harvester_set = _get_oai_harvester_set_mock()

        mock_get_by_set_spec_and_registry.return_value = mock_oai_harvester_set

        # Act
        result = harvester_set_api.save_or_update(mock_oai_harvester_set.setSpec, mock_oai_harvester_set.setName,
                                                  mock_oai_harvester_set.raw, mock_oai_harvester_set.registry,
                                                  mock_oai_harvester_set.harvest)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)


class TestOaiHarvesterSetDeleteAllByRegistry(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.delete_all_by_registry')
    def test_delete_all_by_registry_throws_exception_if_object_does_not_exist(self, mock_delete_all):
        # Arrange
        mock_absent_registry = str(ObjectId())

        mock_delete_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            harvester_set_api.delete_all_by_registry(mock_absent_registry)


class TestOaiHarvesterSetUpdateForAllByRegistry(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.'
           'update_for_all_harvest_by_registry')
    def test_update_for_all_harvest_by_registry_throws_exception_if_object_does_not_exist(self, mock_update_all):
        # Arrange
        mock_absent_registry = str(ObjectId())

        mock_update_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            harvester_set_api.update_for_all_harvest_by_registry(registry=mock_absent_registry, harvest=True)


def _get_oai_harvester_set_mock():
    """
    Mock an OaiHarvestSet object
    :return:
    """
    mock_oai_harvester_set = Mock(spec=OaiHarvesterSet)
    mock_oai_harvester_set.setSpec = "oai_test"
    mock_oai_harvester_set.setName = "test"
    mock_oai_harvester_set.id = ObjectId()
    mock_oai_harvester_set.raw = '<set xmlns="http://www.openarchives.org/OAI/2.0/" ' \
                                 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' \
                                 '<setSpec>soft</setSpec>' \
                                 '<setName>software</setName>' \
                                 '<setDescription><oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/' \
                                 'oai_dc/" ' \
                                 'xmlns:dc="http://purl.org/dc/elements/1.1/" ' \
                                 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
                                 'xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ ' \
                                 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd">' \
                                 '<dc:description xml:lang="en">\n Get software records\n' \
                                 '</dc:description></oai_dc:dc></setDescription></set>'
    mock_oai_harvester_set.registry = str(ObjectId())
    mock_oai_harvester_set.harvest = True

    return mock_oai_harvester_set
