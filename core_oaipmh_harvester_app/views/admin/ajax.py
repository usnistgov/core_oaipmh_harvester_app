""" OAI pmh havester Ajax file
"""
from os.path import join

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.utils import formats
from django.utils.html import escape
from io import StringIO
from rest_framework import status
from wsgiref.util import FileWrapper

import core_oaipmh_harvester_app.components.oai_harvester_metadata_format.api as oai_metadata_format_api
import core_oaipmh_harvester_app.components.oai_harvester_set.api as oai_set_api
import core_oaipmh_harvester_app.components.oai_identify.api as oai_identify_api
import core_oaipmh_harvester_app.components.oai_record.api as oai_record_api
import core_oaipmh_harvester_app.components.oai_registry.api as oai_registry_api
import core_oaipmh_harvester_app.components.oai_verbs.api as oai_verb_api
from core_main_app.utils.datetime import datetime_now
from core_main_app.utils.xml import xsl_transform
from core_main_app.views.common.ajax import EditObjectModalView
from core_oaipmh_harvester_app.components.oai_registry.models import (
    OaiRegistry,
)
from core_oaipmh_harvester_app.views.admin.forms import (
    AddRegistryForm,
    EditRegistryForm,
    EditHarvestRegistryForm,
)
from xml_utils.xsd_tree.xsd_tree import XSDTree

logger = logging.getLogger(__name__)


@staff_member_required
def add_registry(request):
    """Add a registry.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == "POST":
            form = AddRegistryForm(request.POST)
            if form.is_valid():
                url = form.cleaned_data.get("url")
                harvest_rate = form.cleaned_data.get("harvest_rate")
                harvest = form.cleaned_data.get("harvest")
                oai_registry_api.add_registry_by_url(
                    url, harvest_rate, harvest, request=request
                )
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Data provider added with success.",
                )
            else:
                return HttpResponseBadRequest("Please enter a valid URL.")
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )

    return HttpResponse(json.dumps({}), content_type="application/javascript")


@staff_member_required
def deactivate_registry(request):
    """Deactivate a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry = oai_registry_api.get_by_id(request.GET["id"])
        registry.is_activated = False
        oai_registry_api.upsert(registry)
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )

    return HttpResponse(json.dumps({}), content_type="application/javascript")


@staff_member_required
def activate_registry(request):
    """Activate a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry = oai_registry_api.get_by_id(request.GET["id"])
        registry.is_activated = True
        oai_registry_api.upsert(registry)
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )

    return HttpResponse(json.dumps({}), content_type="application/javascript")


@staff_member_required
def delete_registry(request):
    """Delete a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry = oai_registry_api.get_by_id(request.GET["id"])
        oai_registry_api.delete(registry)
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )

    return HttpResponse(json.dumps({}), content_type="application/javascript")


@staff_member_required
def check_registry(request):
    """Check the availability of a registry.
    Args:
        request:

    Returns:

    """
    try:
        req, status_code = oai_verb_api.identify(request.GET["url"])
        is_available = status_code == status.HTTP_200_OK
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )

    return HttpResponse(
        json.dumps({"is_available": is_available}),
        content_type="application/javascript",
    )


class EditRegistryView(EditObjectModalView):
    """Edit Registry View"""

    form_class = EditRegistryForm
    model = OaiRegistry
    success_url = reverse_lazy(
        "core-admin:core_oaipmh_harvester_app_registries"
    )
    success_message = "Data provider edited with success."

    def _save(self, form):
        # Save treatment.
        try:
            oai_registry_api.upsert(self.object)
        except Exception as exception:
            form.add_error(None, str(exception))


@staff_member_required
def view_registry(request):
    """View a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry_id = request.GET["id"]
        template = loader.get_template(
            "core_oaipmh_harvester_app/admin/registries/list/modals/view_registry_table.html"
        )
        context = {
            "registry": oai_registry_api.get_by_id(registry_id),
            "identify": oai_identify_api.get_by_registry_id(registry_id),
            "metadata_formats": oai_metadata_format_api.get_all_by_registry_id(
                registry_id
            ),
            "sets": oai_set_api.get_all_by_registry_id(registry_id),
            "nb_records": oai_record_api.get_count_by_registry_id(
                registry_id, request.user
            ),
        }
        return HttpResponse(
            json.dumps({"template": template.render(context)}),
            content_type="application/javascript",
        )
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )


class EditHarvestRegistryView(EditObjectModalView):
    """Edit Harvest Registry View"""

    template_name = "core_oaipmh_harvester_app/admin/registries/list/modals/edit_harvest_registry_form.html"
    form_class = EditHarvestRegistryForm
    model = OaiRegistry
    success_url = reverse_lazy(
        "core-admin:core_oaipmh_harvester_app_registries"
    )
    success_message = "Data provider edited with success."
    metadata_formats = None
    sets = None

    def _save(self, form):
        # Save treatment.
        try:
            registry_id = self.object.id
            metadata_formats = form.cleaned_data.get("metadata_formats", [])
            sets = form.cleaned_data.get("sets", [])
            oai_metadata_format_api.update_for_all_harvest_by_list_ids(
                oai_metadata_format_api.get_all_by_registry_id(
                    registry_id
                ).values_list("id", flat=True),
                False,
            )
            oai_metadata_format_api.update_for_all_harvest_by_list_ids(
                metadata_formats.values_list("id", flat=True), True
            )
            oai_set_api.update_for_all_harvest_by_list_ids(
                oai_set_api.get_all_by_registry_id(registry_id).values_list(
                    "id", flat=True
                ),
                False,
            )
            oai_set_api.update_for_all_harvest_by_list_ids(
                sets.values_list("id", flat=True), True
            )
        except Exception as exception:
            form.add_error(None, str(exception))

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
        arguments."""
        # grab the current set of form #kwargs
        kwargs = super().get_form_kwargs()
        # Update the kwargs
        kwargs["metadata_formats"] = self.metadata_formats
        kwargs["sets"] = self.sets

        return kwargs

    def get_initial(self):
        """get_initial

        Returns:
        """
        initial = super().get_initial()
        self.metadata_formats = oai_metadata_format_api.get_all_by_registry_id(
            self.object.id
        )
        self.sets = oai_set_api.get_all_by_registry_id(self.object.id)
        initial["metadata_formats"] = [
            mf.id for mf in self.metadata_formats if mf.harvest
        ]
        initial["sets"] = [set_.id for set_ in self.sets if set_.harvest]

        return initial


@staff_member_required
def update_registry(request):
    """Update information of a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry = oai_registry_api.get_by_id(request.GET["id"])
        oai_registry_api.update_registry_info(registry, request=request)

        return HttpResponse(
            json.dumps({}), content_type="application/javascript"
        )
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )


@staff_member_required
def check_update_registry(request):
    """Check if a registry is updating.
    Args:
        request:

    Returns:

    """
    if request.method == "GET":
        try:
            update_info = []
            registries = oai_registry_api.get_all()
            for registry in registries:
                last_update = None
                # Check if the registry has a last_update and try to format it.
                if registry.last_update is not None:
                    try:
                        last_update = formats.date_format(
                            registry.last_update, "DATETIME_FORMAT"
                        )
                    except Exception as exception:
                        logger.warning(
                            "check_update_registry threw an exception: {0}".format(
                                str(exception)
                            )
                        )

                result_json = {
                    "registry_id": str(registry.id),
                    "is_updating": registry.is_updating,
                    "name": registry.name,
                    "last_update": last_update,
                }

                update_info.append(result_json)

            return HttpResponse(
                json.dumps(update_info), content_type="application/javascript"
            )
        except Exception as exception:
            return HttpResponseBadRequest(
                escape(str(exception)), content_type="application/javascript"
            )


@staff_member_required
def harvest_registry(request):
    """Harvest a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry = oai_registry_api.get_by_id(request.GET["id"])
        oai_registry_api.harvest_registry(registry)

        return HttpResponse(
            json.dumps({}), content_type="application/javascript"
        )
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )


@staff_member_required
def check_harvest_registry(request):
    """Check if a registry is harvesting.
    Args:
        request:

    Returns:

    """
    if request.method == "GET":
        try:
            update_info = []
            registries = oai_registry_api.get_all()
            for registry in registries:
                result_json = {
                    "registry_id": str(registry.id),
                    "is_harvesting": registry.is_harvesting,
                }
                update_info.append(result_json)

            return HttpResponse(
                json.dumps(update_info), content_type="application/javascript"
            )
        except Exception:
            return HttpResponseBadRequest(
                "An error occurred. Please contact your administrator."
            )


@staff_member_required
def all_sets(request):
    """Returns all the sets of a registry.
    Args:
        request:

    Returns:
        List of set's name

    """
    try:
        sets = []
        registry_sets = oai_set_api.get_all_by_registry_id(
            request.GET["id"], "set_name"
        )
        for set_ in registry_sets:
            sets.append({"key": set_.set_name, "value": set_.set_spec})

        return HttpResponse(
            json.dumps(sets), content_type="application/javascript"
        )
    except Exception:
        return HttpResponseBadRequest(
            "An error occurred. Please contact your administrator."
        )


@staff_member_required
def all_metadata_prefix(request):
    """Returns all the sets of a registry
    Args:
        request:

    Returns:
        List of metadata prefix's name

    """
    try:
        metadata_prefixes = []
        metadata_formats = oai_metadata_format_api.get_all_by_registry_id(
            request.GET["id"], "metadata_prefix"
        )
        for format_ in metadata_formats:
            metadata_prefixes.append(format_.metadata_prefix)

        return HttpResponse(
            json.dumps(metadata_prefixes),
            content_type="application/javascript",
        )
    except Exception:
        return HttpResponseBadRequest(
            "An error occurred. Please contact your administrator."
        )


@staff_member_required
def get_data(request):
    """Perform an OAI-PMH request.
    Args:
        request:

    Returns:

    """
    url = request.GET["url"]
    args_url = json.loads(request.GET["args_url"])
    # Encode args for the Get request
    encoded_args = urllib.parse.urlencode(args_url)
    # Build the url
    url = url + "?" + encoded_args
    try:
        xml_string = oai_verb_api.get_data(url, request=request).data
        request.session["xmlStringOAIPMH"] = xml_string
        # loads XSLT
        xslt_path = finders.find(
            join("core_main_app", "common", "xsl", "xml2html.xsl")
        )
        # reads XSLT
        xslt_string = _read_file_content(xslt_path)
        # transform XML to HTML
        xml_to_html_string = xsl_transform(xml_string, xslt_string)
        content = {"message": xml_to_html_string}

        return HttpResponse(
            json.dumps(content), content_type="application/javascript"
        )
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )


@staff_member_required
def download_xml_build_req(request):
    """Download xml of the building request.
    Args:
        request:

    Returns:
        XML file to download.

    """
    if "xmlStringOAIPMH" not in request.session:
        return HttpResponseBadRequest(
            "An error occurred. Please reload the page and try again."
        )

    # We retrieve the XML file in session
    xml_string = request.session["xmlStringOAIPMH"]
    try:
        xml_tree = XSDTree.build_tree(xml_string)
        xml_string_encoded = XSDTree.tostring(xml_tree, pretty=True)
    except Exception:
        xml_string_encoded = xml_string
    # Get the date to append it to the file title
    i = datetime_now()
    title = "OAI_PMH_BUILD_REQ_%s_.xml" % i.isoformat()
    file_obj = StringIO(xml_string_encoded)
    # Return the XML file
    response = HttpResponse(
        FileWrapper(file_obj), content_type="application/xml"
    )
    response["Content-Disposition"] = "attachment; filename=" + title

    return response


def _read_file_content(file_path):
    """Reads the content of a file

    Args:
        file_path:

    Returns:

    """
    with open(file_path) as _file:
        file_content = _file.read()
        return file_content
