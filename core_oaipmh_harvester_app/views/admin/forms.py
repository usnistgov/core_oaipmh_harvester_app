from django import forms
from django.core.validators import MinValueValidator
from mongodbforms import DocumentForm

import core_oaipmh_harvester_app.components.oai_registry.api as oai_registry_api
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry

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
                                      widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '60'}),
                                      min_value=0)
    harvest = forms.BooleanField(label='Enable automatic harvesting', required=False, initial=True,
                                 widget=forms.CheckboxInput(attrs={'class': 'cmn-toggle cmn-toggle-round',
                                                                   'visibility': 'hidden'}))


class EditRegistryForm(DocumentForm):
    harvest_rate = forms.IntegerField(label='Harvest Rate (seconds)',
                                      validators=[MinValueValidator(0)],
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    harvest = forms.BooleanField(label='Enable automatic harvesting', initial=True, required=False,
                                 widget=forms.CheckboxInput())

    class Meta:
        document = OaiRegistry
        fields = ['harvest_rate', 'harvest']


class FormDataModelChoiceFieldMF(forms.ModelMultipleChoiceField):
    # Used to return the prefix of the metadata format
    def label_from_instance(self, obj):
        return obj.metadata_prefix


class FormDataModelChoiceFieldSet(forms.ModelMultipleChoiceField):
    # Used to return the name of the set
    def label_from_instance(self, obj):
        return obj.set_name


class EditHarvestRegistryForm(DocumentForm):
    """
        A EditHarvestRegistryForm form
    """
    metadata_formats = FormDataModelChoiceFieldMF(label='Metadata Formats', queryset=None,
                                                  required=False,
                                                  widget=forms.CheckboxSelectMultiple())
    sets = FormDataModelChoiceFieldSet(label='Sets', queryset=None, required=False,
                                       widget=forms.CheckboxSelectMultiple())

    class Meta:
        document = OaiRegistry
        fields = ['metadata_formats', 'sets']

    def __init__(self, *args, **kwargs):
        if all(x in kwargs for x in ['metadata_formats', 'sets']):
            metadata_formats = kwargs.pop('metadata_formats')
            sets = kwargs.pop('sets')
            super(EditHarvestRegistryForm, self).__init__(*args, **kwargs)
            self.fields['metadata_formats'].queryset = metadata_formats
            self.fields['sets'].queryset = sets


class RequestForm(forms.Form):
    """
        A request form
    """
    data_provider = forms.ChoiceField(label='Data Provider', choices=[], required=False,
                                      widget=forms.Select(attrs={"class": "form-control"}))
    verb = forms.ChoiceField(label='Verb', choices=VERBS, required=False,
                             widget=forms.Select(attrs={"class": "form-control"}))
    set = forms.ChoiceField(label='Set', choices=[], required=False,
                            widget=forms.Select(attrs={'disabled': 'true',
                                                       "class": "form-control"}))
    identifiers = forms.CharField(label='Identifier', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    metadata_prefix = forms.ChoiceField(label='Metadata Prefix', choices=[], required=False,
                                        widget=forms.Select(attrs={'disabled': 'true',
                                                                   "class": "form-control"}))
    From = forms.CharField(label='From', required=False,
                           widget=forms.DateInput(attrs={'data-date-format': 'yyyy-mm-ddThh:ii:00Z',
                                                         'class': 'form-control',
                                                         'style': 'width:160px'}))
    until = forms.CharField(label='Until', required=False,
                            widget=forms.DateInput(attrs={'data-date-format': 'yyyy-mm-ddThh:ii:00Z',
                                                          'class': 'form-control',
                                                          'style': 'width:160px'}))
    resumption_token = forms.CharField(label='Resumption Token', required=False,
                                       widget=forms.TextInput(attrs={'class': 'form-control',
                                                                     'style': 'width:198px;height:30px'}))

    def __init__(self):
        super(RequestForm, self).__init__()
        self.data_providers = []
        self.data_providers.append(('0', 'Pick one'))
        self.fields['metadata_prefix'].choices = self.data_providers
        self.fields['set'].choices = self.data_providers
        for o in oai_registry_api.get_all_activated_registry():
            self.data_providers.append((str(o.id)+'|'+o.url, str(o.name.encode('utf8'))))
        self.fields['data_provider'].choices = self.data_providers
