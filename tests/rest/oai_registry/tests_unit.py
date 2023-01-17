""" Unit Test Rest OaiRegistry
"""
from rest_framework import status
from unittest.case import TestCase
from unittest.mock import patch, Mock

from core_main_app.commons import exceptions
from core_main_app.utils.datetime import datetime_now
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import (
    api as oai_harvester_metadata_format_api,
)
from core_oaipmh_harvester_app.components.oai_harvester_set import (
    api as oai_harvester_set_api,
)
from core_oaipmh_harvester_app.components.oai_registry import (
    api as oai_registry_api,
)
from core_oaipmh_harvester_app.components.oai_registry.models import (
    OaiRegistry,
)
from core_oaipmh_harvester_app.rest.oai_registry import (
    views as rest_oai_registry,
)


class TestSelectRegistry(TestCase):
    """Test Select Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {}
        self.param = {"registry_id": 1}

    def test_select_registry_unauthorized(self):
        """test_select_registry_unauthorized"""

        # Arrange
        user = create_mock_user("1", has_perm=False)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryDetail.as_view(),
            user,
            self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiRegistry, "get_by_id")
    def test_select_registry_not_found(self, mock_get_by_name):
        """test_select_registry_not_found"""

        # Arrange
        mock_get_by_name.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryDetail.as_view(),
            user=create_mock_user("1", is_staff=True, has_perm=True),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSelectAllRegistries(TestCase):
    """Test Select All Registries"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_select_registry_unauthorized(self):
        """test_select_registry_unauthorized"""

        # Arrange
        user = create_mock_user("1", has_perm=False)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAddRegistry(TestCase):
    """TestAddRegistry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {
            "url": "http://url.com",
            "harvest_rate": 3000,
            "harvest": True,
        }
        self.bad_data = {}

    def test_add_registry_unauthorized(self):
        """test_add_registry_unauthorized"""

        # Arrange
        user = create_mock_user("1", is_staff=False)

        # Act
        response = RequestMock.do_request_post(
            rest_oai_registry.RegistryList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_registry_serializer_invalid(self):
        """test_add_registry_serializer_invalid"""

        # Act
        response = RequestMock.do_request_post(
            rest_oai_registry.RegistryList.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.bad_data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(OaiRegistry, "check_registry_url_already_exists")
    def test_add_registry_raises_exception_if_url_already_exists(
        self, mock_check
    ):
        """test_add_registry_raises_exception_if_url_already_exists"""

        # Arrange
        mock_check.return_value = True

        # Act
        response = RequestMock.do_request_post(
            rest_oai_registry.RegistryList.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class TestUpdateRegistryInfo(TestCase):
    """Test Update Registry Info"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {}
        self.param = {"registry_id": 1}

    def test_update_registry_info_unauthorized(self):
        """test_update_registry_info_unauthorized"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.InfoRegistry.as_view(),
            user=create_mock_user("1", is_staff=False),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiRegistry, "get_by_id")
    def test_update_registry_info_not_found(self, mock_get_by_id):
        """test_update_registry_info_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.InfoRegistry.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUpdateRegistryConf(TestCase):
    """Test Update Registry Conf"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {"harvest_rate": 4000, "harvest": False}
        self.bad_data = {"harvest": False}
        self.param = {"registry_id": 1}

    def test_update_registry_info_unauthorized(self):
        """test_update_registry_info_unauthorized"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.RegistryDetail.as_view(),
            user=create_mock_user("1", is_staff=False),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiRegistry, "get_by_id")
    def test_update_registry_info_serializer_invalid(self, mock_get_by_id):
        """test_update_registry_info_serializer_invalid"""

        # Arrange
        mock_registry = _create_mock_oai_registry()
        mock_get_by_id.return_value = mock_registry
        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.RegistryDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.bad_data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(OaiRegistry, "get_by_id")
    def test_update_registry_info_not_found(self, mock_get_by_id):
        """test_update_registry_info_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.RegistryDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeactivateRegistry(TestCase):
    """Test Deactivate Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {}
        self.param = {"registry_id": 1}

    def test_deactivate_registry_unauthorized(self):
        """test_deactivate_registry_unauthorized"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.DeactivateRegistry.as_view(),
            user=create_mock_user("1", is_staff=False),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiRegistry, "get_by_id")
    def test_deactivate_registry_not_found(self, mock_get_by_id):
        """test_deactivate_registry_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.DeactivateRegistry.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestActivateRegistry(TestCase):
    """Test Activate Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {}
        self.param = {"registry_id": 1}

    def test_activate_registry_unauthorized(self):
        """test_activate_registry_unauthorized"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.ActivateRegistry.as_view(),
            user=create_mock_user("1", is_staff=False),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiRegistry, "get_by_id")
    def test_activate_registry_not_found(self, mock_get_by_id):
        """test_activate_registry_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.ActivateRegistry.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeleteRegistry(TestCase):
    """Test Delete Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {}
        self.param = {"registry_id": 1}

    def test_delete_registry_unauthorized(self):
        """test_delete_registry_unauthorized"""

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_registry.RegistryDetail.as_view(),
            user=create_mock_user("1", is_staff=False),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiRegistry, "get_by_id")
    def test_delete_registry_not_found(self, mock_get_by_id):
        """test_delete_registry_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_registry.RegistryDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestHarvestRegistry(TestCase):
    """Test Harvest Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"registry_id": 1}

    @patch.object(OaiRegistry, "get_by_id")
    @patch.object(oai_registry_api, "_harvest_by_metadata_formats")
    @patch.object(oai_harvester_set_api, "get_all_to_harvest_by_registry_id")
    @patch.object(oai_harvester_set_api, "get_all_by_registry_id")
    @patch.object(
        oai_harvester_metadata_format_api, "get_all_to_harvest_by_registry_id"
    )
    def test_harvest_registry(
        self,
        mock_metadata_formats,
        mock_sets_all,
        mock_sets_to_harvest,
        mock_harvest_by_metadata_formats,
        mock_get_by_id,
    ):
        """test_harvest_registry"""

        # Arrange
        mock_registry = _create_mock_oai_registry()
        mock_get_by_id.return_value = mock_registry
        mock_metadata_formats.return_value = []
        mock_sets_all.return_value = [object(), object()]
        # Harvest all sets.
        mock_sets_to_harvest.return_value = mock_sets_all.return_value
        mock_harvest_by_metadata_formats.return_value = []

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.Harvest.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_harvest_registry_unauthorized(self):
        """test_harvest_registry_unauthorized"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.Harvest.as_view(),
            user=create_mock_user("1", is_staff=False),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiRegistry, "get_by_id")
    def test_harvest_registry_not_found(self, mock_get_by_id):
        """test_harvest_registry_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.Harvest.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


def _create_mock_oai_registry():
    """Mock an OaiRegistry.

    Returns:
        OaiRegistry mock.

    """
    mock_oai_registry = Mock(spec=OaiRegistry)
    _set_oai_registry_fields(mock_oai_registry)

    return mock_oai_registry


def _set_oai_registry_fields(oai_registry):
    """Set OaiRegistry fields.

    Args:
        oai_registry:

    Returns:
        OaiRegistry with assigned fields.

    """
    oai_registry.name = "Registry"
    oai_registry.url = "http://url.com"
    oai_registry.harvest_rate = 3000
    oai_registry.description = "This is the registry"
    oai_registry.harvest = True
    oai_registry.last_update = datetime_now()
    oai_registry.is_harvesting = False
    oai_registry.is_updating = False
    oai_registry.is_activated = True
    oai_registry.is_queued = True

    return oai_registry
