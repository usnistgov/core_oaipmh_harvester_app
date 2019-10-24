"""
Url router for the administration site
"""
from django.conf.urls import url
from django.contrib import admin

from core_oaipmh_harvester_app.views.admin import views as admin_views, ajax as admin_ajax

admin_urls = [
    url(r'^harvesters/builder', admin_views.request_builder_view,
        name='core_oaipmh_harvester_app_request_builder'),
    url(r'^harvesters/list', admin_views.registries_view,
        name='core_oaipmh_harvester_app_registries'),
    url(r'^harvesters/registry/add', admin_ajax.add_registry,
        name='core_oaipmh_harvester_app_add_registry'),
    url(r'^harvesters/registry/deactivate', admin_ajax.deactivate_registry,
        name='core_oaipmh_harvester_app_deactivate_registry'),
    url(r'^harvesters/registry/activate', admin_ajax.activate_registry,
        name='core_oaipmh_harvester_app_activate_registry'),
    url(r'^harvesters/registry/delete', admin_ajax.delete_registry,
        name='core_oaipmh_harvester_app_delete_registry'),
    url(r'^harvesters/registry/check/harvest', admin_ajax.check_harvest_registry,
        name='core_oaipmh_harvester_app_check_harvest_registry'),
    url(r'^harvesters/registry/check/update', admin_ajax.check_update_registry,
        name='core_oaipmh_harvester_app_check_update_registry'),
    url(r'^harvesters/registry/check', admin_ajax.check_registry,
        name='core_oaipmh_harvester_app_check_registry'),
    url(r'^harvesters/registry/harvest/(?P<pk>[\w-]+)/edit/$',
        admin_ajax.EditHarvestRegistryView.as_view(),
        name='core_oaipmh_harvester_app_edit_harvest_registry'),
    url(r'^harvesters/registry/(?P<pk>[\w-]+)/edit/$', admin_ajax.EditRegistryView.as_view(),
        name='core_oaipmh_harvester_app_edit_registry'),
    url(r'^harvesters/registry/view', admin_ajax.view_registry,
        name='core_oaipmh_harvester_app_view_registry'),
    url(r'^harvesters/registry/update', admin_ajax.update_registry,
        name='core_oaipmh_harvester_app_update_registry'),
    url(r'^harvesters/registry/harvest', admin_ajax.harvest_registry,
        name='core_oaipmh_harvester_app_harvest_registry'),
    url(r'^harvesters/registry/all/sets', admin_ajax.all_sets,
        name='core_oaipmh_harvester_app_all_sets'),
    url(r'^harvesters/registry/all/metadataPrefix', admin_ajax.all_metadata_prefix,
        name='core_oaipmh_harvester_app_all_metadata_prefix'),
    url(r'^harvesters/registry/get/data', admin_ajax.get_data,
        name='core_oaipmh_harvester_app_get_data'),
    url(r'^harvesters/build/download/data', admin_ajax.download_xml_build_req,
        name='core_oaipmh_harvester_app_download_xml_build_req'),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
