""" REST abstract views for the Oai Record API
"""
import json
from abc import ABCMeta, abstractmethod

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import core_oaipmh_harvester_app.components.oai_record.api as oai_record_api
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import (
    api as oai_harvester_metadata_format_api,
)
from core_oaipmh_harvester_app.components.oai_registry import (
    api as oai_registry_api,
)
from core_oaipmh_harvester_app.utils.query.mongo.query_builder import (
    OaiPmhQueryBuilder,
)


# FIXME: Could inherit AbstractExecuteQuery from core_main_app
class AbstractExecuteQueryView(APIView, metaclass=ABCMeta):
    """Abstract Execute Query View"""

    sub_document_root = "dict_content"
    query_builder = OaiPmhQueryBuilder

    def post(self, request):
        """Execute query on OaiRecord and return results

        Parameters:

            {"query": {"$or": [{"image.owner": "Peter"}, {"image.owner.#text":"Peter"}]}}
            {"query": "Keyword1 Keyword2", "registries": "[\"5aa00a074697f6d6ac21946e\"]"}

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of data
            - code: 400
              content: Bad request
            - code: 500
              content: Internal server error
        """
        return self.execute_query()

    def execute_query(self):
        """Compute and return query results"""
        try:
            # get query and templates
            query = self.request.data.get("query", None)
            templates = self.request.data.get("templates", "[]")
            registries = self.get_registries()
            order_by_field = self.request.data.get("order_by_field", "")

            if order_by_field:
                order_by_field = order_by_field.split(",")

            if query is None:
                content = {"message": "Query should be passed in parameter."}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            # prepare query
            raw_query = self.build_query(query, templates, registries)
            # execute query
            data_list = self.execute_json_query(raw_query, order_by_field)
            # build and return response
            return self.build_response(data_list)

        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def build_query(self, query, templates, registries):
        """Build the raw query.

        Args:

            query:
            templates:
            registries:

        Returns:

            The raw query
        """
        # build query builder
        query_builder = self.query_builder(query, self.sub_document_root)

        if type(templates) is str:
            templates = json.loads(templates)

        if type(registries) is str:
            registries = json.loads(registries)

        # if registries, check if activated
        list_activated_registry = list(
            oai_registry_api.get_all_activated_registry().values_list(
                "id", flat=True
            )
        )
        if len(registries) > 0:
            activated_registries = [
                activated_registry_id
                for activated_registry_id in registries
                if activated_registry_id in list_activated_registry
            ]
        else:
            activated_registries = list_activated_registry

        if len(templates) > 0:
            # get list of template ids
            list_template_ids = [template["id"] for template in templates]
            # get all metadata formats used by the registries
            list_metadata_format = (
                oai_harvester_metadata_format_api.get_all_by_list_registry_ids(
                    activated_registries
                )
            )
            # Filter metadata formats that use the given templates
            list_metadata_formats_id = [
                x.id
                for x in list_metadata_format
                if x.template is not None
                and x.template.id in list_template_ids
            ]
            query_builder.add_list_metadata_formats_criteria(
                list_metadata_formats_id
            )
        else:
            # Only activated registries
            query_builder.add_list_registries_criteria(activated_registries)

        # do not include deleted records
        query_builder.add_not_deleted_criteria()
        # create a raw query
        return query_builder.get_raw_query()

    def execute_json_query(self, raw_query, order_by_field):
        """Execute the raw query in database

        Args:

            raw_query: Query to execute
            order_by_field:

        Returns:

            Results of the query
        """
        return oai_record_api.execute_json_query(
            raw_query, self.request.user, order_by_field
        )

    @abstractmethod
    def build_response(self, data_list):
        """Build the paginated response

        Args:

            data_list: List of data

        Returns:

            The response
        """
        raise NotImplementedError("build_response method is not implemented.")

    @abstractmethod
    def get_registries(self):
        """Get a list of registry ids. Should return empty list if not found. JSON format

        Returns:

            List of registry ids (JSON format)
        """
        raise NotImplementedError("get_registries method is not implemented.")
