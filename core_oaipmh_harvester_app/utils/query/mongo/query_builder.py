"""OAI-PMH Query builder class
"""
from core_main_app.utils.query.mongo.query_builder import QueryBuilder


class OaiPmhQueryBuilder(QueryBuilder):
    """Query builder class"""

    def add_list_metadata_formats_criteria(self, list_metadata_format_ids):
        """Add a criteria on OaiHarvesterMetadataFormat.

        Args:
            list_metadata_format_ids: List of OaiHarvesterMetadataFormat ids.

        Returns:

        """
        self.criteria.append(
            {"harvester_metadata_format": {"$in": list_metadata_format_ids}}
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
        self.criteria.append({"registry": {"$in": list_registry_ids}})
