""" Test forms from `views.admin.forms`.
"""
from unittest.case import TestCase

from core_oaipmh_harvester_app.views.admin.forms import RequestForm
from django.test import override_settings


class TestRequestForm(TestCase):
    """Test Request Form"""

    @override_settings(BOOTSTRAP_VERSION="4.6.2")
    def test_request_form_bootstrap_v4(self):
        """test_request_form_bootstrap_v4

        Returns:

        """
        # Arrange # Act
        form = RequestForm()

        # Assert
        self.assertEquals(
            form.fields["data_provider"].widget.attrs["class"], "form-control"
        )
        self.assertEquals(
            form.fields["verb"].widget.attrs["class"], "form-control"
        )
        self.assertEquals(
            form.fields["set"].widget.attrs["class"], "form-control"
        )
        self.assertEquals(
            form.fields["metadata_prefix"].widget.attrs["class"],
            "form-control",
        )

    @override_settings(BOOTSTRAP_VERSION="5.1.3")
    def test_request_form_bootstrap_v5(self):
        """test_request_form_bootstrap_v5

        Returns:

        """
        # Arrange # Act
        form = RequestForm()

        # Assert
        self.assertEquals(
            form.fields["data_provider"].widget.attrs["class"], "form-select"
        )
        self.assertEquals(
            form.fields["verb"].widget.attrs["class"], "form-select"
        )
        self.assertEquals(
            form.fields["set"].widget.attrs["class"], "form-select"
        )
        self.assertEquals(
            form.fields["metadata_prefix"].widget.attrs["class"], "form-select"
        )
