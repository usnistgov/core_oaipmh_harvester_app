""" Int Test Rest OaiRegistry
"""

import requests
from rest_framework import status
from unittest.mock import patch

from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_harvester_app.components.oai_verbs import api as oai_verbs_api
from core_oaipmh_harvester_app.rest.oai_registry import (
    views as rest_oai_registry,
)
from tests.components.oai_registry.fixtures.fixtures import (
    OaiPmhFixtures,
    OaiPmhMock,
)


class TestSelectRegistry(IntegrationBaseTestCase):
    """Test Select Registry"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.fixture.insert_registry()
        self.param = {"registry_id": self.fixture.registry.id}

    def test_select_registry_returns(self):
        """test_select_registry_returns"""

        # Arrange
        user = create_mock_user("1", has_perm=True, is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryDetail.as_view(),
            user=user,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSelectAllRegistries(IntegrationBaseTestCase):
    """Test Select All Registries"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_select_all_registries(self):
        """test_select_all_registries"""

        # Arrange
        self.fixture.insert_registry()
        user = create_mock_user("1", has_perm=True, is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUpdateRegistryInfo(IntegrationBaseTestCase):
    """Test Update Registry Info"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.fixture.insert_registry()
        self.param = {"registry_id": self.fixture.registry.id}

    @patch.object(requests, "get")
    @patch.object(oai_verbs_api, "list_sets_as_object")
    @patch.object(oai_verbs_api, "list_metadata_formats_as_object")
    @patch.object(oai_verbs_api, "identify_as_object")
    def test_update_registry_info(
        self, mock_identify, mock_metadata_formats, mock_sets, mock_get
    ):
        """test_update_registry_info"""

        # Arrange
        identify = OaiPmhMock.mock_oai_identify(version=2)
        mock_identify.return_value = identify, status.HTTP_200_OK
        first_metadata_format = OaiPmhMock.mock_oai_metadata_format(version=2)
        mock_metadata_formats.return_value = (
            first_metadata_format,
            status.HTTP_200_OK,
        )
        first_set = OaiPmhMock.mock_oai_set(version=2)
        mock_sets.return_value = first_set, status.HTTP_200_OK
        text = "<test>Hello</test>"
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.InfoRegistry.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUpdateRegistryConf(IntegrationBaseTestCase):
    """Test Update Registry Conf"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.fixture.insert_registry()
        self.param = {"registry_id": str(self.fixture.registry.id)}
        self.data = {
            "harvest_rate": self.fixture.harvest_rate,
            "harvest": self.fixture.harvest,
        }

    def test_update_registry_info(self):
        """test_update_registry_info"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.RegistryDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestActivateRegistry(IntegrationBaseTestCase):
    """Test Activate Registry"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.fixture.insert_registry()
        self.param = {"registry_id": self.fixture.registry.id}

    def test_activate_registry(self):
        """test_activate_registry"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.ActivateRegistry.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDeactivateRegistry(IntegrationBaseTestCase):
    """Test Deactivate Registry"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.fixture.insert_registry()
        self.param = {"registry_id": str(self.fixture.registry.id)}

    def test_deactivate_registry(self):
        """test_deactivate_registry"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.DeactivateRegistry.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDeleteRegistry(IntegrationBaseTestCase):
    """Test Delete Registry"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.fixture.insert_registry()
        self.param = {"registry_id": str(self.fixture.registry.id)}

    def test_delete_registry(self):
        """test_delete_registry"""

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_registry.RegistryDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
