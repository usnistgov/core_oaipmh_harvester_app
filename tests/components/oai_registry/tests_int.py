""" Int Test OaiRegistry
"""

from unittest.mock import patch

import requests
from rest_framework import status

from core_main_app.commons import exceptions
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_oaipmh_common_app.commons import exceptions as oai_pmh_exceptions
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import (
    api as oai_harvester_metadata_format_api,
)
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format_set import (
    api as oai_harvester_metadata_format_set_api,
)
from core_oaipmh_harvester_app.components.oai_harvester_set import (
    api as oai_harvester_set_api,
)
from core_oaipmh_harvester_app.components.oai_identify import api as oai_identify_api
from core_oaipmh_harvester_app.components.oai_record import api as oai_record_api
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_registry import api as oai_registry_api
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.components.oai_verbs import api as oai_verbs_api
from core_oaipmh_harvester_app.system import api as oai_harvester_system_api
from tests.components.oai_registry.fixtures.fixtures import OaiPmhFixtures
from tests.components.oai_registry.fixtures.fixtures import OaiPmhMock

fixture_data = OaiPmhFixtures()


class TestAddRegistry(MongoIntegrationBaseTestCase):
    """
    Test Add Registry
    """

    fixture = fixture_data

    @patch.object(requests, "get")
    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    @patch.object(oai_verbs_api, "identify_as_object")
    def test_add_registry(
        self, mock_identify, mock_metadata_formats, mock_sets, mock_get
    ):
        """Test add registry
        Args:
            mock_identify:
            mock_metadata_formats:
            mock_sets:
            mock_get:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        mock_metadata_formats.return_value = (
            OaiPmhMock.mock_oai_metadata_format(),
            status.HTTP_200_OK,
        )
        mock_sets.return_value = OaiPmhMock.mock_oai_set(), status.HTTP_200_OK
        text = "<test>Hello</test>"
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(
            self.fixture.url,
            self.fixture.harvest_rate,
            self.fixture.harvest,
            request=mock_request,
        )

        # Assert
        self.assertIsInstance(result, OaiRegistry)


class TestAddRegistryNotAvailable(MongoIntegrationBaseTestCase):
    """
    Test Add Registry Not Available
    """

    fixture = fixture_data

    @patch.object(oai_verbs_api, "identify_as_object")
    def test_add_registry_not_available(self, mock_identify):
        """Test add registry not available
        Args:
            mock_identify:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_identify.return_value = (
            {
                "message": "An error occurred when attempting to identify "
                "resource: "
                "404 Client Error: NOT FOUND"
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPILabelledException):
            oai_registry_api.add_registry_by_url(
                self.fixture.url,
                self.fixture.harvest_rate,
                self.fixture.harvest,
                request=mock_request,
            )


class TestAddRegistryNoSetsNoMetadataFormats(MongoIntegrationBaseTestCase):
    """
    Test Add Registry No Sets No Metadata Formats
    """

    fixture = fixture_data

    @patch.object(requests, "get")
    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    @patch.object(oai_verbs_api, "identify_as_object")
    def test_add_registry_no_sets_no_metadata_formats(
        self, mock_identify, mock_metadata_formats, mock_sets, mock_get
    ):
        """Test add registry with no sets and no metadata formats
        Args:
            mock_identify:
            mock_metadata_formats:
            mock_sets:
            mock_get:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        mock_metadata_formats.return_value = [], status.HTTP_200_OK
        mock_sets.return_value = [], status.HTTP_200_OK
        text = "<test>Hello</test>"
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(
            self.fixture.url,
            self.fixture.harvest_rate,
            self.fixture.harvest,
            request=mock_request,
        )

        # Assert
        self.assertIsInstance(result, OaiRegistry)


class TestAddRegistryIdentify(MongoIntegrationBaseTestCase):
    """
    Test Add Registry Identify
    """

    fixture = fixture_data

    @patch.object(requests, "get")
    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    @patch.object(oai_verbs_api, "identify_as_object")
    def test_add_registry_identify(
        self, mock_identify, mock_metadata_formats, mock_sets, mock_get
    ):
        """Test add registry identify
        Args:
            mock_identify:
            mock_metadata_formats:
            mock_sets:
            mock_get:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        identify = OaiPmhMock.mock_oai_identify()
        mock_identify.return_value = identify, status.HTTP_200_OK
        mock_metadata_formats.return_value = [], status.HTTP_200_OK
        mock_sets.return_value = [], status.HTTP_200_OK
        text = "<test>Hello</test>"
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(
            self.fixture.url,
            self.fixture.harvest_rate,
            self.fixture.harvest,
            request=mock_request,
        )

        # Assert
        _assert_identify(self, identify, result.id)


class TestAddRegistrySets(MongoIntegrationBaseTestCase):
    """
    Test Add Registry Sets
    """

    fixture = fixture_data

    @patch.object(requests, "get")
    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    @patch.object(oai_verbs_api, "identify_as_object")
    def test_add_registry_sets(
        self, mock_identify, mock_metadata_formats, mock_sets, mock_get
    ):
        """Test add registry sets
        Args:
            mock_identify:
            mock_metadata_formats:
            mock_sets:
            mock_get:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        mock_metadata_formats.return_value = [], status.HTTP_200_OK
        list_sets = OaiPmhMock.mock_oai_set()
        mock_sets.return_value = list_sets, status.HTTP_200_OK
        text = "<test>Hello</test>"
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(
            self.fixture.url,
            self.fixture.harvest_rate,
            self.fixture.harvest,
            request=mock_request,
        )

        # Assert
        _assert_set(self, list_sets, result.id)


class TestAddRegistryMetadataFormats(MongoIntegrationBaseTestCase):
    """
    Test Add Registry Metadata Formats
    """

    fixture = fixture_data

    @patch.object(requests, "get")
    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    @patch.object(oai_verbs_api, "identify_as_object")
    def test_add_registry_metadata_format(
        self, mock_identify, mock_metadata_formats, mock_sets, mock_get
    ):
        """Test add registry metadata formats
        Args:
            mock_identify:
            mock_metadata_formats:
            mock_sets:
            mock_get:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_identify.return_value = OaiPmhMock.mock_oai_identify(), status.HTTP_200_OK
        list_metadata_formats = OaiPmhMock.mock_oai_metadata_format()
        mock_metadata_formats.return_value = list_metadata_formats, status.HTTP_200_OK
        mock_sets.return_value = [], status.HTTP_200_OK
        text = "<test>Hello</test>"
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.add_registry_by_url(
            self.fixture.url,
            self.fixture.harvest_rate,
            self.fixture.harvest,
            request=mock_request,
        )

        # Assert
        _assert_metadata_format(self, list_metadata_formats, result.id)


class TestAddRegistryConstraints(MongoIntegrationBaseTestCase):
    """
    Test Add Registry Constraints
    """

    fixture = fixture_data

    def setUp(self):
        """setUp"""

        super().setUp()
        self.fixture.insert_registry()

    def test_add_registry_raises_exception_if_url_already_exists(self):
        """Test add registry with existing URL"""
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act + Assert
        with self.assertRaises(oai_pmh_exceptions.OAIAPINotUniqueError):
            oai_registry_api.add_registry_by_url(
                self.fixture.url,
                self.fixture.harvest_rate,
                self.fixture.harvest,
                request=mock_request,
            )


class TestUpdateRegistryInfo(MongoIntegrationBaseTestCase):
    """
    Test Update Registry Info
    """

    fixture = fixture_data

    def setUp(self):
        """setUp"""

        super().setUp()
        self.fixture.insert_registry()

    @patch.object(requests, "get")
    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    @patch.object(oai_verbs_api, "identify_as_object")
    def test_update_registry(
        self, mock_identify, mock_metadata_formats, mock_sets, mock_get
    ):
        """test_update_registry"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        identify = OaiPmhMock.mock_oai_identify(version=2)
        mock_identify.return_value = identify, status.HTTP_200_OK
        first_metadata_format = OaiPmhMock.mock_oai_metadata_format(version=2)
        mock_metadata_formats.return_value = first_metadata_format, status.HTTP_200_OK
        first_set = OaiPmhMock.mock_oai_set(version=2)
        mock_sets.return_value = first_set, status.HTTP_200_OK
        text = "<test>Hello</test>"
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        result = oai_registry_api.update_registry_info(
            self.fixture.registry, request=mock_request
        )

        # Assert
        _assert_identify(self, identify, result.id)
        _assert_metadata_format(self, first_metadata_format, result.id)
        _assert_set(self, first_set, result.id)


class TestUpsertIdentifyForRegistry(MongoIntegrationBaseTestCase):
    """
    Test Upsert Identify For Registry
    """

    fixture = fixture_data

    def setUp(self):
        """Set up test"""

        super().setUp()

    def test_upsert_updates_if_does_exist(self):
        """Test upsert update"""
        self.fixture.insert_registry()

        # Arrange
        repository_name = "update_test"
        self.fixture.oai_identify.repository_name = repository_name
        # Act
        oai_registry_api._upsert_identify_for_registry(
            self.fixture.oai_identify, self.fixture.registry
        )

        # Assert
        identify_in_database = oai_identify_api.get_by_registry_id(
            self.fixture.registry.id
        )
        self.assertEquals(identify_in_database.repository_name, repository_name)

    def test_upsert_creates_if_does_not_exist(self):
        """Test upsert create"""
        # Arrange
        oai_identify = OaiPmhMock.mock_oai_identify()
        self.fixture.insert_registry(insert_related_collections=True)

        # Act
        oai_registry_api._upsert_identify_for_registry(
            oai_identify, self.fixture.registry
        )

        # Assert
        identify_in_database = oai_identify_api.get_by_registry_id(
            self.fixture.registry.id
        )
        self.assertEquals(identify_in_database, oai_identify)


class TestUpsertMetadataFormatForRegistry(MongoIntegrationBaseTestCase):
    """
    Test Upsert Metadata Format For Registry
    """

    fixture = fixture_data

    def setUp(self):
        super().setUp()

    @patch.object(requests, "get")
    def test_upsert_updates_if_does_exist(self, mock_get):
        """Test upsert update
        Args:
            mock_get:

        Returns:

        """
        self.fixture.insert_registry()

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        text = "<test>Hello</test>"
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text
        metadata_format = self.fixture.oai_metadata_formats[0]
        schema = "http://www.dummy-url.us"
        metadata_format.schema = schema

        # Act
        oai_registry_api._upsert_metadata_format_for_registry(
            metadata_format, self.fixture.registry, request=mock_request
        )

        # Assert
        metadata_format_in_database = (
            oai_harvester_metadata_format_api.get_by_metadata_prefix_and_registry_id(
                metadata_format.metadata_prefix, self.fixture.registry.id
            )
        )
        self.assertEquals(metadata_format_in_database.schema, schema)

    @patch.object(requests, "get")
    def test_upsert_creates_if_does_not_exist(self, mock_get):
        """Test upsert create
        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        text = "<test>Hello</test>"
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text
        oai_harvester_metadata_format = OaiPmhMock.mock_oai_first_metadata_format()
        self.fixture.insert_registry(insert_related_collections=False)

        # Act
        oai_registry_api._upsert_metadata_format_for_registry(
            oai_harvester_metadata_format, self.fixture.registry, request=mock_request
        )

        # Assert
        metadata_format_in_database = (
            oai_harvester_metadata_format_api.get_by_metadata_prefix_and_registry_id(
                oai_harvester_metadata_format.metadata_prefix, self.fixture.registry.id
            )
        )

        self.assertEquals(oai_harvester_metadata_format, metadata_format_in_database)


class TestUpsertSetForRegistry(MongoIntegrationBaseTestCase):
    """
    Test Upsert Set For Registry
    """

    fixture = fixture_data

    def setUp(self):
        """Set up test"""
        super().setUp()

    def test_upsert_updates_if_does_exist(self):
        """Test upsert update"""
        self.fixture.insert_registry()

        # Arrange
        oai_harvester_set = self.fixture.oai_sets[0]
        set_name = "name_test"
        oai_harvester_set.set_name = set_name

        # Act
        oai_registry_api._upsert_set_for_registry(
            oai_harvester_set, self.fixture.registry
        )

        # Assert
        set_in_database = oai_harvester_set_api.get_by_set_spec_and_registry_id(
            oai_harvester_set.set_spec, self.fixture.registry.id
        )
        self.assertEquals(set_in_database.set_name, set_name)

    def test_upsert_creates_if_does_not_exist(self):
        """Test upsert create"""
        # Arrange
        oai_harvester_set = OaiPmhMock.mock_oai_first_set()
        self.fixture.insert_registry(insert_related_collections=True)

        # Act
        oai_registry_api._upsert_identify_for_registry(
            oai_harvester_set, self.fixture.registry
        )

        # Assert
        set_in_database = oai_harvester_set_api.get_by_set_spec_and_registry_id(
            oai_harvester_set.set_spec, self.fixture.registry.id
        )

        self.assertEquals(oai_harvester_set, set_in_database)


class TestUpsertRecordForRegistry(MongoIntegrationBaseTestCase):
    """
    Test Upsert Record For Registry
    """

    fixture = fixture_data

    def setUp(self):
        """Set up test"""

        super().setUp()

    @patch.object(OaiRecord, "convert_to_file")
    def test_upsert_updates_if_does_exist(self, mock_convert_file):
        """Test upsert update"""
        self.fixture.insert_registry()

        # Arrange
        oai_record = OaiPmhMock.mock_oai_first_record(as_json=True)
        metadata_format = self.fixture.oai_metadata_formats[0]
        identifier = "fake_identifier"
        oai_record["identifier"] = identifier
        mock_convert_file.return_value = None

        # Act
        record_in_database = oai_registry_api._upsert_record_for_registry(
            oai_record, metadata_format, self.fixture.registry, []
        )

        # Assert
        self.assertEquals(record_in_database.identifier, identifier)
        self.assertEquals(record_in_database.harvester_metadata_format, metadata_format)

    @patch.object(OaiRecord, "convert_to_file")
    def test_upsert_creates_if_does_not_exist(self, mock_convert_file):
        """Test upsert create"""
        # Arrange
        oai_record = OaiPmhMock.mock_oai_first_record(as_json=True)
        self.fixture.insert_registry(insert_related_collections=False)
        metadata_format = OaiHarvesterMetadataFormat(
            raw={}, registry=self.fixture.registry
        )
        metadata_format.save()
        mock_convert_file.return_value = None

        # Act
        saved_record = oai_registry_api._upsert_record_for_registry(
            oai_record, metadata_format, self.fixture.registry, []
        )

        # Assert
        record_in_database = (
            oai_harvester_system_api.get_oai_record_by_identifier_and_metadata_format(
                oai_record["identifier"], metadata_format
            )
        )

        self.assertEquals(record_in_database, saved_record)


class TestHarvestByMetadataFormats(MongoIntegrationBaseTestCase):
    """
    Test Harvest By Metadata Formats
    """

    fixture = fixture_data

    def setUp(self):
        """Set up test"""

        super().setUp()
        self.fixture.insert_registry(insert_records=False)

    @patch.object(requests, "get")
    @patch.object(OaiRecord, "convert_to_file")
    def test_harvest_by_metadata_formats_saves_record(
        self, mock_convert_file, mock_get
    ):
        """Test harvest by metadata formats save
        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = OaiPmhMock.mock_oai_response_list_records(
            with_resumption_token=False
        )
        metadata_format = [self.fixture.oai_metadata_formats[0]]
        mock_convert_file.return_value = None

        # Act
        result = oai_registry_api._harvest_by_metadata_formats(
            self.fixture.registry, metadata_format, self.fixture.oai_sets
        )

        # Assert
        record_in_database = oai_record_api.get_all_by_registry_id(
            self.fixture.registry.id
        )
        self.assertEquals(result, [])
        self.assertTrue(len(record_in_database) > 0)

    @patch.object(requests, "get")
    @patch.object(OaiRecord, "convert_to_file")
    def test_harvest_by_metadata_formats_updates_dates(
        self, mock_convert_file, mock_get
    ):
        """Test harvest by metadata formats update
        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = OaiPmhMock.mock_oai_response_list_records(
            with_resumption_token=False
        )
        metadata_format = self.fixture.oai_metadata_formats[0]
        set_ = self.fixture.oai_sets[0]
        mock_convert_file.return_value = None

        # Assert
        # Metadata Format date
        self.assertEquals(metadata_format.last_update, None)
        # Metadata Format + Set date
        with self.assertRaises(exceptions.DoesNotExist):
            oai_harvester_metadata_format_set_api.get_by_metadata_format_and_set(
                metadata_format, set_
            )

        # Act
        result = oai_registry_api._harvest_by_metadata_formats(
            self.fixture.registry, [metadata_format], self.fixture.oai_sets
        )

        # Assert
        self.assertEquals(result, [])
        # Metadata Format date
        metadata_format_in_database = oai_harvester_metadata_format_api.get_by_id(
            metadata_format.id
        )
        self.assertNotEquals(metadata_format_in_database.last_update, None)
        # Metadata Format + Set date
        oai_h_mf_set = (
            oai_harvester_metadata_format_set_api.get_by_metadata_format_and_set(
                metadata_format, set_
            )
        )
        self.assertNotEquals(oai_h_mf_set.last_update, None)


class TestHarvestByMetadataFormatsAndSets(MongoIntegrationBaseTestCase):
    """
    Test Harvest By Metadata Formats And Sets
    """

    fixture = fixture_data

    def setUp(self):
        """Set up test"""
        super().setUp()
        self.fixture.insert_registry(insert_records=False)

    @patch.object(requests, "get")
    @patch.object(OaiRecord, "convert_to_file")
    def test_harvest_by_metadata_formats_and_sets_saves_record(
        self, mock_convert_file, mock_get
    ):
        """Test harvest by metadata formats and sets save
        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = OaiPmhMock.mock_oai_response_list_records(
            with_resumption_token=False
        )
        metadata_format = [self.fixture.oai_metadata_formats[0]]
        set_ = [self.fixture.oai_sets[0]]
        mock_convert_file.return_value = None

        # Act
        result = oai_registry_api._harvest_by_metadata_formats_and_sets(
            self.fixture.registry, metadata_format, set_, self.fixture.oai_sets
        )

        # Assert
        record_in_database = oai_record_api.get_all_by_registry_id(
            self.fixture.registry.id
        )
        self.assertEquals(result, [])
        self.assertTrue(len(record_in_database) > 0)

    @patch.object(requests, "get")
    @patch.object(OaiRecord, "convert_to_file")
    def test_harvest_by_metadata_formats_and_sets_updates_dates(
        self, mock_convert_file, mock_get
    ):
        """Test harvest by metadata formats and sets update
        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = OaiPmhMock.mock_oai_response_list_records(
            with_resumption_token=False
        )
        metadata_format = self.fixture.oai_metadata_formats[0]
        set_ = self.fixture.oai_sets[0]
        mock_convert_file.return_value = None

        # Assert
        # Metadata Format date
        self.assertEquals(metadata_format.last_update, None)
        # Metadata Format + Set date
        with self.assertRaises(exceptions.DoesNotExist):
            oai_harvester_metadata_format_set_api.get_by_metadata_format_and_set(
                metadata_format, set_
            )

        # Act
        result = oai_registry_api._harvest_by_metadata_formats_and_sets(
            self.fixture.registry, [metadata_format], [set_], self.fixture.oai_sets
        )

        # Assert
        self.assertEquals(result, [])
        # Metadata Format date
        metadata_format_in_database = oai_harvester_metadata_format_api.get_by_id(
            metadata_format.id
        )
        self.assertIsNotNone(metadata_format_in_database.last_update)
        # Metadata Format + Set date
        oai_h_mf_set = (
            oai_harvester_metadata_format_set_api.get_by_metadata_format_and_set(
                metadata_format, set_
            )
        )
        self.assertIsNotNone(oai_h_mf_set.last_update)


class TestHarvestRegistry(MongoIntegrationBaseTestCase):
    """
    Test class
    """

    fixture = fixture_data

    def setUp(self):
        """Set up test"""
        super().setUp()
        self.fixture.insert_registry(insert_records=False)

    @patch.object(requests, "get")
    @patch.object(OaiRecord, "convert_to_file")
    def test_harvest_registry_saves_record(self, mock_convert_file, mock_get):
        """Test harvest save
        Args:
            mock_get:
            mock_convert_file:

        Returns:

        """
        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = OaiPmhMock.mock_oai_response_list_records(
            with_resumption_token=False
        )
        mock_convert_file.return_value = None

        # Act
        result = oai_registry_api.harvest_registry(self.fixture.registry)

        # Assert
        record_in_database = oai_record_api.get_all_by_registry_id(
            self.fixture.registry.id
        )
        self.assertEquals(result, [])
        self.assertTrue(len(record_in_database) > 0)

    @patch.object(requests, "get")
    @patch.object(OaiRecord, "convert_to_file")
    def test_harvest_registry_updates_dates(self, mock_convert_file, mock_get):
        """Test harvest update
        Args:
            mock_get:
            mock_convert_file:

        Returns:

        """
        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = OaiPmhMock.mock_oai_response_list_records(
            with_resumption_token=False
        )
        mock_convert_file.return_value = None

        # Assert
        # Registry date
        self.assertEquals(self.fixture.registry.last_update, None)

        # Act
        result = oai_registry_api.harvest_registry(self.fixture.registry)

        # Assert
        self.assertEquals(result, [])
        # Registry date
        self.assertNotEquals(self.fixture.registry.last_update, None)


class TestHandleDeleteSet(MongoIntegrationBaseTestCase):
    """
    Test Handle Delete Set
    """

    fixture = fixture_data

    def setUp(self):
        """Set up test"""
        super().setUp()
        self.fixture.insert_registry(insert_records=False)

    def test_handle_deleted_set_deletes_set(self):
        """Test"""
        # Arrange
        index = 2
        removed_sets = self.fixture.oai_sets[:index]
        sets_response = self.fixture.oai_sets[index:]
        sets_count = len(self.fixture.oai_sets)

        # Act
        oai_registry_api._handle_deleted_set(self.fixture.registry.id, sets_response)

        # Assert
        record_in_database = oai_harvester_set_api.get_all_by_registry_id(
            self.fixture.registry.id
        )
        self.assertTrue(len(record_in_database) == (sets_count - index))
        self.assertTrue(
            x.set_spec not in [y.set_spec for y in record_in_database]
            for x in removed_sets
        )


class TestHandleDeleteMetadataFormat(MongoIntegrationBaseTestCase):
    """
    Test Handle Delete Metadata Format
    """

    fixture = fixture_data

    def setUp(self):
        """Set up test"""
        super().setUp()
        self.fixture.insert_registry(insert_records=False)

    def test_handle_deleted_metadata_format_deletes_metadata_format(self):
        """Test handle deleted metadata format
        Returns:

        """
        # Arrange
        index = 2
        removed_metadata_formats = self.fixture.oai_metadata_formats[:index]
        metadata_formats_response = self.fixture.oai_metadata_formats[index:]
        metadata_formats_count = len(self.fixture.oai_metadata_formats)

        # Act
        oai_registry_api._handle_deleted_metadata_format(
            self.fixture.registry.id, metadata_formats_response
        )

        # Assert
        record_in_database = oai_harvester_metadata_format_api.get_all_by_registry_id(
            self.fixture.registry.id
        )
        self.assertTrue(len(record_in_database) == (metadata_formats_count - index))
        self.assertTrue(
            x.metadata_prefix not in [y.metadata_prefix for y in record_in_database]
            for x in removed_metadata_formats
        )


def _assert_identify(self, mock, registry_id):
    """Assert identify
    Args:
        self:
        mock:
        registry_id:

    Returns:

    """
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
    """Assert set
    Args:
        self:
        mock:
        registry_id:

    Returns:

    """
    sets = oai_harvester_set_api.get_all_by_registry_id(registry_id)
    for set_ in sets:
        obj_in_database = next((x for x in mock if x.set_spec == set_.set_spec), [None])
        if obj_in_database != [None]:
            self.assertEquals(set_.set_spec, obj_in_database.set_spec)
            self.assertEquals(set_.set_name, obj_in_database.set_name)
            self.assertEquals(set_.raw, obj_in_database.raw)


def _assert_metadata_format(self, mock, registry_id):
    """Assert metadata format
    Args:
        self:
        mock:
        registry_id:

    Returns:

    """
    metadata_formats = oai_harvester_metadata_format_api.get_all_by_registry_id(
        registry_id
    )
    for metadata_format in metadata_formats:
        obj_in_database = next(
            (x for x in mock if x.metadata_prefix == metadata_format.metadata_prefix),
            [None],
        )
        if obj_in_database != [None]:
            self.assertEquals(
                metadata_format.metadata_prefix, obj_in_database.metadata_prefix
            )
            self.assertEquals(metadata_format.schema, obj_in_database.schema)
            self.assertEquals(
                metadata_format.metadata_namespace, obj_in_database.metadata_namespace
            )
            self.assertEquals(metadata_format.raw, obj_in_database.raw)
