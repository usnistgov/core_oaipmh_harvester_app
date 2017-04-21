""" Int Test OaiRegistry
"""
from core_main_app.utils.integration_tests.integration_base_test_case import MongoIntegrationBaseTestCase
from mock.mock import patch
from rest_framework import status
from core_oaipmh_common_app.commons import exceptions as oai_pmh_exceptions
from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import OaiHarvesterMetadataFormat
from core_oaipmh_harvester_app.components.oai_registry import api as oai_registry_api
from core_oaipmh_harvester_app.components.oai_harvester_set import api as oai_harvester_set_api
from core_oaipmh_harvester_app.components.oai_identify import api as oai_identify_api
from core_oaipmh_harvester_app.components.oai_record import api as oai_record_api
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import api as oai_harvester_metadata_format_api
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify
from core_oaipmh_harvester_app.components.oai_verbs import api as oai_verbs_api
import requests
from core_oaipmh_harvester_app.components.oai_registry.tests.fixtures.fixtures import OaiPmhFixtures
from core_oaipmh_harvester_app.components.oai_registry.tests.fixtures.fixtures import OaiPmhMock
from bson.objectid import ObjectId

fixture_data = OaiPmhFixtures()


class TestAddRegistry(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    @patch.object(requests, 'get')
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    def test_add_registry(self, mock_identify, mock_metadata_formats, mock_sets, mock_get):
        # Arrange
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        mock_metadata_formats.return_value = OaiPmhMock.mock_oai_metadata_format(), status.HTTP_200_OK
        mock_sets.return_value = OaiPmhMock.mock_oai_set(), status.HTTP_200_OK
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(self.fixture.url, self.fixture.harvest_rate,
                                                      self.fixture.harvest)

        # Assert
        self.assertIsInstance(result, OaiRegistry)


class TestAddRegistryNotAvailable(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    @patch.object(oai_verbs_api, 'identify_as_object')
    def test_add_registry_not_available(self, mock_identify):
        # Arrange
        mock_identify.return_value = {'message': 'An error occurred when attempting to identify resource: '
                                                 '404 Client Error: NOT FOUND'}, \
                                     status.HTTP_500_INTERNAL_SERVER_ERROR

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException):
            oai_registry_api.add_registry_by_url(self.fixture.url, self.fixture.harvest_rate,
                                                 self.fixture.harvest)


class TestAddRegistryNoSetsNoMetadataFormats(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    @patch.object(requests, 'get')
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    def test_add_registry_no_sets_no_metadata_formats(self, mock_identify, mock_metadata_formats, mock_sets, mock_get):
        # Arrange
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        mock_metadata_formats.return_value = [], status.HTTP_200_OK
        mock_sets.return_value = [], status.HTTP_200_OK
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(self.fixture.url, self.fixture.harvest_rate,
                                                      self.fixture.harvest)

        # Assert
        self.assertIsInstance(result, OaiRegistry)


class TestAddRegistryIdentify(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    @patch.object(requests, 'get')
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    def test_add_registry_identify(self, mock_identify, mock_metadata_formats, mock_sets, mock_get):
        # Arrange
        identify = OaiPmhMock.mock_oai_identify()
        mock_identify.return_value = identify, status.HTTP_200_OK
        mock_metadata_formats.return_value = [], status.HTTP_200_OK
        mock_sets.return_value = [], status.HTTP_200_OK
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(self.fixture.url, self.fixture.harvest_rate,
                                                      self.fixture.harvest)

        # Assert
        _assert_identify(self, identify, result.id)


class TestAddRegistrySets(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    @patch.object(requests, 'get')
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    def test_add_registry_sets(self, mock_identify, mock_metadata_formats, mock_sets, mock_get):
        # Arrange
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        mock_metadata_formats.return_value = [], status.HTTP_200_OK
        list_sets = OaiPmhMock.mock_oai_set()
        mock_sets.return_value = list_sets, status.HTTP_200_OK
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(self.fixture.url, self.fixture.harvest_rate,
                                                      self.fixture.harvest)

        # Assert
        _assert_set(self, list_sets, result.id)


class TestAddRegistryMetadataFormats(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    @patch.object(requests, 'get')
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    def test_add_registry_metadata_format(self, mock_identify, mock_metadata_formats, mock_sets, mock_get):
        # Arrange
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        list_metadata_formats = OaiPmhMock.mock_oai_metadata_format()
        mock_metadata_formats.return_value = list_metadata_formats, status.HTTP_200_OK
        mock_sets.return_value = [], status.HTTP_200_OK
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(self.fixture.url, self.fixture.harvest_rate,
                                                      self.fixture.harvest)

        # Assert
        _assert_metadata_format(self, list_metadata_formats, result.id)


class TestAddRegistryConstraints(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestAddRegistryConstraints, self).setUp()
        self.fixture.insert_registry()

    def test_add_registry_raises_exception_if_url_already_exists(self):
        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPINotUniqueError):
            oai_registry_api.add_registry_by_url(self.fixture.url, self.fixture.harvest_rate,
                                                 self.fixture.harvest)


class TestUpdateRegistryInfo(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestUpdateRegistryInfo, self).setUp()
        self.fixture.insert_registry()

    @patch.object(requests, 'get')
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    def test_update_registry(self, mock_identify, mock_metadata_formats, mock_sets, mock_get):
        # Arrange
        identify = OaiPmhMock.mock_oai_identify(version=2)
        mock_identify.return_value = identify, status.HTTP_200_OK
        first_metadata_format = OaiPmhMock.mock_oai_metadata_format(version=2)
        mock_metadata_formats.return_value = first_metadata_format, status.HTTP_200_OK
        first_set = OaiPmhMock.mock_oai_set(version=2)
        mock_sets.return_value = first_set, status.HTTP_200_OK
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.update_registry_info(self.fixture.registry)

        # Assert
        _assert_identify(self, identify, result.id)
        _assert_metadata_format(self, first_metadata_format, result.id)
        _assert_set(self, first_set, result.id)


class TestUpsertIdentifyForRegistry(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestUpsertIdentifyForRegistry, self).setUp()

    def test_upsert_updates_if_does_exist(self):
        self.fixture.insert_registry()

        # Arrange
        repository_name = "update_test"
        self.fixture.oai_identify.repository_name = repository_name
        # Act
        oai_registry_api._upsert_identify_for_registry(self.fixture.oai_identify, self.fixture.registry)

        # Assert
        identify_in_database = oai_identify_api.get_by_registry_id(self.fixture.registry.id)
        self.assertEquals(identify_in_database.repository_name, repository_name)

    def test_upsert_creates_if_does_not_exist(self):
        # Arrange
        oai_identify = OaiPmhMock.mock_oai_identify()
        self.fixture.insert_registry(insert_related_collections=False)

        # Act
        oai_registry_api._upsert_identify_for_registry(oai_identify, self.fixture.registry)

        # Assert
        identify_in_database = oai_identify_api.get_by_registry_id(self.fixture.registry.id)
        self.assertEquals(identify_in_database, oai_identify)


class TestUpsertMetadataFormatForRegistry(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestUpsertMetadataFormatForRegistry, self).setUp()

    @patch.object(requests, 'get')
    def test_upsert_updates_if_does_exist(self, mock_get):
        self.fixture.insert_registry()

        # Arrange
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text
        metadata_format = self.fixture.oai_metadata_formats[0]
        schema = "http://www.dummy-url.us"
        metadata_format.schema = schema

        # Act
        oai_registry_api._upsert_metadata_format_for_registry(metadata_format, self.fixture.registry)

        # Assert
        metadata_format_in_database = oai_harvester_metadata_format_api.\
            get_by_metadata_prefix_and_registry_id(metadata_format.metadata_prefix, self.fixture.registry.id)
        self.assertEquals(metadata_format_in_database.schema, schema)

    @patch.object(requests, 'get')
    def test_upsert_creates_if_does_not_exist(self, mock_get):
        # Arrange
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text
        oai_harvester_metadata_format = OaiPmhMock.mock_oai_first_metadata_format()
        self.fixture.insert_registry(insert_related_collections=False)

        # Act
        oai_registry_api._upsert_metadata_format_for_registry(oai_harvester_metadata_format, self.fixture.registry)

        # Assert
        metadata_format_in_database = oai_harvester_metadata_format_api. \
            get_by_metadata_prefix_and_registry_id(oai_harvester_metadata_format.metadata_prefix,
                                                   self.fixture.registry.id)

        self.assertEquals(oai_harvester_metadata_format, metadata_format_in_database)


class TestUpsertSetForRegistry(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestUpsertSetForRegistry, self).setUp()

    def test_upsert_updates_if_does_exist(self):
        self.fixture.insert_registry()

        # Arrange
        oai_harvester_set = self.fixture.oai_sets[0]
        set_name = "name_test"
        oai_harvester_set.set_name = set_name

        # Act
        oai_registry_api._upsert_set_for_registry(oai_harvester_set, self.fixture.registry)

        # Assert
        set_in_database = oai_harvester_set_api.get_by_set_spec_and_registry_id(oai_harvester_set.set_spec,
                                                                                self.fixture.registry.id)
        self.assertEquals(set_in_database.set_name, set_name)

    def test_upsert_creates_if_does_not_exist(self):
        # Arrange
        oai_harvester_set = OaiPmhMock.mock_oai_first_set()
        self.fixture.insert_registry(insert_related_collections=False)

        # Act
        oai_registry_api._upsert_identify_for_registry(oai_harvester_set, self.fixture.registry)

        # Assert
        set_in_database = oai_harvester_set_api.get_by_set_spec_and_registry_id(oai_harvester_set.set_spec,
                                                                                self.fixture.registry.id)

        self.assertEquals(oai_harvester_set, set_in_database)


class TestUpsertRecordForRegistry(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestUpsertRecordForRegistry, self).setUp()

    def test_upsert_updates_if_does_exist(self):
        self.fixture.insert_registry()

        # Arrange
        oai_record = self.fixture.oai_records[0]
        metadata_format = self.fixture.oai_metadata_formats[0]
        identifier = "fake_identifier"
        oai_record.identifier = identifier

        # Act
        oai_registry_api._upsert_record_for_registry(oai_record, metadata_format, self.fixture.registry)

        # Assert
        record_in_database = oai_record_api.get_by_id(oai_record.id)
        self.assertEquals(record_in_database.identifier, identifier)
        self.assertEquals(record_in_database.harvester_metadata_format, metadata_format)

    def test_upsert_creates_if_does_not_exist(self):
        # Arrange
        oai_record = OaiPmhMock.mock_oai_first_record()
        metadata_format = OaiHarvesterMetadataFormat()
        metadata_format.id = ObjectId()
        self.fixture.insert_registry(insert_related_collections=False)

        # Act
        oai_registry_api._upsert_record_for_registry(oai_record, metadata_format, self.fixture.registry)

        # Assert
        record_in_database = oai_record_api.get_by_identifier_and_metadata_format(oai_record.identifier,
                                                                                  metadata_format)

        self.assertEquals(record_in_database, oai_record)


def _assert_identify(self, mock, registry_id):
    obj_in_database = oai_identify_api.get_by_registry_id(registry_id)
    self.assertEquals(mock.admin_email, obj_in_database.admin_email)
    self.assertEquals(mock.repository_name, obj_in_database.repository_name)
    self.assertEquals(mock.deleted_record, obj_in_database.deleted_record)
    self.assertEquals(mock.delimiter, obj_in_database.delimiter)
    self.assertEquals(mock.description, obj_in_database.description)
    self.assertEquals(mock.granularity, obj_in_database.granularity)
    self.assertEquals(mock.oai_identifier, obj_in_database.oai_identifier)
    self.assertEquals(mock.protocol_version, obj_in_database.protocol_version)
    self.assertEquals(mock.repository_identifier, obj_in_database.repository_identifier)
    self.assertEquals(mock.sample_identifier, obj_in_database.sample_identifier)
    self.assertEquals(mock.scheme, obj_in_database.scheme)
    self.assertEquals(mock.raw, obj_in_database.raw)


def _assert_set(self, mock, registry_id):
    sets = oai_harvester_set_api.get_all_by_registry_id(registry_id)
    for set_ in sets:
        obj_in_database = next((x for x in mock if x.set_spec == set_.set_spec), [None])
        if obj_in_database != [None]:
            self.assertEquals(set_.set_spec, obj_in_database.set_spec)
            self.assertEquals(set_.set_name, obj_in_database.set_name)
            self.assertEquals(set_.raw, obj_in_database.raw)


def _assert_metadata_format(self, mock, registry_id):
    metadata_formats = oai_harvester_metadata_format_api.get_all_by_registry_id(registry_id)
    for metadata_format in metadata_formats:
        obj_in_database = next((x for x in mock if x.metadata_prefix == metadata_format.metadata_prefix), [None])
        if obj_in_database != [None]:
            self.assertEquals(metadata_format.metadata_prefix, obj_in_database.metadata_prefix)
            self.assertEquals(metadata_format.schema, obj_in_database.schema)
            self.assertEquals(metadata_format.metadata_namespace, obj_in_database.metadata_namespace)
            self.assertEquals(metadata_format.raw, obj_in_database.raw)
