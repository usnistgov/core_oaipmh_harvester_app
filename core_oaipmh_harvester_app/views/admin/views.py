from django.contrib.admin.views.decorators import staff_member_required
from core_main_app.utils.rendering import admin_render
from core_oaipmh_harvester_app.views.admin.forms import AddRegistryForm, RequestForm
import core_oaipmh_harvester_app.components.oai_registry.api as oai_registry_api
from django.contrib.staticfiles import finders
from os.path import join


@staff_member_required
def request_builder_view(request):
    assets = {
        "js": [
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/request_builder/init.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/request_builder/populate.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/request_builder/submit.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/libs/bootstrap-datetimepicker/1.0/js/bootstrap-datetimepicker.js",
                "is_raw": False
            }
        ],
        "css": [
            "core_oaipmh_harvester_app/libs/bootstrap-datetimepicker/1.0/css/bootstrap-datetimepicker.css",
            "core_oaipmh_harvester_app/admin/css/registries/request_builder/main.css",
            "core_main_app/common/css/XMLTree.css"
        ]
    }

    context = {
        "request_form": RequestForm()
    }

    return admin_render(request, "core_oaipmh_harvester_app/admin/registries/request_builder.html", context=context,
                        assets=assets)


@staff_member_required
def registries_view(request):
    modals = [
        "core_oaipmh_harvester_app/admin/registries/list/modals/view_registry.html",
        "core_oaipmh_harvester_app/admin/registries/list/modals/add_registry.html",
        "core_oaipmh_harvester_app/admin/registries/list/modals/deactivate_registry.html",
        "core_oaipmh_harvester_app/admin/registries/list/modals/delete_registry.html",
        "core_oaipmh_harvester_app/admin/registries/list/modals/edit_registry.html",
        "core_oaipmh_harvester_app/admin/registries/list/modals/edit_harvest_registry.html"
    ]

    assets = {
        "js": [
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/view_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/add_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/deactivate_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/activate_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/delete_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/check_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/edit_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/edit_harvest_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/update_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/harvest_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/refresh.js",
                "is_raw": False
            },
        ],
        "css": [
            "core_oaipmh_harvester_app/admin/css/registries/list/modals/view_registry.css",
            "core_oaipmh_harvester_app/admin/css/registries/list/modals/edit_harvest_registry.css"
        ]
    }

    context = {
        "registries": oai_registry_api.get_all(),
        "add_registry_form": AddRegistryForm()
    }

    return admin_render(request, "core_oaipmh_harvester_app/admin/registries/list.html", modals=modals,
                        assets=assets, context=context)
