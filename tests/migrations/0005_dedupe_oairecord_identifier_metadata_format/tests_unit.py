"""Unit tests for data migrations"""

import importlib
from unittest.mock import MagicMock

from django.test import TestCase as DjangoTestCase

dedupe_oai_records = importlib.import_module(
    "core_oaipmh_harvester_app.migrations."
    "0005_dedupe_oairecord_identifier_metadata_format"
).dedupe_oai_records


class TestDedupeOaiRecordsMigration(DjangoTestCase):
    def test_dedupe_oai_records_deletes_duplicate_keeps_first(self):
        """test_dedupe_oai_records_deletes_duplicate_keeps_first"""
        # Mock records
        rec1 = MagicMock()
        rec1.identifier = "id1"
        rec1.harvester_metadata_format_id = 1
        rec1.pk = 1
        rec1.delete = MagicMock()
        rec2 = MagicMock()
        rec2.identifier = "id1"
        rec2.harvester_metadata_format_id = 1
        rec2.pk = 2
        rec2.delete = MagicMock()
        # Mock queryset
        mock_qs = MagicMock()
        mock_qs.order_by.return_value = [rec1, rec2]
        mock_model = MagicMock()
        mock_model.objects.all.return_value = mock_qs

        class MockApps:
            @staticmethod
            def get_model(app_label, model_name):  # noqa
                return mock_model

        dedupe_oai_records(MockApps(), None)
        # First record kept, second deleted
        rec2.delete.assert_called_once()
        rec1.delete.assert_not_called()
