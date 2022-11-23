""" REST views for the data API
"""
import json
from django.conf import settings
from rest_framework.response import Response

from core_main_app.utils.databases.mongo.pymongo_database import (
    get_full_text_query,
)
from core_main_app.utils.pagination.django_paginator.results_paginator import (
    ResultsPaginator,
)
from core_oaipmh_harvester_app.rest.oai_record.abstract_views import (
    AbstractExecuteQueryView,
)


class ExecuteQueryView(AbstractExecuteQueryView):
    """Execute Query View"""

    def get_registries(self):
        """Get a list of registry ids. Should return empty list if not found. JSON format.

        Returns:
            List of registry ids (JSON format).

        """
        return self.request.data.get("registries", json.dumps(list()))

    def build_response(self, data_list):
        """Build the paginated response.

        Args:
            data_list: List of data.

        Returns:
            The response.

        """
        # Paginator
        page = self.request.query_params.get("page", 1)
        results_paginator = ResultsPaginator.get_results(data_list, page, 10)

        if settings.MONGODB_INDEXING:
            from core_oaipmh_harvester_app.rest.mongo.serializers import (
                MongoOaiRecordSerializer,
            )

            serializer = MongoOaiRecordSerializer
        else:
            from core_oaipmh_harvester_app.rest.serializers import (
                OaiRecordSerializer,
            )

            serializer = OaiRecordSerializer

        data_serializer = serializer(results_paginator, many=True)

        return Response(data_serializer.data)


class ExecuteKeywordQueryView(ExecuteQueryView):
    """Execute Keyword Query View"""

    def build_query(self, query, templates, options):
        """Build the raw query. Prepare the query for a keyword search.
        Args:
            query:
            templates:
            options:

        Returns:
            The raw query.

        """
        # build query builder
        query = json.dumps(get_full_text_query(query))
        return super().build_query(str(query), templates, options)
