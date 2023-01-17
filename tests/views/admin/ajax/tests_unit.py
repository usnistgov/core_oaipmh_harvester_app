""" Unit tests for admin AJAX views
"""
from unittest.mock import patch

from django.test.testcases import TestCase
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_oaipmh_harvester_app.views.admin.ajax import download_xml_build_req
from tests.mocks import MockRequest


class TestDownloadXmlBuildReq(TestCase):
    """Tests for download_xml_build_req function"""

    def test_incorrect_session_returns_400(self):
        """test_incorrect_session_returns_400"""
        mock_request = MockRequest()
        mock_request.user = create_mock_user(1, is_staff=True)
        mock_request.session = {}

        response = download_xml_build_req(mock_request)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("core_oaipmh_harvester_app.views.admin.ajax.XSDTree")
    def test_success_returns_200(self, mock_xsd_tree):
        """test_success_returns_200"""
        mock_xsd_tree.build_tree.return_value = None
        mock_xsd_tree.tostring.return_value = None

        mock_request = MockRequest()
        mock_request.user = create_mock_user(1, is_staff=True)
        mock_request.session = {"xmlStringOAIPMH": "mock_xml_string"}

        response = download_xml_build_req(mock_request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
