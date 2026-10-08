"""Integration tests for `core_oaipmh_harvester_app.components.oai_verbs.api`"""

from django.test import TestCase
from rest_framework import status

from core_oaipmh_common_app.commons import exceptions as oai_pmh_exceptions
from core_oaipmh_harvester_app.components.oai_verbs import api as oai_verbs_api
from tests.mocks import MockProviderResponse, MockRequest
from unittest.mock import patch

REGISTRY_URL = "http://registry.example.com/oai_pmh/server/?verb=GetRecord"
SAME_ORIGIN_REGISTRY_URL = (
    "http://127.0.0.1:8000/oai_pmh/server/?verb=GetRecord"
)


class TestGetDataDoesNotLeakSessionCookieCrossOrigin(TestCase):
    """Tests to ensure `get_data` function does not forward the staff session cookie to a
    cross-origin registry URL.
    """

    @patch.object(oai_verbs_api, "send_get_request")
    @patch.object(oai_verbs_api, "identify")
    def test_get_data_does_not_forward_session_cookie_cross_origin(
        self, mock_identify, mock_send_get_request
    ):
        """test_get_data_does_not_forward_session_cookie_cross_origin"""
        mock_identify.return_value = ({}, status.HTTP_200_OK)
        mock_send_get_request.side_effect = MockProviderResponse()
        request = MockRequest(session_key=MockProviderResponse.session_id_key)

        try:
            oai_verbs_api.get_data(REGISTRY_URL, request=request)
        except oai_pmh_exceptions.OAIAPIException:
            pass

        sent_cookies = mock_send_get_request.call_args.kwargs.get("cookies")
        self.assertFalse(
            sent_cookies and sent_cookies.get("sessionid"),
            "get_data forwarded the staff session cookie to a cross-origin registry URL",
        )

    @patch.object(oai_verbs_api, "send_get_request")
    @patch.object(oai_verbs_api, "identify")
    def test_get_data_cannot_retrieve_non_public_record_cross_origin(
        self, mock_identify, mock_send_get_request
    ):
        """test_get_data_cannot_retrieve_non_public_record_cross_origin"""
        mock_identify.return_value = ({}, status.HTTP_200_OK)
        mock_send_get_request.side_effect = MockProviderResponse()
        request = MockRequest(session_key=MockProviderResponse.session_id_key)

        with self.assertRaises(oai_pmh_exceptions.OAIAPIException):
            oai_verbs_api.get_data(REGISTRY_URL, request=request)


class TestGetDataStillWorksSameOrigin(TestCase):
    """Regression tests for the self-harvesting behavior: same-origin requests (e.g.
    harvesting your own instance) must still forward the session cookie and must still be
    able to retrieve non-public records.
    """

    @patch.object(oai_verbs_api, "send_get_request")
    @patch.object(oai_verbs_api, "identify")
    def test_get_data_still_forwards_session_cookie_same_origin(
        self, mock_identify, mock_send_get_request
    ):
        """test_get_data_still_forwards_session_cookie_same_origin"""
        mock_identify.return_value = ({}, status.HTTP_200_OK)
        mock_send_get_request.side_effect = MockProviderResponse()
        request = MockRequest(session_key=MockProviderResponse.session_id_key)

        oai_verbs_api.get_data(SAME_ORIGIN_REGISTRY_URL, request=request)

        sent_cookies = mock_send_get_request.call_args.kwargs.get("cookies")
        self.assertEqual(
            sent_cookies,
            {"sessionid": MockProviderResponse.session_id_key},
            "get_data no longer forwards the staff session cookie to a same-origin registry URL",
        )

    @patch.object(oai_verbs_api, "send_get_request")
    @patch.object(oai_verbs_api, "identify")
    def test_get_data_can_still_retrieve_non_public_record_same_origin(
        self, mock_identify, mock_send_get_request
    ):
        """test_get_data_can_still_retrieve_non_public_record_same_origin"""
        mock_identify.return_value = ({}, status.HTTP_200_OK)
        mock_send_get_request.side_effect = MockProviderResponse()
        request = MockRequest(session_key=MockProviderResponse.session_id_key)

        response = oai_verbs_api.get_data(
            SAME_ORIGIN_REGISTRY_URL, request=request
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MockProviderResponse.success_data)
