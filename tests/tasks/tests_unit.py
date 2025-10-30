""" Unit tests for tasks.py module.
"""

from unittest.mock import patch, MagicMock

from django.test import TestCase

from core_oaipmh_harvester_app import tasks
from core_main_app.utils.datetime import datetime_now, datetime_timedelta


class TestHarvestRegistries(TestCase):
    """Unit tests for harvest_registries tasks."""

    def setUp(self):
        """setUp"""

        # Create a harvestable registry.
        self.registry_sample = MagicMock()
        self.registry_sample.harvest = True
        self.registry_sample.is_harvesting = False
        self.registry_sample.last_update = datetime_now() - datetime_timedelta(
            days=7
        )
        self.registry_sample.harvest_rate = 30  # in seconds

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    def test_get_all_activated_registries_called(self, mock_oai_registry_api):
        """test_get_all_activated_registries_called"""
        tasks.harvest_registries()

        mock_oai_registry_api.get_all_activated_registry.assert_called_with()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch.object(tasks, "logger")
    def test_get_all_activated_registries_exception_logged(
        self, mock_logger, mock_oai_registry_api
    ):
        """test_get_all_activated_registries_exception_logged"""
        mock_oai_registry_api.get_all_activated_registry.side_effect = (
            Exception(
                "mock_oai_registry_api_get_all_activated_registry_exception"
            )
        )

        tasks.harvest_registries()

        mock_oai_registry_api.get_all_activated_registry.assert_called()
        mock_logger.error.assert_called()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    def test_registry_not_to_be_harvest_is_skipped(
        self, mock_oai_registry_api
    ):
        """test_registry_not_to_be_harvest_is_skipped"""
        self.registry_sample.harvest = False
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]

        tasks.harvest_registries()

        mock_oai_registry_api.update_registry_info.assert_not_called()
        mock_oai_registry_api.harvest_registry.assert_not_called()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    def test_registry_already_harvesting_is_skipped(
        self, mock_oai_registry_api
    ):
        """test_registry_already_harvesting_is_skipped"""
        self.registry_sample.is_harvesting = True
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]

        tasks.harvest_registries()

        mock_oai_registry_api.update_registry_info.assert_not_called()
        mock_oai_registry_api.harvest_registry.assert_not_called()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    def test_recently_harvested_registry_is_skipped(
        self, mock_oai_registry_api
    ):
        """test_recently_harvested_registry_is_skipped"""
        self.registry_sample.last_update = datetime_now() + datetime_timedelta(
            hours=1
        )
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]

        tasks.harvest_registries()

        mock_oai_registry_api.update_registry_info.assert_not_called()
        mock_oai_registry_api.harvest_registry.assert_not_called()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    def test_update_registry_info_is_called(self, mock_oai_registry_api):
        """test_update_registry_info_is_called"""
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]

        tasks.harvest_registries()

        mock_oai_registry_api.update_registry_info.assert_called_with(
            self.registry_sample
        )

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch.object(tasks, "logger")
    def test_update_registry_info_exception_logged(
        self, mock_logger, mock_oai_registry_api
    ):
        """test_update_registry_info_exception_logged"""
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]
        mock_oai_registry_api.update_registry_info.side_effect = Exception(
            "mock_oai_registry_api_update_registry_info_exception"
        )

        tasks.harvest_registries()

        mock_oai_registry_api.update_registry_info.assert_called()
        mock_logger.error.assert_called()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    def test_harvest_registry_is_called(self, mock_oai_registry_api):
        """test_harvest_registry_is_called"""
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]

        tasks.harvest_registries()

        mock_oai_registry_api.harvest_registry.assert_called_with(
            self.registry_sample
        )

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch.object(tasks, "logger")
    def test_harvest_registry_exception_logged(
        self, mock_logger, mock_oai_registry_api
    ):
        """test_harvest_registry_exception_logged"""
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]
        mock_oai_registry_api.harvest_registry.side_effect = Exception(
            "mock_oai_registry_api_harvest_registry_exception"
        )

        tasks.harvest_registries()

        mock_oai_registry_api.harvest_registry.assert_called()
        mock_logger.error.assert_called()
