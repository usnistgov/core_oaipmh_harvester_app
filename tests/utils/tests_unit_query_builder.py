""" Unit tests for query builder
"""
from unittest import TestCase

from django.test import override_settings

from core_oaipmh_harvester_app.utils.query.mongo.query_builder import (
    OaiPmhQueryBuilder,
    OaiPmhAggregateQueryBuilder,
)


class TestQueryBuilder(TestCase):
    """Test Query Builder"""

    def test_add_metadata_format(self):
        """test_transform_oai_identify_return_object"""

        # Act
        query_builder = OaiPmhQueryBuilder(query={}, sub_document_root="root")
        query_builder.add_list_metadata_formats_criteria(["1"])

        # Assert
        self.assertTrue(
            "harvester_metadata_format" in query_builder.criteria[1]
        )

    @override_settings(MONGODB_INDEXING=True)
    def test_add_metadata_format_for_mongo_query(self):
        """test_transform_oai_identify_return_object"""

        # Act
        query_builder = OaiPmhQueryBuilder(query={}, sub_document_root="root")
        query_builder.add_list_metadata_formats_criteria(["1"])

        # Assert
        self.assertTrue(
            "_harvester_metadata_format_id" in query_builder.criteria[1]
        )

    def test_add_registries(self):
        """test_transform_oai_identify_return_object"""

        # Act
        query_builder = OaiPmhQueryBuilder(query={}, sub_document_root="root")
        query_builder.add_list_registries_criteria(["1"])

        # Assert
        self.assertTrue("registry" in query_builder.criteria[1])

    @override_settings(MONGODB_INDEXING=True)
    def test_add_registries_for_mongo_query(self):
        """test_transform_oai_identify_return_object"""

        # Act
        query_builder = OaiPmhQueryBuilder(query={}, sub_document_root="root")
        query_builder.add_list_registries_criteria(["1"])

        # Assert
        self.assertTrue("_registry_id" in query_builder.criteria[1])


class TestAggregateQueryBuilder(TestCase):
    """Test Aggregate Query Builder"""

    def test_add_metadata_format(self):
        """test_transform_oai_identify_return_object"""

        # Act
        query_builder = OaiPmhAggregateQueryBuilder(
            query={}, sub_document_root="root"
        )
        query_builder.add_list_metadata_formats_criteria(["1"])

        # Assert
        self.assertTrue(
            "harvester_metadata_format" in query_builder.criteria[1]
        )

    def test_add_registries(self):
        """test_transform_oai_identify_return_object"""

        # Act
        query_builder = OaiPmhAggregateQueryBuilder(
            query={}, sub_document_root="root"
        )
        query_builder.add_list_registries_criteria(["1"])

        # Assert
        self.assertTrue("registry" in query_builder.criteria[1])
