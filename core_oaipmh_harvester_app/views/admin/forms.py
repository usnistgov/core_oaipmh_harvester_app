from django import forms
from django.core.validators import MinValueValidator

import core_oaipmh_harvester_app.components.oai_registry.api as oai_registry_api
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry

VERBS = (
    ("0", "Pick one"),
    ("1", "Identify"),
    ("2", "Get Record"),
    ("3", "List Records"),
    ("4", "List Sets"),
    ("5", "List Identifiers"),
    ("6", "List Metadata Formats"),
)


class AddRegistryForm(forms.Form):
    """
    A registry form
    """

    name = forms.CharField(widget=forms.HiddenInput(), required=False)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    url = forms.URLField(
        label="Enter provider URL",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "https://remote-url.com:8080/oai/registry",
            }
        ),
    )
    harvest_rate = forms.IntegerField(
        label="Harvest Rate (seconds)",
        required=False,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "60"}),
        min_value=0,
    )
    harvest = forms.BooleanField(
        label="Enable automatic harvesting",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={"class": "cmn-toggle cmn-toggle-round", "visibility": "hidden"}
        ),
    )


class EditRegistryForm(forms.ModelForm):
    """Edit Registry Form"""

    harvest_rate = forms.IntegerField(
        label="Harvest Rate (seconds)",
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    harvest = forms.BooleanField(
        label="Enable automatic harvesting",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(),
    )

    class Meta:
        """Meta"""

        model = OaiRegistry
        fields = ["harvest_rate", "harvest"]


class FormDataModelChoiceFieldMF(forms.ModelMultipleChoiceField):
    """Form Data Model Choice Field MF"""

    # Used to return the prefix of the metadata format
    def label_from_instance(self, obj):
        """label_from_instance
        Args:
            obj:

        Returns:

        """
        return obj.metadata_prefix


class FormDataModelChoiceFieldSet(forms.ModelMultipleChoiceField):
    """Form Data Model Choice Field Set"""

    # Used to return the name of the set
    def label_from_instance(self, obj):
        """label_from_instance
        Args:
            obj:

        Returns:

        """
        return obj.set_name


class EditHarvestRegistryForm(forms.ModelForm):
    """
    A EditHarvestRegistryForm form
    """

    metadata_formats = FormDataModelChoiceFieldMF(
        label="Metadata Formats",
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    sets = FormDataModelChoiceFieldSet(
        label="Sets",
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        """Meta"""

        model = OaiRegistry
        fields = ["metadata_formats", "sets"]

    def __init__(self, *args, **kwargs):
        if all(x in kwargs for x in ["metadata_formats", "sets"]):
            metadata_formats = kwargs.pop("metadata_formats")
            sets = kwargs.pop("sets")
            super().__init__(*args, **kwargs)
            self.fields["metadata_formats"].queryset = metadata_formats
            self.fields["sets"].queryset = sets


class RequestForm(forms.Form):
    """Request builder form"""

    # Widget attributes
    default_attributes = {"class": "form-control"}
    disabled_attributes = {"class": "form-control", "disabled": "true"}
    date_attributes = {
        "data-date-format": "yyyy-mm-ddThh:ii:00Z",
        "class": "form-control",
        "style": "width:160px",
    }

    data_provider = forms.ChoiceField(
        label="Data Provider",
        choices=[],
        required=False,
        widget=forms.Select(attrs=default_attributes),
    )
    verb = forms.ChoiceField(
        label="Verb",
        choices=VERBS,
        required=False,
        widget=forms.Select(attrs=default_attributes),
    )
    set = forms.ChoiceField(
        label="Set",
        choices=[],
        required=False,
        widget=forms.Select(attrs=disabled_attributes),
    )
    identifier = forms.CharField(
        label="Identifier",
        required=False,
        widget=forms.TextInput(attrs=default_attributes),
    )
    metadata_prefix = forms.ChoiceField(
        label="Metadata Prefix",
        choices=[],
        required=False,
        widget=forms.Select(attrs=disabled_attributes),
    )
    from_date = forms.CharField(
        label="From", required=False, widget=forms.DateInput(attrs=date_attributes)
    )
    until_date = forms.CharField(
        label="Until", required=False, widget=forms.DateInput(attrs=date_attributes)
    )
    resumption_token = forms.CharField(
        label="Resumption Token",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def __init__(self):
        super().__init__()

        default_fields = [("0", "Pick one")]

        self.fields["metadata_prefix"].choices = default_fields
        self.fields["set"].choices = default_fields

        for registry in oai_registry_api.get_all_activated_registry():
            default_fields.append(
                ("%s|%s" % (str(registry.id), registry.url), str(registry.name))
            )

        self.fields["data_provider"].choices = default_fields
