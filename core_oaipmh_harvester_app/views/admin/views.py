""" Admin views
"""

from django.contrib.admin.views.decorators import staff_member_required

from core_main_app.utils.rendering import admin_render
import core_oaipmh_harvester_app.components.oai_registry.api as oai_registry_api
from core_oaipmh_harvester_app.views.admin.ajax import EditRegistryView
from core_oaipmh_harvester_app.views.admin.forms import AddRegistryForm, RequestForm


@staff_member_required
def request_builder_view(request):
    """request_builder_view

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/"
                "request_builder/init.js",
                "is_raw": False,
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/"
                "request_builder/submit.js",
                "is_raw": False,
            },
            {
                "path": "core_oaipmh_harvester_app/libs/"
                "bootstrap-datetimepicker/1.0/js/"
                "bootstrap-datetimepicker.js",
                "is_raw": False,
            },
            {"path": "core_main_app/common/js/XMLTree.js", "is_raw": True},
        ],
        "css": [
            "core_oaipmh_harvester_app/libs/bootstrap-datetimepicker/1.0/css/"
            "bootstrap-datetimepicker.css",
            "core_oaipmh_harvester_app/admin/css/registries/request_builder/"
            "main.css",
            "core_main_app/common/css/XMLTree.css",
        ],
    }

    context = {"request_form": RequestForm()}

    return admin_render(
        request,
        "core_oaipmh_harvester_app/admin/registries/request_builder.html",
        context=context,
        assets=assets,
    )


@staff_member_required
def registries_view(request):
    """registries_view

    Args:
        request:

    Returns:

    """
    modals = [
        "core_oaipmh_harvester_app/admin/registries/list/modals/view_registry.html",
        "core_oaipmh_harvester_app/admin/registries/list/modals/add_registry.html",
        "core_oaipmh_harvester_app/admin/registries/list/modals/deactivate_registry.html",
        "core_oaipmh_harvester_app/admin/registries/list/modals/delete_registry.html",
        EditRegistryView.get_modal_html_path(),
    ]

    assets = {
        "js": [
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/view_registry.js",
                "is_raw": False,
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/add_registry.js",
                "is_raw": False,
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/deactivate_registry.js",
                "is_raw": False,
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/activate_registry.js",
                "is_raw": False,
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/delete_registry.js",
                "is_raw": False,
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/check_registry.js",
                "is_raw": False,
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/update_registry.js",
                "is_raw": False,
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/harvest_registry.js",
                "is_raw": False,
            },
            {
                "path": "core_oaipmh_harvester_app/admin/js/registries/list/modals/refresh.js",
                "is_raw": False,
            },
            EditRegistryView.get_modal_js_path(),
        ],
        "css": [
            "core_oaipmh_harvester_app/admin/css/registries/list/modals/view_registry.css",
            "core_oaipmh_harvester_app/admin/css/registries/list/modals/edit_harvest_registry.css",
        ],
    }

    context = {
        "registries": oai_registry_api.get_all(),
        "add_registry_form": AddRegistryForm(),
    }

    return admin_render(
        request,
        "core_oaipmh_harvester_app/admin/registries/list.html",
        modals=modals,
        assets=assets,
        context=context,
    )
