""" Unit tests for MongoOaiRecord component
"""
from unittest import TestCase

from django.test import override_settings, tag
from unittest.mock import patch, Mock, MagicMock

from tests.mocks import MockObject


class TestMongoOaiRecordExecuteQuery(TestCase):
    """Test MongoOaiRecord execute_query method"""

    @patch(
        "core_oaipmh_harvester_app.components.mongo.models.MongoOaiRecord.objects"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_returns_queryset_from_mongo_oai_records(
        self, mock_mongo_oai_record_qset
    ):
        """test_returns_queryset_from_mongo_oai_records"""
        from core_oaipmh_harvester_app.components.mongo.models import (
            MongoOaiRecord,
        )

        mock_queryset = MagicMock()
        mock_queryset.order_by.return_value = ["mock_queryset"]
        mock_mongo_oai_record_qset.filter.return_value = mock_queryset
        result = MongoOaiRecord.execute_query("mock_query", [])

        self.assertEqual(result, ["mock_queryset"])

    @patch(
        "core_oaipmh_harvester_app.components.mongo.models.MongoOaiRecord.objects"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_order_by_field_not_none_adds_filtering(
        self, mock_mongo_oai_record_qset
    ):
        """test_order_by_field_not_none_adds_filtering"""
        from core_oaipmh_harvester_app.components.mongo.models import (
            MongoOaiRecord,
        )

        mock_queryset = Mock()
        mock_order_by_filters = ["+mock_field"]
        mock_mongo_oai_record_qset.filter.return_value = mock_queryset
        MongoOaiRecord.execute_query("mock_query", mock_order_by_filters)

        mock_queryset.order_by.assert_called_with(*mock_order_by_filters)


class TestMongoOaiRecordPostDeleteData(TestCase):
    """Test MongoOaiRecord post_delete_data method"""

    @patch(
        "core_oaipmh_harvester_app.components.mongo.models.delete_mongo_oai_record"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=True)
    @tag("mongodb")
    def test_mongo_async_true_uses_async_task(
        self, mock_delete_mongo_oai_record
    ):
        """test_mongo_async_true_uses_async_task"""
        from core_oaipmh_harvester_app.components.mongo.models import (
            MongoOaiRecord,
        )

        mock_id = "mock_id"
        MongoOaiRecord.post_delete_data(None, MockObject(id=mock_id))
        mock_delete_mongo_oai_record.apply_async.assert_called_with((mock_id,))
