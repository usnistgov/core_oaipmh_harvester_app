from django import forms
from django.core.validators import MinValueValidator
import core_oaipmh_harvester_app.components.oai_registry.api as oai_registry_api
import core_oaipmh_harvester_app.components.oai_harvester_metadata_format.api as oai_metadata_format_api
import core_oaipmh_harvester_app.components.oai_harvester_set.api as oai_set_api


VERBS = (('0', 'Pick one'),
         ('1', 'Identify'),
         ('2', 'Get Record'),
         ('3', 'List Records'),
         ('4', 'List Sets'),
         ('5', 'List Identifiers'),
         ('6', 'List Metadata Formats'))


class AddRegistryForm(forms.Form):
    """
        A registry form
    """
    name = forms.CharField(widget=forms.HiddenInput(), required=False)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    url = forms.URLField(label='Enter provider URL', required=True,
                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'https://remote-url.com:8080/oai/registry'}))
    harvest_rate = forms.IntegerField(label='Harvest Rate (seconds)', required=False, validators=[MinValueValidator(0)],
                                      widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '60'}))
    harvest = forms.BooleanField(label='Enable automatic harvesting', required=False, initial=True,
                                 widget=forms.CheckboxInput(attrs={'class': 'cmn-toggle cmn-toggle-round',
                                                                   'visibility': 'hidden'}))


class EditRegistryForm(forms.Form):
    """
        A registry update form
    """
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    harvest_rate = forms.IntegerField(label='Harvest Rate (seconds)', required=False, validators=[MinValueValidator(0)],
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    harvest = forms.BooleanField(label='Enable automatic harvesting', required=False, initial=True,
                                 widget=forms.CheckboxInput(attrs={'class': 'cmn-toggle cmn-toggle-round',
                                                                   'visibility': 'hidden'}))


class FormDataModelChoiceFieldMF(forms.ModelChoiceField):
    # Used to return the prefix of the metadata format
    def label_from_instance(self, obj):
        return obj.metadata_prefix


class FormDataModelChoiceFieldSet(forms.ModelChoiceField):
    # Used to return the name of the set
    def label_from_instance(self, obj):
        return obj.set_name


class EditHarvestRegistryForm(forms.Form):
    """
        A EditHarvestRegistryForm form
    """
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    metadata_formats = FormDataModelChoiceFieldMF(label='Metadata Formats', queryset=[], empty_label=None,
                                                  required=False,
                                                  widget=forms.CheckboxSelectMultiple(
                                                     attrs={'class': 'cmn-toggle cmn-toggle-round'}))
    sets = FormDataModelChoiceFieldSet(label='Sets', queryset=[], required=False, empty_label=None,
                                       widget=forms.CheckboxSelectMultiple(
                                           attrs={'class': 'cmn-toggle cmn-toggle-round'}))

    def __init__(self, *args, **kwargs):
        if 'id' in kwargs:
            registry_id = kwargs.pop('id')
            metadata_formats = oai_metadata_format_api.get_all_by_registry_id(registry_id)
            sets = oai_set_api.get_all_by_registry_id(registry_id)
            super(EditHarvestRegistryForm, self).__init__(*args, **kwargs)
            self.fields['id'].initial = registry_id
            self.fields['metadata_formats'].initial = [mf.id for mf in metadata_formats if mf.harvest]
            self.fields['metadata_formats'].queryset = metadata_formats
            self.fields['sets'].initial = [set_.id for set_ in sets if set_.harvest]
            self.fields['sets'].queryset = sets
