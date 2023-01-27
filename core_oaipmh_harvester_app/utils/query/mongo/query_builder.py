"""OAI-PMH Query builder class
"""
from core_main_app.utils.query.mongo.query_builder import QueryBuilder
from django.conf import settings


class OaiPmhQueryBuilder(QueryBuilder):
    """Query builder class"""

    def add_list_metadata_formats_criteria(self, list_metadata_format_ids):
        """Add a criteria on OaiHarvesterMetadataFormat.

        Args:
            list_metadata_format_ids: List of OaiHarvesterMetadataFormat ids.

        Returns:

        """
        if settings.MONGODB_INDEXING:
            harvester_metadata_key = "_harvester_metadata_format_id"
        else:
            harvester_metadata_key = "harvester_metadata_format"
        self.criteria.append(
            {harvester_metadata_key: {"$in": list_metadata_format_ids}}
        )

    def add_not_deleted_criteria(self):
        """Add a criteria on the deleted field. Do not include deleted records.

        Returns:

        """
        self.criteria.append({"deleted": False})

    def add_list_registries_criteria(self, list_registry_ids):
        """Add a criteria on OaiRegistry.

        Returns:

        """
        if settings.MONGODB_INDEXING:
            registry_key = "_registry_id"
        else:
            registry_key = "registry"
        self.criteria.append({registry_key: {"$in": list_registry_ids}})


class OaiPmhAggregateQueryBuilder(OaiPmhQueryBuilder):
    """Query builder class for aggregate queries"""

    def add_list_metadata_formats_criteria(self, list_metadata_format_ids):
        """Add a criteria on OaiHarvesterMetadataFormat.

        Args:
            list_metadata_format_ids: List of OaiHarvesterMetadataFormat ids.

        Returns:

        """
        self.criteria.append(
            {"harvester_metadata_format": {"$in": list_metadata_format_ids}}
        )

    def add_list_registries_criteria(self, list_registry_ids):
        """Add a criteria on OaiRegistry.

        Returns:

        """
        self.criteria.append({"registry": {"$in": list_registry_ids}})
