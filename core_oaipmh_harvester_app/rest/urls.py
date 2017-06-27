"""Url router for the REST API
"""
from django.conf.urls import url
from core_oaipmh_harvester_app.rest.oai_registry import views as oai_registry_views


urlpatterns = [
    url(r'^select/registry$', oai_registry_views.select_registry,
        name='core_oaipmh_harvester_app_rest_select_registry'),
    url(r'^select/all/registries', oai_registry_views.select_all_registries,
        name='core_oaipmh_harvester_app_rest_select_all_registries'),
    url(r'^add/registry$', oai_registry_views.add_registry,
        name='core_oaipmh_harvester_app_rest_add_registry'),
    url(r'^update/registry/info$', oai_registry_views.update_registry_info,
        name='core_oaipmh_harvester_app_rest_update_registry_info'),
    url(r'^update/registry/conf$', oai_registry_views.update_registry_conf,
        name='core_oaipmh_harvester_app_rest_update_registry_conf'),
    url(r'^deactivate/registry$', oai_registry_views.deactivate_registry,
        name='core_oaipmh_harvester_app_rest_deactivate_registry'),
    url(r'^activate/registry$', oai_registry_views.activate_registry,
        name='core_oaipmh_harvester_app_rest_activate_registry'),
    url(r'^delete/registry$', oai_registry_views.delete_registry,
        name='core_oaipmh_harvester_app_rest_delete_registry'),
    url(r'^harvest/registry$', oai_registry_views.harvest_registry,
        name='core_oaipmh_harvester_app_rest_harvest_registry'),
    url(r'^update/registry/harvest/conf$', oai_registry_views.update_registry_harvest_conf,
        name='core_oaipmh_harvester_app_rest_update_registry_harvest_conf'),
]
