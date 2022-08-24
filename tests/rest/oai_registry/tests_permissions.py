""" Permissions Test for OAI Registry Rest API
"""
from unittest.mock import patch, Mock

from django.db.models.query import QuerySet
from django.test import SimpleTestCase
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import (
    api as oai_metadata_format_api,
)
from core_oaipmh_harvester_app.components.oai_harvester_set import api as oai_set_api
from core_oaipmh_harvester_app.components.oai_registry import api as oai_registry_api
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.rest.oai_registry import views as rest_oai_registry
from core_oaipmh_harvester_app.rest.serializers import (
    RegistrySerializer,
    UpdateRegistrySerializer,
    HarvestSerializer,
)


class TestGetRegistry(SimpleTestCase):
    """Test Get Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {}
        self.param = {"registry_id": 1}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryDetail.as_view(),
            None,
            self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryDetail.as_view(), user=user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(oai_registry_api, "get_by_id")
    @patch.object(RegistrySerializer, "data")
    def test_staff_returns_http_200(
        self, mock_oai_registry_api_get_by_id, mock_data_serializer_data
    ):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", has_perm=True, is_staff=True)
        mock_oai_registry_api_get_by_id.return_value = None
        mock_data_serializer_data.return_value = []

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryDetail.as_view(), user=user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDeleteRegistry(SimpleTestCase):
    """Test Delete Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {}
        self.param = {"registry_id": 1}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_registry.RegistryDetail.as_view(),
            None,
            self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_registry.RegistryDetail.as_view(), user=user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(oai_registry_api, "get_by_id")
    @patch.object(oai_registry_api, "delete")
    def test_staff_returns_http_204(
        self, mock_oai_registry_api_get_by_id, mock_oai_registry_api_delete
    ):
        """test_staff_returns_http_204"""

        # Arrange
        user = create_mock_user("1", has_perm=True, is_staff=True)
        mock_oai_registry_api_get_by_id.return_value = None
        mock_oai_registry_api_delete.return_value = None

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_registry.RegistryDetail.as_view(), user=user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestPatchRegistry(SimpleTestCase):
    """Test Patch Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"registry_id": 0}
        self.data = {"harvest_rate": 1, "harvest": False}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.RegistryDetail.as_view(),
            None,
            self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.RegistryDetail.as_view(), user=user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(oai_registry_api, "get_by_id")
    @patch.object(UpdateRegistrySerializer, "data")
    @patch.object(UpdateRegistrySerializer, "is_valid")
    @patch.object(UpdateRegistrySerializer, "save")
    @patch.object(OaiPmhMessage, "get_message_labelled")
    def test_staff_returns_http_200(
        self,
        mock_data_serializer_data,
        mock_data_serializer_is_valid,
        mock_data_serializer_save,
        mock_oaipmhmessage_get_message_labelled,
        mock_oai_registry_api_get_by_id,
    ):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", has_perm=True, is_staff=True)
        mock_oai_registry_api_get_by_id.return_value = Mock(spec=OaiRegistry)
        mock_data_serializer_data.return_value = []
        mock_data_serializer_is_valid.return_value = True
        mock_data_serializer_save.return_value = None
        mock_oaipmhmessage_get_message_labelled.return_value = None

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.RegistryDetail.as_view(), user=user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestInfoRegistry(SimpleTestCase):
    """Test Info Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"registry_id": 1}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.InfoRegistry.as_view(), user=None, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.InfoRegistry.as_view(),
            user=create_mock_user("1"),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(oai_registry_api, "get_by_id")
    @patch.object(oai_registry_api, "update_registry_info")
    @patch.object(OaiPmhMessage, "get_message_labelled")
    def test_staff_returns_http_200(
        self,
        mock_oaipmhmessage_get_message_labelled,
        mock_oai_registry_api_update_registry_info,
        mock_oai_registry_api_get_by_id,
    ):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        mock_oaipmhmessage_get_message_labelled.return_value = None
        mock_oai_registry_api_update_registry_info.return_value = Mock(spec=OaiRegistry)
        mock_oai_registry_api_get_by_id.return_value = Mock(spec=OaiRegistry)

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.InfoRegistry.as_view(), user=user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestHarvestRegistry(SimpleTestCase):
    """Test Harvest Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"registry_id": 1}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.Harvest.as_view(), user=None, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.Harvest.as_view(),
            user=create_mock_user("1"),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(oai_registry_api, "get_by_id")
    @patch.object(oai_registry_api, "harvest_registry")
    @patch.object(OaiPmhMessage, "get_message_labelled")
    def test_staff_returns_http_200(
        self,
        mock_oaipmhmessage_get_message_labelled,
        mock_oai_registry_api_harvest_registry,
        mock_oai_registry_api_get_by_id,
    ):
        """test_staff_returns_http_200"""

        # Arrange
        mock_oaipmhmessage_get_message_labelled.return_value = None
        mock_oai_registry_api_harvest_registry.return_value = []
        mock_oai_registry_api_get_by_id.return_value = Mock(spec=OaiRegistry)

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.Harvest.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestEditHarvestRegistry(SimpleTestCase):
    """Test Edit Harvest Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"registry_id": 0}
        self.data = {"metadata_formats": [], "sets": []}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        # Act
        response = RequestMock.do_request_put(
            rest_oai_registry.Harvest.as_view(), user=None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        # Act
        response = RequestMock.do_request_put(
            rest_oai_registry.Harvest.as_view(), user=create_mock_user("1")
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(QuerySet, "values_list")
    @patch.object(oai_set_api, "update_for_all_harvest_by_list_ids")
    @patch.object(oai_metadata_format_api, "update_for_all_harvest_by_list_ids")
    @patch.object(oai_set_api, "get_all_by_registry_id")
    @patch.object(oai_metadata_format_api, "get_all_by_registry_id")
    @patch.object(HarvestSerializer, "data")
    @patch.object(HarvestSerializer, "is_valid")
    @patch.object(oai_registry_api, "get_by_id")
    @patch.object(oai_registry_api, "harvest_registry")
    @patch.object(OaiPmhMessage, "get_message_labelled")
    def test_staff_returns_http_200(
        self,
        mock_oaipmhmessage_get_message_labelled,
        mock_oai_registry_api_harvest_registry,
        mock_oai_registry_api_get_by_id,
        mock_data_serializer_is_valid,
        mock_data_serializer_data,
        mock_oai_metadata_format_api_get_all_by_registry_id,
        mock_oai_set_api_get_all_by_registry_id,
        mock_oai_metadata_format_api_update_for_all_harvest_by_list_ids,
        mock_oai_set_api_update_for_all_harvest_by_list_ids,
        mock_queryset_values_list,
    ):
        """test_staff_returns_http_200"""

        # Arrange
        mock_oaipmhmessage_get_message_labelled.return_value = None
        mock_oai_registry_api_harvest_registry.return_value = []
        mock_oai_registry_api_get_by_id.return_value = Mock(spec=OaiRegistry)
        mock_data_serializer_data.return_value = Mock(spec=HarvestSerializer)
        mock_data_serializer_is_valid.return_value = True
        mock_oai_metadata_format_api_get_all_by_registry_id.return_value = Mock(
            spec=QuerySet
        )
        mock_oai_set_api_get_all_by_registry_id.return_value = Mock(spec=QuerySet)
        mock_oai_metadata_format_api_update_for_all_harvest_by_list_ids.return_value = (
            None
        )
        mock_oai_set_api_update_for_all_harvest_by_list_ids.return_value = None
        mock_queryset_values_list.return_value = None

        # Act
        response = RequestMock.do_request_put(
            rest_oai_registry.Harvest.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestActivateRegistry(SimpleTestCase):
    """Test Activate Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"registry_id": 1}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.ActivateRegistry.as_view(), None, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.ActivateRegistry.as_view(), user=user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(oai_registry_api, "get_by_id")
    @patch.object(oai_registry_api, "upsert")
    @patch.object(OaiPmhMessage, "get_message_labelled")
    def test_staff_returns_http_200(
        self,
        mock_oaipmhmessage_get_message_labelled,
        mock_oai_registry_api_upsert,
        mock_oai_registry_api_get_by_id,
    ):
        """test_staff_returns_http_200"""

        # Arrange
        mock_oaipmhmessage_get_message_labelled.return_value = None
        mock_oai_registry_api_upsert.return_value = None
        mock_oai_registry_api_get_by_id.return_value = Mock(spec=OaiRegistry)

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.ActivateRegistry.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDeactivateRegistry(SimpleTestCase):
    """Test Deactivate Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"registry_id": 1}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.DeactivateRegistry.as_view(), None, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.DeactivateRegistry.as_view(), user=user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(oai_registry_api, "get_by_id")
    @patch.object(oai_registry_api, "upsert")
    @patch.object(OaiPmhMessage, "get_message_labelled")
    def test_staff_returns_http_200(
        self,
        mock_oaipmhmessage_get_message_labelled,
        mock_oai_registry_api_upsert,
        mock_oai_registry_api_get_by_id,
    ):
        """test_staff_returns_http_200"""

        # Arrange
        mock_oaipmhmessage_get_message_labelled.return_value = None
        mock_oai_registry_api_upsert.return_value = None
        mock_oai_registry_api_get_by_id.return_value = Mock(spec=OaiRegistry)

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_registry.DeactivateRegistry.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetAllRegistries(SimpleTestCase):
    """Test Get All Registries"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryList.as_view(), None, None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        # Arrange
        user = create_mock_user("1", has_perm=True)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryList.as_view(), user, None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(oai_registry_api, "get_all")
    @patch.object(RegistrySerializer, "data")
    def test_staff_returns_http_200(
        self, mock_oai_registry_api_get_all, mock_data_serializer_data
    ):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", has_perm=True, is_staff=True)
        mock_oai_registry_api_get_all.return_value = None
        mock_data_serializer_data.return_value = None

        # Act
        response = RequestMock.do_request_get(
            rest_oai_registry.RegistryList.as_view(), user, None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCreateRegistry(SimpleTestCase):
    """Test Create Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"url": "", "harvest_rate": 1, "harvest": False}

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        # Act
        response = RequestMock.do_request_post(
            rest_oai_registry.RegistryList.as_view(), None, None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        # Arrange
        user = create_mock_user("1", has_perm=True)

        # Act
        response = RequestMock.do_request_post(
            rest_oai_registry.RegistryList.as_view(), user, None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(RegistrySerializer, "data")
    @patch.object(RegistrySerializer, "is_valid")
    @patch.object(RegistrySerializer, "save")
    @patch.object(OaiPmhMessage, "get_message_labelled")
    def test_staff_returns_http_201(
        self,
        mock_oaipmhmessage_get_message_labelled,
        mock_data_serializer_save,
        mock_data_serializer_is_valid,
        mock_data_serializer_data,
    ):
        """test_staff_returns_http_201"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        mock_data_serializer_data.return_value = None
        mock_data_serializer_is_valid.return_value = True
        mock_data_serializer_save.return_value = Mock(spec=OaiRegistry)
        mock_oaipmhmessage_get_message_labelled.return_value = None

        # Act
        response = RequestMock.do_request_post(
            rest_oai_registry.RegistryList.as_view(), user, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
