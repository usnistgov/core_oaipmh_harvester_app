"""
Url router for the administration site
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_main_app.admin import core_admin_site
from core_main_app.utils.admin_site.view_only_admin import ViewOnlyAdmin
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format_set.models import (
    OaiHarvesterMetadataFormatSet,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.views.admin import (
    views as admin_views,
    ajax as admin_ajax,
)

admin.site.register(OaiHarvesterMetadataFormat, ViewOnlyAdmin)
admin.site.register(OaiHarvesterMetadataFormatSet, ViewOnlyAdmin)
admin.site.register(OaiHarvesterSet, ViewOnlyAdmin)
admin.site.register(OaiIdentify, ViewOnlyAdmin)
admin.site.register(OaiRecord, ViewOnlyAdmin)
admin.site.register(OaiRegistry, ViewOnlyAdmin)

admin_urls = [
    re_path(
        r"^harvesters/builder",
        admin_views.request_builder_view,
        name="core_oaipmh_harvester_app_request_builder",
    ),
    re_path(
        r"^harvesters/list",
        admin_views.registries_view,
        name="core_oaipmh_harvester_app_registries",
    ),
    re_path(
        r"^harvesters/registry/add",
        admin_ajax.add_registry,
        name="core_oaipmh_harvester_app_add_registry",
    ),
    re_path(
        r"^harvesters/registry/deactivate",
        admin_ajax.deactivate_registry,
        name="core_oaipmh_harvester_app_deactivate_registry",
    ),
    re_path(
        r"^harvesters/registry/activate",
        admin_ajax.activate_registry,
        name="core_oaipmh_harvester_app_activate_registry",
    ),
    re_path(
        r"^harvesters/registry/delete",
        admin_ajax.delete_registry,
        name="core_oaipmh_harvester_app_delete_registry",
    ),
    re_path(
        r"^harvesters/registry/check/harvest",
        admin_ajax.check_harvest_registry,
        name="core_oaipmh_harvester_app_check_harvest_registry",
    ),
    re_path(
        r"^harvesters/registry/check/update",
        admin_ajax.check_update_registry,
        name="core_oaipmh_harvester_app_check_update_registry",
    ),
    re_path(
        r"^harvesters/registry/check",
        admin_ajax.check_registry,
        name="core_oaipmh_harvester_app_check_registry",
    ),
    re_path(
        r"^harvesters/registry/harvest/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditHarvestRegistryView.as_view()),
        name="core_oaipmh_harvester_app_edit_harvest_registry",
    ),
    re_path(
        r"^harvesters/registry/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditRegistryView.as_view()),
        name="core_oaipmh_harvester_app_edit_registry",
    ),
    re_path(
        r"^harvesters/registry/view",
        admin_ajax.view_registry,
        name="core_oaipmh_harvester_app_view_registry",
    ),
    re_path(
        r"^harvesters/registry/update",
        admin_ajax.update_registry,
        name="core_oaipmh_harvester_app_update_registry",
    ),
    re_path(
        r"^harvesters/registry/harvest",
        admin_ajax.harvest_registry,
        name="core_oaipmh_harvester_app_harvest_registry",
    ),
    re_path(
        r"^harvesters/registry/all/sets",
        admin_ajax.all_sets,
        name="core_oaipmh_harvester_app_all_sets",
    ),
    re_path(
        r"^harvesters/registry/all/metadataPrefix",
        admin_ajax.all_metadata_prefix,
        name="core_oaipmh_harvester_app_all_metadata_prefix",
    ),
    re_path(
        r"^harvesters/registry/get/data",
        admin_ajax.get_data,
        name="core_oaipmh_harvester_app_get_data",
    ),
    re_path(
        r"^harvesters/build/download/data",
        admin_ajax.download_xml_build_req,
        name="core_oaipmh_harvester_app_download_xml_build_req",
    ),
]

urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
