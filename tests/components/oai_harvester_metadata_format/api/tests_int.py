"""Integration tests for `core_oaipmh_harvester_app.components.oai_harvester_metadata_format.api`"""

from unittest.mock import patch

from django.test import TestCase

from core_main_app.commons import exceptions
from core_main_app.components.template import api as api_template
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import (
    api as harvester_metadata_format_api,
)
from tests.mocks import MockMetadataFormat, MockProviderResponse, MockRequest

SCHEMA_URL = "http://registry.example.com/rest/template/download/private.xsd"
SAME_ORIGIN_SCHEMA_URL = (
    "http://127.0.0.1:8000/rest/template/download/private.xsd"
)


class TestInitSchemaInfoDoesNotLeakSessionCookieCrossOrigin(TestCase):
    """Integration tests to verify `init_schema_info` does not forward the staff session
    cookie to a cross-origin schema URL."""

    @patch.object(api_template, "get_all_accessible_by_hash")
    @patch.object(harvester_metadata_format_api, "send_get_request")
    def test_init_schema_info_does_not_forward_session_cookie_cross_origin(
        self, mock_send_get_request, mock_get_all_by_hash
    ):
        """test_init_schema_info_does_not_forward_session_cookie_cross_origin"""
        mock_send_get_request.side_effect = MockProviderResponse()
        mock_get_all_by_hash.return_value = []
        metadata_format = MockMetadataFormat(SCHEMA_URL)
        request = MockRequest(session_key=MockProviderResponse.session_id_key)

        try:
            harvester_metadata_format_api.init_schema_info(
                metadata_format, request=request
            )
        except exceptions.ApiError:
            pass

        sent_cookies = mock_send_get_request.call_args.kwargs.get("cookies")
        self.assertFalse(
            sent_cookies and sent_cookies.get("sessionid"),
            "init_schema_info forwarded the staff session cookie to a cross-origin schema URL",
        )

    @patch.object(api_template, "get_all_accessible_by_hash")
    @patch.object(harvester_metadata_format_api, "send_get_request")
    def test_init_schema_info_cannot_retrieve_non_public_schema_cross_origin(
        self, mock_send_get_request, mock_get_all_by_hash
    ):
        """test_init_schema_info_cannot_retrieve_non_public_schema_cross_origin"""
        mock_send_get_request.side_effect = MockProviderResponse()
        mock_get_all_by_hash.return_value = []
        metadata_format = MockMetadataFormat(SCHEMA_URL)
        request = MockRequest(session_key=MockProviderResponse.session_id_key)

        with self.assertRaises(exceptions.ApiError):
            harvester_metadata_format_api.init_schema_info(
                metadata_format, request=request
            )


class TestInitSchemaInfoStillWorksSameOrigin(TestCase):
    """Regression test to check the self-harvesting behavior: same-origin requests (e.g.
    a schema hosted on this instance itself) must still forward the session cookie and
    must still be able to retrieve non-public schemas."""

    @patch.object(api_template, "get_all_accessible_by_hash")
    @patch.object(harvester_metadata_format_api, "send_get_request")
    def test_init_schema_info_still_forwards_session_cookie_same_origin(
        self, mock_send_get_request, mock_get_all_by_hash
    ):
        """ "test_init_schema_info_still_forwards_session_cookie_same_origin"""
        mock_send_get_request.side_effect = MockProviderResponse()
        mock_get_all_by_hash.return_value = []
        metadata_format = MockMetadataFormat(SAME_ORIGIN_SCHEMA_URL)
        request = MockRequest(session_key=MockProviderResponse.session_id_key)

        harvester_metadata_format_api.init_schema_info(
            metadata_format, request=request
        )

        sent_cookies = mock_send_get_request.call_args.kwargs.get("cookies")
        self.assertEqual(
            sent_cookies,
            {"sessionid": MockProviderResponse.session_id_key},
            "init_schema_info no longer forwards the staff session cookie to a same-origin schema URL",
        )

    @patch.object(api_template, "get_all_accessible_by_hash")
    @patch.object(harvester_metadata_format_api, "send_get_request")
    def test_init_schema_info_can_still_retrieve_non_public_schema_same_origin(
        self, mock_send_get_request, mock_get_all_by_hash
    ):
        """test_init_schema_info_can_still_retrieve_non_public_schema_same_origin"""
        mock_send_get_request.side_effect = MockProviderResponse()
        mock_get_all_by_hash.return_value = []
        metadata_format = MockMetadataFormat(SAME_ORIGIN_SCHEMA_URL)
        request = MockRequest(session_key=MockProviderResponse.session_id_key)

        result = harvester_metadata_format_api.init_schema_info(
            metadata_format, request=request
        )
        self.assertEqual(result.xml_schema, MockProviderResponse.success_data)
