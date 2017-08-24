""" Int Test Rest OaiRegistry
"""
from mock.mock import patch, Mock
from core_main_app.utils.integration_tests.integration_base_test_case import MongoIntegrationBaseTestCase
from tests.components.oai_registry.fixtures.fixtures import OaiPmhFixtures, OaiPmhMock
from core_oaipmh_harvester_app.components.oai_verbs import api as oai_verbs_api
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_harvester_app.rest.oai_registry import views as rest_oai_registry
from rest_framework import status
from bson import ObjectId
from django.contrib.auth.models import User
from unittest import skip
import requests


class TestSelectRegistry(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestSelectRegistry, self).setUp()
        self.data = {"registry_name": self.fixture.name}
        self.bad_data = {}

    def test_select_registry_returns(self):
        # Arrange
        self.fixture.insert_registry()
        user = _create_mock_user(has_perm=True)

        # Act
        response = RequestMock.do_request_get(rest_oai_registry.select_registry, user=user, data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSelectAllRegistries(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestSelectAllRegistries, self).setUp()
        self.data = None

    def test_select_all_registries(self):
        # Arrange
        self.fixture.insert_registry()
        user = _create_mock_user(has_perm=True)

        # Act
        response = RequestMock.do_request_get(rest_oai_registry.select_all_registries, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUpdateRegistryInfo(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestUpdateRegistryInfo, self).setUp()
        self.data = {}
        self.bad_data = {}
        self.bad_registry = {"registry_id": ObjectId()}

    @patch.object(requests, 'get')
    @patch.object(oai_verbs_api, 'list_sets_as_object')
    @patch.object(oai_verbs_api, 'list_metadata_formats_as_object')
    @patch.object(oai_verbs_api, 'identify_as_object')
    def test_update_registry_info(self, mock_identify, mock_metadata_formats, mock_sets, mock_get):
        # Arrange
        self.fixture.insert_registry()
        self.data = {"registry_id": self.fixture.registry.id}
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
        response = RequestMock.do_request_post(rest_oai_registry.update_registry_info,
                                               user=_create_mock_user(is_staff=True),
                                               data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUpdateRegistryConf(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestUpdateRegistryConf, self).setUp()
        self.data = {"harvest_rate": self.fixture.harvest_rate, "harvest": self.fixture.harvest}
        self.bad_registry = {"registry_id": str(ObjectId()), "harvest_rate": self.fixture.harvest_rate,
                             "harvest": self.fixture.harvest}
        self.bad_data = {}

    def test_update_registry_info(self):
        # Arrange
        self.fixture.insert_registry()
        self.data.update({"registry_id": str(self.fixture.registry.id)})

        # Act
        response = RequestMock.do_request_put(rest_oai_registry.update_registry_conf,
                                              user=_create_mock_user(is_staff=True),
                                              data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestActivateRegistry(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestActivateRegistry, self).setUp()
        self.data = {}
        self.bad_data = {}
        self.bad_registry = {"registry_id": str(ObjectId())}

    def test_activate_registry(self):
        # Arrange
        self.fixture.insert_registry()
        self.data = {"registry_id": str(self.fixture.registry.id)}

        # Act
        response = RequestMock.do_request_post(rest_oai_registry.activate_registry,
                                               user=_create_mock_user(is_staff=True),
                                               data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDeactivateRegistry(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestDeactivateRegistry, self).setUp()
        self.data = {}
        self.bad_data = {}
        self.bad_registry = {"registry_id": str(ObjectId())}

    def test_deactivate_registry(self):
        # Arrange
        self.fixture.insert_registry()
        self.data = {"registry_id": str(self.fixture.registry.id)}

        # Act
        response = RequestMock.do_request_post(rest_oai_registry.deactivate_registry,
                                               user=_create_mock_user(is_staff=True),
                                               data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@skip("TODO: Fix this test")
class TestDeleteRegistry(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestDeleteRegistry, self).setUp()
        self.data = {}
        self.bad_data = {}
        self.bad_registry = {"registry_id": str(ObjectId())}

    def test_delete_registry(self):
        # Arrange
        self.fixture.insert_registry()
        self.data = {"registry_id": str(self.fixture.registry.id)}

        # Act
        response = RequestMock.do_request_post(rest_oai_registry.delete_registry,
                                               user=_create_mock_user(is_staff=True),
                                               data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


def _create_mock_user(is_staff=False, has_perm=False, is_anonymous=False):
    """ Mock an User.

        Returns:
            User mock.

    """
    mock_user = Mock(spec=User)
    mock_user.is_staff = is_staff
    if is_staff:
        mock_user.has_perm.return_value = True
        mock_user.is_anonymous.return_value = False
    else:
        mock_user.has_perm.return_value = has_perm
        mock_user.is_anonymous.return_value = is_anonymous

    return mock_user
