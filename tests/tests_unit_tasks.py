""" Unit tests for tasks
"""

from unittest import TestCase
from unittest.mock import patch

from core_oaipmh_harvester_app.tasks import init_harvest


class TestInitHarvest(TestCase):
    """Test Init Harvest"""

    @patch(
        "core_oaipmh_harvester_app.components.oai_registry.api.get_all_activated_registry"
    )
    @patch("core_oaipmh_harvester_app.tasks.watch_registry_harvest_task")
    def test_init_harvest_calls_harvest_task(
        self, mock_watch_registry_harvest_task, mock_get_all_activated_registry
    ):
        """test_init_harvest_calls_harvest_task"""
        # Arrange
        mock_get_all_activated_registry.return_value = []

        # Act
        init_harvest()

        # Assert
        self.assertEqual(
            mock_watch_registry_harvest_task.apply_async.call_count, 1
        )
