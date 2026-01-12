""" Unit tests for discover.py module.
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.core.exceptions import ObjectDoesNotExist
from django.test import override_settings, tag

from core_oaipmh_harvester_app import discover


class TestInitHarvest(TestCase):
    """Unit tests for init_harvest function in the discover module"""

    def setUp(self):
        """setUp"""
        pass

    @patch.object(discover, "CrontabSchedule")
    def test_crontab_schedule_get_called(self, mock_crontab_schedule):
        """test_crontab_schedule_get_called"""
        mock_harvest_rate_value = 135
        discover.WATCH_REGISTRY_HARVEST_RATE = mock_harvest_rate_value
        discover.init_harvest()

        mock_crontab_schedule.objects.get_or_create.assert_called_with(
            minute=f"*/{int(round(mock_harvest_rate_value / 60))}"
        )

    @patch.object(discover, "CrontabSchedule")
    def test_crontab_schedule_is_at_least_one_minute(
        self, mock_crontab_schedule
    ):
        """test_crontab_schedule_is_at_least_one_minute"""
        discover.WATCH_REGISTRY_HARVEST_RATE = 25
        discover.init_harvest()

        mock_crontab_schedule.objects.get_or_create.assert_called_with(
            minute="*/1"
        )

    @patch.object(discover, "CrontabSchedule")
    @patch.object(discover, "logger")
    def test_crontab_schedule_get_exception_is_logged(
        self, mock_logger, mock_crontab_schedule
    ):
        """test_crontab_schedule_get_exception_is_logged"""
        mock_crontab_schedule.side_effect = Exception(
            "mock_crontab_schedule_exception"
        )

        discover.init_harvest()

        mock_logger.error.assert_called()

    @patch.object(discover, "CrontabSchedule")
    @patch.object(discover, "PeriodicTask")
    @patch.object(discover, "harvest_registries")
    def test_periodic_task_get_called(
        self,
        mock_harvest_registries,
        mock_periodic_task,
        mock_crontab_schedule,
    ):
        """test_periodic_task_get_called"""
        mock_schedule = MagicMock()
        mock_result = MagicMock()
        mock_crontab_schedule.objects.get_or_create.return_value = (
            mock_schedule,
            mock_result,
        )

        mock_name = MagicMock()
        mock_harvest_registries.__name__ = mock_name

        discover.init_harvest()

        mock_periodic_task.objects.get.assert_called_with(
            name=mock_name,
        )

    @patch.object(discover, "CrontabSchedule")
    @patch.object(discover, "PeriodicTask")
    @patch.object(discover, "harvest_registries")
    def test_periodic_task_does_not_exist_create_periodic_task(
        self,
        mock_harvest_registries,
        mock_periodic_task,
        mock_crontab_schedule,
    ):
        """test_periodic_task_does_not_exist_create_periodic_task"""
        mock_name = MagicMock()
        mock_harvest_registries.__name__ = mock_name

        mock_schedule = MagicMock()
        mock_result = MagicMock()
        mock_crontab_schedule.objects.get_or_create.return_value = (
            mock_schedule,
            mock_result,
        )

        mock_periodic_task.objects.get.side_effect = ObjectDoesNotExist(
            "mock_periodic_task_does_not_exist"
        )

        discover.init_harvest()

        mock_periodic_task.objects.create.assert_called_with(
            crontab=mock_schedule,
            name=mock_name,
            task="core_oaipmh_harvester_app.tasks.harvest_registries",
        )

    @patch.object(discover, "CrontabSchedule")
    @patch.object(discover, "PeriodicTask")
    @patch.object(discover, "logger")
    def test_periodic_task_get_exception_is_logged(
        self, mock_logger, mock_periodic_task, mock_crontab_schedule
    ):
        """test_periodic_task_get_exception_is_logged"""
        mock_schedule = MagicMock()
        mock_result = MagicMock()
        mock_crontab_schedule.objects.get_or_create.return_value = (
            mock_schedule,
            mock_result,
        )

        mock_periodic_task.objects.get.side_effect = Exception(
            "mock_periodic_task_exception"
        )

        discover.init_harvest()

        mock_periodic_task.objects.get.assert_called()
        mock_logger.error.assert_called()

    @patch.object(discover, "CrontabSchedule")
    @patch.object(discover, "PeriodicTask")
    @patch.object(discover, "harvest_registries")
    @patch.object(discover, "logger")
    def test_periodic_task_create_exception_is_logged(
        self,
        mock_logger,
        mock_harvest_registries,
        mock_periodic_task,
        mock_crontab_schedule,
    ):
        """test_periodic_task_create_exception_is_logged"""
        mock_name = MagicMock()
        mock_harvest_registries.__name__ = mock_name

        mock_schedule = MagicMock()
        mock_result = MagicMock()
        mock_crontab_schedule.objects.get_or_create.return_value = (
            mock_schedule,
            mock_result,
        )

        mock_periodic_task.objects.get.side_effect = ObjectDoesNotExist(
            "mock_periodic_task_does_not_exist"
        )
        mock_periodic_task.objects.create.side_effect = Exception(
            "mock_periodic_task_exception"
        )

        discover.init_harvest()

        mock_periodic_task.objects.create.assert_called()
        mock_logger.error.assert_called()

    @patch.object(discover, "CrontabSchedule")
    @patch.object(discover, "PeriodicTask")
    @patch.object(discover, "harvest_registries")
    def test_crontab_different_from_schedule_update_crontab(
        self,
        mock_harvest_registries,
        mock_periodic_task,
        mock_crontab_schedule,
    ):
        """test_crontab_different_from_schedule_update_crontab"""
        mock_name = MagicMock()
        mock_harvest_registries.__name__ = mock_name

        mock_schedule = MagicMock()
        mock_result = MagicMock()
        mock_crontab_schedule.objects.get_or_create.return_value = (
            mock_schedule,
            mock_result,
        )

        mock_crontab = MagicMock()
        mock_periodic_task_instance = MagicMock()
        mock_periodic_task_instance.crontab = mock_crontab

        mock_periodic_task.objects.get.return_value = (
            mock_periodic_task_instance
        )

        discover.init_harvest()

        self.assertEqual(mock_periodic_task_instance.crontab, mock_schedule)

    @patch.object(discover, "CrontabSchedule")
    @patch.object(discover, "PeriodicTask")
    @patch.object(discover, "harvest_registries")
    def test_crontab_different_from_schedule_save_periodic_task(
        self,
        mock_harvest_registries,
        mock_periodic_task,
        mock_crontab_schedule,
    ):
        """test_crontab_different_from_schedule_save_periodic_task"""
        mock_name = MagicMock()
        mock_harvest_registries.__name__ = mock_name

        mock_schedule = MagicMock()
        mock_result = MagicMock()
        mock_crontab_schedule.objects.get_or_create.return_value = (
            mock_schedule,
            mock_result,
        )

        mock_periodic_task_instance = MagicMock()

        mock_periodic_task.objects.get.return_value = (
            mock_periodic_task_instance
        )

        discover.init_harvest()

        mock_periodic_task_instance.save.assert_called_with()

    @patch.object(discover, "CrontabSchedule")
    @patch.object(discover, "PeriodicTask")
    @patch.object(discover, "harvest_registries")
    @patch.object(discover, "logger")
    def test_save_periodic_task_exception_is_logged(
        self,
        mock_logger,
        mock_harvest_registries,
        mock_periodic_task,
        mock_crontab_schedule,
    ):
        """test_save_periodic_task_exception_is_logged"""
        mock_name = MagicMock()
        mock_harvest_registries.__name__ = mock_name

        mock_schedule = MagicMock()
        mock_result = MagicMock()
        mock_crontab_schedule.objects.get_or_create.return_value = (
            mock_schedule,
            mock_result,
        )

        mock_periodic_task_instance = MagicMock()
        mock_periodic_task_instance.save.side_effect = Exception(
            "mock_periodic_task_instance_save_exception"
        )

        mock_periodic_task.objects.get.return_value = (
            mock_periodic_task_instance
        )

        discover.init_harvest()

        mock_logger.error.assert_called()


class TestInitMongoIndexing(TestCase):
    """Unit tests for init_mongo_indexing function in the discover module"""

    @override_settings(MONGODB_INDEXING=False)
    @patch.object(discover, "init_text_index")
    def test_mongo_indexing_false_does_not_call_init_text_index(
        self, mock_init_text_index
    ):
        """test_mongo_indexing_false_does_not_call_init_text_index"""
        discover.init_mongo_indexing()

        mock_init_text_index.assert_not_called()

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    @patch("core_oaipmh_harvester_app.components.mongo.models.MongoOaiRecord")
    @patch.object(discover, "init_text_index")
    def test_init_text_index_called(
        self, mock_init_text_index, mock_mongo_oai_record
    ):
        """test_init_text_index_called"""
        discover.init_mongo_indexing()

        mock_init_text_index.assert_called_with(mock_mongo_oai_record)

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    @patch("core_oaipmh_harvester_app.components.mongo.models.MongoOaiRecord")
    @patch.object(discover, "init_text_index")
    @patch.object(discover, "logger")
    def test_init_text_index_exception_is_logged(
        self, mock_logger, mock_init_text_index, mock_mongo_oai_record
    ):
        """test_init_text_index_exception_is_logged"""
        mock_init_text_index.side_effect = Exception(
            "mock_init_text_index_exception"
        )

        discover.init_mongo_indexing()

        mock_init_text_index.assert_called()
        mock_logger.error.assert_called()

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    @patch("core_oaipmh_harvester_app.components.mongo.models.MongoOaiRecord")
    @patch.object(discover, "OaiRecord")
    @patch.object(discover, "init_text_index")
    @patch.object(discover, "post_save")
    def test_post_save_connect_called(
        self,
        mock_post_save,
        mock_init_text_index,
        mock_oai_record,
        mock_mongo_oai_record,
    ):
        """test_post_save_connect_called"""
        discover.init_mongo_indexing()

        mock_post_save.connect.assert_called_with(
            mock_mongo_oai_record.post_save_data, sender=mock_oai_record
        )

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    @patch("core_oaipmh_harvester_app.components.mongo.models.MongoOaiRecord")
    @patch.object(discover, "OaiRecord")
    @patch.object(discover, "init_text_index")
    @patch.object(discover, "post_save")
    @patch.object(discover, "logger")
    def test_post_save_connect_exception_is_logged(
        self,
        mock_logger,
        mock_post_save,
        mock_init_text_index,
        mock_oai_record,
        mock_mongo_oai_record,
    ):
        """test_post_save_connect_exception_is_logged"""
        mock_post_save.connect.side_effect = Exception(
            "mock_post_save_connect_exception"
        )

        discover.init_mongo_indexing()

        mock_post_save.connect.assert_called()
        mock_logger.error.assert_called()

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    @patch("core_oaipmh_harvester_app.components.mongo.models.MongoOaiRecord")
    @patch.object(discover, "OaiRecord")
    @patch.object(discover, "init_text_index")
    @patch.object(discover, "post_save")
    @patch.object(discover, "post_delete")
    def test_post_delete_connect_called(
        self,
        mock_post_delete,
        mock_post_save,
        mock_init_text_index,
        mock_oai_record,
        mock_mongo_oai_record,
    ):
        """test_post_delete_connect_called"""
        discover.init_mongo_indexing()

        mock_post_delete.connect.assert_called_with(
            mock_mongo_oai_record.post_delete_data, sender=mock_oai_record
        )

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    @patch("core_oaipmh_harvester_app.components.mongo.models.MongoOaiRecord")
    @patch.object(discover, "OaiRecord")
    @patch.object(discover, "init_text_index")
    @patch.object(discover, "post_save")
    @patch.object(discover, "post_delete")
    @patch.object(discover, "logger")
    def test_post_delete_connect_exception_is_logged(
        self,
        mock_logger,
        mock_post_delete,
        mock_post_save,
        mock_init_text_index,
        mock_oai_record,
        mock_mongo_oai_record,
    ):
        """test_post_delete_connect_exception_is_logged"""
        mock_post_delete.connect.side_effect = Exception(
            "mock_post_delete_connect_exception"
        )

        discover.init_mongo_indexing()

        mock_post_delete.connect.assert_called()
        mock_logger.error.assert_called()
