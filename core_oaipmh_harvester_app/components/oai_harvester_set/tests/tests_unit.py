from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
import core_oaipmh_harvester_app.components.oai_harvester_set.api as harvester_set_api
from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_harvester_set.models import OaiHarvesterSet
from core_main_app.utils.xml import OrderedDict


class TestOaiHarvesterSetGetById(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_by_id')
    def test_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        mock_oai_harvester_set = _create_mock_oai_harvester_set()
        mock_oai_harvester_set.id = ObjectId()

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
        with self.assertRaises(exceptions.ApiError):
            harvester_set_api.get_by_id(mock_absent_id)


class TestOaiHarvesterSetGetBySetSpecAndRegistry(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_by_set_spec_and_registry')
    def test_get_by_set_spec_and_registry_return_object(self, mock_get):
        # Arrange
        mock_oai_harvester_set = _create_mock_oai_harvester_set()

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
        with self.assertRaises(exceptions.ApiError):
            harvester_set_api.get_by_set_spec_and_registry(mock_absent_set_spec, mock_absent_registry)


class TestOaiHarvesterSetGetAll(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_all')
    def test_get_all_contains_only_oai_harvester_set(self, mock_get_all):
        # Arrange
        mock_oai_harvester_set1 = _create_mock_oai_harvester_set()
        mock_oai_harvester_set2 = _create_mock_oai_harvester_set()

        mock_get_all.return_value = [mock_oai_harvester_set1, mock_oai_harvester_set2]

        # Act
        result = harvester_set_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in result))


class TestOaiHarvesterSetGetAllByRegistry(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.get_all_by_registry')
    def test_get_all_contains_only_oai_harvester_set(self, mock_get_all_by_registry):
        # Arrange
        mock_oai_harvester_set1 = _create_mock_oai_harvester_set()
        mock_oai_harvester_set2 = _create_mock_oai_harvester_set()

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
        with self.assertRaises(exceptions.ApiError):
            harvester_set_api.get_all_by_registry(mock_absent_registry)


class TestOaiHarvesterSetGetAllToHarvestByRegistry(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.'
           'get_all_by_registry_and_harvest')
    def test_get_all_contains_only_oai_harvester_set_to_harvest_by_registry(self, mock_get_all):
        # Arrange
        mock_oai_harvester_set1 = _create_mock_oai_harvester_set()
        mock_oai_harvester_set2 = _create_mock_oai_harvester_set()

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
        with self.assertRaises(exceptions.ApiError):
            harvester_set_api.get_all_to_harvest_by_registry(mock_absent_registry)


class TestOaiHarvestSetUpsert(TestCase):
    def setUp(self):
        self.oai_harvester_metadata_format = _create_oai_harvester_set()

    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.save')
    def test_upsert_oai_harvester_throws_exception_if_save_failed(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            harvester_set_api.upsert(self.oai_harvester_metadata_format)

    @patch(
        'core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.save')
    def test_upsert_oai_harvester_set_with_raw(self, mock_create):
        # Arrange
        mock_create.return_value = self.oai_harvester_metadata_format

        # Act
        result = harvester_set_api.upsert(self.oai_harvester_metadata_format)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)

    @patch(
        'core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.save')
    def test_upsert_oai_harvester_set_throws_exception_if_no_raw(self, mock_create):
        # Arrange
        self.oai_harvester_metadata_format.raw = {}

        mock_create.return_value = self.oai_harvester_metadata_format

        # Act
        result = harvester_set_api.upsert(self.oai_harvester_metadata_format)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)
        self.assertEquals(result.raw, {})

    @patch(
        'core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.save')
    def test_upsert_oai_harvester_set_does_not_throw_exception_if_invalid_raw(self, mock_create):
        # Arrange
        self.oai_harvester_metadata_format.raw = '<root?</root>'

        mock_create.return_value = self.oai_harvester_metadata_format

        # Act
        result = harvester_set_api.upsert(self.oai_harvester_metadata_format)

        # Act + Assert
        self.assertIsInstance(result, OaiHarvesterSet)
        self.assertEquals(result.raw, {})

    @patch(
        'core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.save')
    def test_upsert_oai_harvester_set_no_exception_if_raw_not_string(self, mock_create):
        # Arrange
        self.oai_harvester_metadata_format.raw = OrderedDict([(u'test', u'Hello')])

        mock_create.return_value = self.oai_harvester_metadata_format

        # Act
        result = harvester_set_api.upsert(self.oai_harvester_metadata_format)

        # Assert
        self.assertIsInstance(result, OaiHarvesterSet)


class TestOaiHarvesterSetDeleteAllByRegistry(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.delete_all_by_registry')
    def test_delete_all_by_registry_throws_exception_if_object_does_not_exist(self, mock_delete_all):
        # Arrange
        mock_absent_registry = str(ObjectId())

        mock_delete_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            harvester_set_api.delete_all_by_registry(mock_absent_registry)


class TestOaiHarvesterSetDelete(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.'
           'delete')
    def test_delete_oai_harvester_seet_throws_exception_if_object_does_not_exist(self, mock_delete):
        # Arrange
        oai_harvester_set = _create_oai_harvester_set()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            harvester_set_api.delete(oai_harvester_set)


class TestOaiHarvesterSetUpdateForAllByRegistry(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.'
           'update_for_all_harvest_by_registry')
    def test_update_for_all_harvest_by_registry_throws_exception_if_object_does_not_exist(self, mock_update_all):
        # Arrange
        mock_absent_registry = str(ObjectId())

        mock_update_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            harvester_set_api.update_for_all_harvest_by_registry(registry=mock_absent_registry, harvest=True)


class TestOaiSetUpdateForAllByListIds(TestCase):
    @patch('core_oaipmh_harvester_app.components.oai_harvester_set.models.OaiHarvesterSet.'
           'update_for_all_harvest_by_list_ids')
    def test_update_for_all_harvest_by_list_ids_throws_exception_if_object_does_not_exist(self, mock_update_all):
        # Arrange
        mock_absent_list_ids = [str(ObjectId()), str(ObjectId())]

        mock_update_all.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            harvester_set_api.update_for_all_harvest_by_list_ids(mock_absent_list_ids, True)


def _create_oai_harvester_set():
    """
    Get an OaiHarvestSet object
    :return:
    """
    oai_harvester_set = OaiHarvesterSet()
    _set_oai_harvester_set_fields(oai_harvester_set)

    return oai_harvester_set


def _create_mock_oai_harvester_set():
    """
    Mock an OaiHarvestSet object
    :return:
    """
    mock_oai_harvester_set = Mock(spec=OaiHarvesterSet)
    _set_oai_harvester_set_fields(mock_oai_harvester_set)

    return mock_oai_harvester_set


def _set_oai_harvester_set_fields(oai_harvester_set):
    """
    Set OaiHarvestSet fields
    :return:
    """
    oai_harvester_set.setSpec = "oai_test"
    oai_harvester_set.setName = "test"
    oai_harvester_set.raw = '<set xmlns="http://www.openarchives.org/OAI/2.0/" ' \
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
    oai_harvester_set.registry = str(ObjectId())
    oai_harvester_set.harvest = True

    return oai_harvester_set
