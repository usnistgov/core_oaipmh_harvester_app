"""Unit tests for tasks.py module."""

import datetime
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.utils.timezone import make_aware

from core_oaipmh_harvester_app import tasks
from core_main_app.utils.datetime import datetime_timedelta


class TestHarvestRegistries(TestCase):
    """Unit tests for harvest_registries tasks."""

    def setUp(self):
        """setUp"""
        # Fixed aware datetime for deterministic tests
        self.fixed_now = make_aware(datetime.datetime(2020, 1, 1, 12, 0, 0))

        # Create a harvestable registry.
        self.registry_sample = MagicMock()
        self.registry_sample.harvest = True
        self.registry_sample.is_harvesting = False
        # Ensure last_update is aware and in the past
        self.registry_sample.last_update = self.fixed_now - datetime_timedelta(
            days=7
        )
        self.registry_sample.harvest_rate = 30  # in seconds

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch("core_main_app.utils.datetime.datetime_now")
    def test_get_all_activated_registries_called(
        self, mock_datetime_now, mock_oai_registry_api
    ):
        """test_get_all_activated_registries_called"""
        mock_datetime_now.return_value = self.fixed_now
        tasks.harvest_registries()

        mock_oai_registry_api.get_all_activated_registry.assert_called_with()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch.object(tasks, "logger")
    @patch("core_main_app.utils.datetime.datetime_now")
    def test_get_all_activated_registries_exception_logged(
        self, mock_datetime_now, mock_logger, mock_oai_registry_api
    ):
        """test_get_all_activated_registries_exception_logged"""
        mock_datetime_now.return_value = self.fixed_now
        mock_oai_registry_api.get_all_activated_registry.side_effect = (
            Exception(
                "mock_oai_registry_api_get_all_activated_registry_exception"
            )
        )

        tasks.harvest_registries()

        mock_oai_registry_api.get_all_activated_registry.assert_called()
        mock_logger.error.assert_called()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch("core_main_app.utils.datetime.datetime_now")
    def test_registry_not_to_be_harvest_is_skipped(
        self, mock_datetime_now, mock_oai_registry_api
    ):
        """test_registry_not_to_be_harvest_is_skipped"""
        mock_datetime_now.return_value = self.fixed_now
        self.registry_sample.harvest = False
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]

        tasks.harvest_registries()

        mock_oai_registry_api.update_registry_info.assert_not_called()
        mock_oai_registry_api.harvest_registry.assert_not_called()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch("core_main_app.utils.datetime.datetime_now")
    def test_registry_already_harvesting_is_skipped(
        self, mock_datetime_now, mock_oai_registry_api
    ):
        """test_registry_already_harvesting_is_skipped"""
        mock_datetime_now.return_value = self.fixed_now
        self.registry_sample.is_harvesting = True
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]

        tasks.harvest_registries()

        mock_oai_registry_api.update_registry_info.assert_not_called()
        mock_oai_registry_api.harvest_registry.assert_not_called()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch("core_main_app.utils.datetime.datetime_now")
    def test_recently_harvested_registry_is_skipped(
        self, mock_datetime_now, mock_oai_registry_api
    ):
        """test_recently_harvested_registry_is_skipped"""
        mock_datetime_now.return_value = self.fixed_now
        self.registry_sample.last_update = self.fixed_now + datetime_timedelta(
            hours=1
        )
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]

        tasks.harvest_registries()

        mock_oai_registry_api.update_registry_info.assert_not_called()
        mock_oai_registry_api.harvest_registry.assert_not_called()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch("core_main_app.utils.datetime.datetime_now")
    def test_update_registry_info_is_called(
        self, mock_datetime_now, mock_oai_registry_api
    ):
        """test_update_registry_info_is_called"""
        mock_datetime_now.return_value = self.fixed_now
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]

        tasks.harvest_registries()

        mock_oai_registry_api.update_registry_info.assert_called_with(
            self.registry_sample
        )

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch.object(tasks, "logger")
    @patch("core_main_app.utils.datetime.datetime_now")
    def test_update_registry_info_exception_logged(
        self, mock_datetime_now, mock_logger, mock_oai_registry_api
    ):
        """test_update_registry_info_exception_logged"""
        mock_datetime_now.return_value = self.fixed_now
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
    @patch("core_main_app.utils.datetime.datetime_now")
    def test_harvest_registry_is_called(
        self, mock_datetime_now, mock_oai_registry_api
    ):
        """test_harvest_registry_is_called"""
        mock_datetime_now.return_value = self.fixed_now
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]

        tasks.harvest_registries()

        mock_oai_registry_api.harvest_registry.assert_called_with(
            self.registry_sample
        )

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch.object(tasks, "logger")
    @patch("core_main_app.utils.datetime.datetime_now")
    def test_harvest_registry_exception_logged(
        self, mock_datetime_now, mock_logger, mock_oai_registry_api
    ):
        """test_harvest_registry_exception_logged"""
        mock_datetime_now.return_value = self.fixed_now
        mock_oai_registry_api.get_all_activated_registry.return_value = [
            self.registry_sample
        ]
        mock_oai_registry_api.harvest_registry.side_effect = Exception(
            "mock_oai_registry_api_harvest_registry_exception"
        )

        tasks.harvest_registries()

        mock_oai_registry_api.harvest_registry.assert_called()
        mock_logger.error.assert_called()

    @patch("core_oaipmh_harvester_app.components.oai_registry.api")
    @patch("core_main_app.utils.datetime.datetime_now")
    @patch.object(tasks, "logger")
    def test_harvest_registries_continues_after_exception(
        self, mock_logger, mock_datetime_now, mock_api
    ):
        """test_harvest_registries_continues_after_exception"""
        mock_datetime_now.return_value = None
        registry1 = MagicMock(name="registry1")
        registry1.harvest = True
        registry1.is_harvesting = False
        registry1.last_update = None
        registry1.harvest_rate = 30
        registry2 = MagicMock(name="registry2")
        registry2.harvest = True
        registry2.is_harvesting = False
        registry2.last_update = None
        registry2.harvest_rate = 30

        mock_api.get_all_activated_registry.return_value = [
            registry1,
            registry2,
        ]
        mock_api.update_registry_info.side_effect = [
            Exception("mock_exception"),
            None,
        ]
        mock_api.harvest_registry.return_value = []

        tasks.harvest_registries()

        self.assertEqual(mock_api.update_registry_info.call_count, 2)
        self.assertTrue(mock_api.harvest_registry.called)
        self.assertTrue(mock_logger.error.called)
