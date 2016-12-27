"""
Url router for the administration site
"""
from django.contrib import admin
from django.conf.urls import url

from views.admin import views as admin_views, ajax as admin_ajax

admin_urls = [
    url(r'^harvesters/builder', admin_views.request_builder_view,
        name='core_oaipmh_harvester_app_request_builder'),
    url(r'^harvesters/list', admin_views.registries_view,
        name='core_oaipmh_harvester_app_registries'),
    url(r'^harvesters/config', admin_views.local_configuration_view,
        name='core_oaipmh_harvester_app_local_configuration'),
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
    url(r'^harvesters/registry/edit/harvest', admin_ajax.edit_harvest_registry,
        name='core_oaipmh_harvester_app_edit_harvest_registry'),
    url(r'^harvesters/registry/edit', admin_ajax.edit_registry,
        name='core_oaipmh_harvester_app_edit_registry'),
    url(r'^harvesters/registry/view', admin_ajax.view_registry,
        name='core_oaipmh_harvester_app_view_registry'),
    url(r'^harvesters/registry/update', admin_ajax.update_registry,
        name='core_oaipmh_harvester_app_update_registry'),
    url(r'^harvesters/registry/harvest', admin_ajax.harvest_registry,
        name='core_oaipmh_harvester_app_harvest_registry'),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
