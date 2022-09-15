""" Int Test Rest OaiRecord
"""
from rest_framework import status

from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_harvester_app.rest.oai_record import views as oai_record_rest_views
from tests.components.oai_registry.fixtures.fixtures import OaiPmhFixtures


class TestExecuteQueryView(MongoIntegrationBaseTestCase):
    """Test Execute Query View"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.fixture.insert_registry()
        self.one_record_data = {
            "query": "{"
            '"experiment.experimentType.tracerDiffusivity.material.materialName": "Test 1"}'
        }
        self.user = create_mock_user("1")

    def test_post_query_zero_data_returns_zero_data(self):
        """test_post_query_zero_data_returns_zero_data"""

        # Arrange
        data = {"query": '{"bad.path": "bad_value"}'}

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteQueryView.as_view(), self.user, data=data
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_post_query_one_data_returns_http_200(self):
        """test_post_query_one_data_returns_http_200"""

        # Arrange
        data = self.one_record_data

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteQueryView.as_view(), self.user, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_query_one_data_returns_one_data(self):
        """test_post_query_one_data_returns_one_data"""

        # Arrange
        data = self.one_record_data

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteQueryView.as_view(), self.user, data=data
        )

        # Assert
        self.assertEqual(len(response.data), 1)
