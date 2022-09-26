"""Url router for the REST API
"""

from django.urls import re_path

from core_oaipmh_harvester_app.rest.oai_record import views as oai_record_views
from core_oaipmh_harvester_app.rest.oai_registry import (
    views as oai_registry_views,
)

urlpatterns = [
    re_path(
        r"^registry/(?P<registry_id>\w+)/info/$",
        oai_registry_views.InfoRegistry.as_view(),
        name="core_oaipmh_harvester_app_rest_registry_info",
    ),
    re_path(
        r"^registry/(?P<registry_id>\w+)/activate/$",
        oai_registry_views.ActivateRegistry.as_view(),
        name="core_oaipmh_harvester_app_rest_harvest",
    ),
    re_path(
        r"^registry/(?P<registry_id>\w+)/deactivate/$",
        oai_registry_views.DeactivateRegistry.as_view(),
        name="core_oaipmh_harvester_app_rest_harvest",
    ),
    re_path(
        r"^registry/(?P<registry_id>\w+)/harvest/$",
        oai_registry_views.Harvest.as_view(),
        name="core_oaipmh_harvester_app_rest_harvest",
    ),
    re_path(
        r"^registry/(?P<registry_id>\w+)/$",
        oai_registry_views.RegistryDetail.as_view(),
        name="core_oaipmh_harvester_app_rest_registry_detail",
    ),
    re_path(
        r"^registry/$",
        oai_registry_views.RegistryList.as_view(),
        name="core_oaipmh_harvester_app_rest_registry_list",
    ),
    re_path(
        r"^registry/local/query/keyword/$",
        oai_record_views.ExecuteKeywordQueryView.as_view(),
        name="core_oaipmh_harvester_app_rest_local_query_keyword",
    ),
    re_path(
        r"^registry/local/query/$",
        oai_record_views.ExecuteQueryView.as_view(),
        name="core_oaipmh_harvester_app_rest_local_query",
    ),
]
