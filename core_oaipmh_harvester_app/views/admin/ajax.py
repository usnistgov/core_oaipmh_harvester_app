from django.http.response import HttpResponseBadRequest, HttpResponse
from core_oaipmh_harvester_app.views.admin.forms import AddRegistryForm, EditRegistryForm, EditHarvestRegistryForm
import core_oaipmh_harvester_app.components.oai_registry.api as oai_registry_api
import core_oaipmh_harvester_app.components.oai_harvester_metadata_format.api as oai_metadata_format_api
import core_oaipmh_harvester_app.components.oai_identify.api as oai_identify_api
import core_oaipmh_harvester_app.components.oai_harvester_set.api as oai_set_api
import core_oaipmh_harvester_app.components.oai_record.api as oai_record_api
import core_oaipmh_harvester_app.components.oai_verbs.api as oai_verb_api
from django.contrib import messages
import json
from rest_framework import status
from django.template import loader


def add_registry(request):
    """ Add a registry.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            form = AddRegistryForm(request.POST)
            if form.is_valid():
                url = request.POST.get('url')
                harvest_rate = request.POST.get('harvest_rate')
                harvest = request.POST.get('harvest') == 'on'
                oai_registry_api.add_registry_by_url(url, harvest_rate, harvest)
                messages.add_message(request, messages.SUCCESS, 'Data provider added with success.')
            else:
                return HttpResponseBadRequest('Bad entries. Please enter a valid URL and a positive integer')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def deactivate_registry(request):
    """ Deactivate a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry = oai_registry_api.get_by_id(request.GET['id'])
        registry.is_activated = False
        oai_registry_api.upsert(registry)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def activate_registry(request):
    """ Activate a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry = oai_registry_api.get_by_id(request.GET['id'])
        registry.is_activated = True
        oai_registry_api.upsert(registry)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def delete_registry(request):
    """ Delete a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry = oai_registry_api.get_by_id(request.GET['id'])
        oai_registry_api.delete(registry)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def check_registry(request):
    """ Check the availability of a registry.
    Args:
        request:

    Returns:

    """
    try:
        req, status_code = oai_verb_api.identify(request.GET['url'])
        is_available = status_code == status.HTTP_200_OK
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({'is_available': is_available}), content_type='application/javascript')


def edit_registry(request):
    """ Edit a registry.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            form = EditRegistryForm(request.POST)
            if form.is_valid():
                registry = oai_registry_api.get_by_id(request.POST['id'])
                registry.harvest_rate = request.POST.get('harvest_rate')
                registry.harvest = request.POST.get('harvest') == 'on'
                oai_registry_api.upsert(registry)
                messages.add_message(request, messages.SUCCESS, 'Data provider edited with success.')

                return HttpResponse(json.dumps({}), content_type='application/javascript')
            else:
                return HttpResponseBadRequest('Bad entries. Please enter a positive integer')
        elif request.method == 'GET':
            registry = oai_registry_api.get_by_id(request.GET['id'])
            data = {'id': registry.id, 'harvest_rate': registry.harvest_rate, 'harvest': registry.harvest}
            edit_registry_form = EditRegistryForm(data)
            template_name = 'core_oaipmh_harvester_app/admin/registries/list/modals/edit_registry_form.html'
            context = {
                "edit_registry_form": edit_registry_form
            }

            return HttpResponse(json.dumps({'template': loader.render_to_string(template_name, context)}),
                                'application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def view_registry(request):
    """ View a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry_id = request.GET['id']
        template = loader.\
            get_template('core_oaipmh_harvester_app/admin/registries/list/modals/view_registry_table.html')
        context = {
            'registry': oai_registry_api.get_by_id(registry_id),
            'identify': oai_identify_api.get_by_registry_id(registry_id),
            'metadata_formats': oai_metadata_format_api.get_all_by_registry_id(registry_id),
            'sets': oai_set_api.get_all_by_registry_id(registry_id),
            'nb_records': oai_record_api.get_count_by_registry_id(registry_id),
        }
        return HttpResponse(json.dumps({'template': template.render(context)}),
                            content_type='application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def edit_harvest_registry(request):
    """ Edit the harvesting of a registry.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            metadata_formats = request.POST.getlist('metadata_formats', [])
            sets = request.POST.getlist('sets', [])
            oai_metadata_format_api.\
                update_for_all_harvest_by_list_ids(oai_metadata_format_api.get_all_by_registry_id(id).values_list('id'),
                                                   False)
            oai_metadata_format_api.update_for_all_harvest_by_list_ids(metadata_formats, True)
            oai_set_api.update_for_all_harvest_by_list_ids(oai_set_api.get_all_by_registry_id(id).values_list('id'),
                                                           False)
            oai_set_api.update_for_all_harvest_by_list_ids(sets, True)
            messages.add_message(request, messages.SUCCESS, 'Data provider edited with success.')

            return HttpResponse(json.dumps({}), content_type='application/javascript')
        elif request.method == 'GET':
            registry_id = request.GET['id']
            edit_harvest_registry_form = EditHarvestRegistryForm(id=registry_id)
            template_name = 'core_oaipmh_harvester_app/admin/registries/list/modals/edit_harvest_registry_form.html'
            context = {
                'edit_harvest_registry_form': edit_harvest_registry_form,
            }

            return HttpResponse(json.dumps({'template': loader.render_to_string(template_name, context)}),
                                'application/javascript')
    except Exception, e:
            return HttpResponseBadRequest(e.message, content_type='application/javascript')


def update_registry(request):
    """ Update information of a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry = oai_registry_api.get_by_id(request.GET['id'])
        oai_registry_api.update_registry_info(registry)

        return HttpResponse(json.dumps({}), content_type='application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def check_update_registry(request):
    """ Check if a registry is updating.
    Args:
        request:

    Returns:

    """
    if request.method == 'GET':
        try:
            update_info = []
            registries = oai_registry_api.get_all()
            for registry in registries:
                result_json = {}
                result_json['registry_id'] = str(registry.id)
                result_json['is_updating'] = registry.is_updating
                result_json['name'] = registry.name
                update_info.append(result_json)

            return HttpResponse(json.dumps(update_info), content_type='application/javascript')
        except Exception as e:
            return HttpResponseBadRequest('An error occurred. Please contact your administrator.')


def harvest_registry(request):
    """ Harvest a registry.
    Args:
        request:

    Returns:

    """
    try:
        registry = oai_registry_api.get_by_id(request.GET['id'])
        # TODO: Create harvest_registry in oai_registry_api
        # oai_registry_api.harvest_registry(registry)

        return HttpResponse(json.dumps({}), content_type='application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def check_harvest_registry(request):
    """ Check if a registry is harvesting.
    Args:
        request:

    Returns:

    """
    if request.method == 'GET':
        try:
            update_info = []
            registries = oai_registry_api.get_all()
            for registry in registries:
                result_json = {}
                result_json['registry_id'] = str(registry.id)
                result_json['is_harvesting'] = registry.is_harvesting
                update_info.append(result_json)

            return HttpResponse(json.dumps(update_info), content_type='application/javascript')
        except Exception as e:
            return HttpResponseBadRequest('An error occurred. Please contact your administrator.')