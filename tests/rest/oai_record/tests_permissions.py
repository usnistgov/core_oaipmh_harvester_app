""" Permissions Test for OAI Registry Rest API
"""
from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.response import Response

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_harvester_app.rest.oai_record import views as oai_record_rest_views
from core_oaipmh_harvester_app.rest.oai_record.abstract_views import (
    AbstractExecuteQueryView,
)


class TestGetLocalQueryRegistry(SimpleTestCase):
    """Test Get Local Query Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.one_record_data = {
            "query": "{"
            '"experiment.experimentType.tracerDiffusivity.material.materialName": "Test 1"}'
        }
        self.user = create_mock_user("1")

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_anonymous_returns_http_200(self, mock_execute_query):
        """test_anonymous_returns_http_200"""

        # Arrange
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_get(
            oai_record_rest_views.ExecuteQueryView.as_view(), None, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_authenticated_returns_http_200(self, mock_execute_query):
        """test_authenticated_returns_http_200"""

        # Arrange
        user = create_mock_user("1")
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_get(
            oai_record_rest_views.ExecuteQueryView.as_view(), user=user, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_staff_returns_http_200(self, mock_execute_query):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_get(
            oai_record_rest_views.ExecuteQueryView.as_view(), user=user, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPostLocalQueryRegistry(SimpleTestCase):
    """Test Post Local Query Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.one_record_data = {
            "query": "{"
            '"experiment.experimentType.tracerDiffusivity.material.materialName": "Test 1"}'
        }
        self.user = create_mock_user("1")

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_anonymous_returns_http_200(self, mock_execute_query):
        """test_anonymous_returns_http_200"""

        # Arrange
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteQueryView.as_view(), None, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_authenticated_returns_http_200(self, mock_execute_query):
        """test_anonymous_returns_http_200"""

        # Arrange
        user = create_mock_user("1")
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteQueryView.as_view(), user=user, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_staff_returns_http_200(self, mock_execute_query):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteQueryView.as_view(), user=user, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetLocalKeywordQueryRegistry(SimpleTestCase):
    """Test Get Local Keyword Query Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.one_record_data = {
            "query": "{"
            '"experiment.experimentType.tracerDiffusivity.material.materialName": "Test 1"}'
        }
        self.user = create_mock_user("1")

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_anonymous_returns_http_200(self, mock_execute_query):
        """test_anonymous_returns_http_200"""

        # Arrange
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_get(
            oai_record_rest_views.ExecuteKeywordQueryView.as_view(), None, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_authenticated_returns_http_200(self, mock_execute_query):
        """test_authenticated_returns_http_200"""

        # Arrange
        user = create_mock_user("1")
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_get(
            oai_record_rest_views.ExecuteKeywordQueryView.as_view(),
            user=user,
            data=data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_staff_returns_http_200(self, mock_execute_query):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_get(
            oai_record_rest_views.ExecuteKeywordQueryView.as_view(),
            user=user,
            data=data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPostLocalKeywordQueryRegistry(SimpleTestCase):
    """Test Post Local Keyword Query Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.one_record_data = {
            "query": "{"
            '"experiment.experimentType.tracerDiffusivity.material.materialName": "Test 1"}'
        }
        self.user = create_mock_user("1")

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_anonymous_returns_http_200(self, mock_execute_query):
        """test_anonymous_returns_http_200"""

        # Arrange
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteKeywordQueryView.as_view(), None, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_authenticated_returns_http_200(self, mock_execute_query):
        """test_authenticated_returns_http_200"""

        # Arrange
        user = create_mock_user("1")
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteKeywordQueryView.as_view(),
            user=user,
            data=data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_staff_returns_http_200(self, mock_execute_query):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteKeywordQueryView.as_view(),
            user=user,
            data=data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
