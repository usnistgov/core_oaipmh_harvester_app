""" Int Test Rest OaiRecord
"""
from django.test import override_settings, tag
from rest_framework import status

from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoDBIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_harvester_app.rest.oai_record import (
    views as oai_record_rest_views,
)
from core_oaipmh_harvester_app.tasks import init_mongo_indexing
from tests.components.oai_registry.fixtures.fixtures import OaiPmhFixtures


class TestExecuteQueryView(MongoDBIntegrationBaseTestCase):
    """Test Execute Query View"""

    @classmethod
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    def setUpClass(cls):
        super().setUpClass()
        init_mongo_indexing()

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    def setUp(self):
        """setUp"""
        self.fixture = OaiPmhFixtures()
        self.fixture.insert_registry()
        self.one_record_data = {
            "query": "{"
            '"experiment.experimentType.tracerDiffusivity.material.materialName": "Test 1"}'
        }
        self.user = create_mock_user("1")

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_post_query_zero_data_returns_zero_data(self):
        """test_post_query_zero_data_returns_zero_data"""

        # Arrange
        data = {"query": '{"bad.path": "bad_value"}'}

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteQueryView.as_view(),
            self.user,
            data=data,
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_post_query_one_data_returns_http_200(self):
        """test_post_query_one_data_returns_http_200"""

        # Arrange
        data = self.one_record_data

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteQueryView.as_view(),
            self.user,
            data=data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_post_query_one_data_returns_one_data(self):
        """test_post_query_one_data_returns_one_data"""

        # Arrange
        data = self.one_record_data

        # Act
        response = RequestMock.do_request_post(
            oai_record_rest_views.ExecuteQueryView.as_view(),
            self.user,
            data=data,
        )

        # Assert
        self.assertEqual(len(response.data), 1)
