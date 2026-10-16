"""Unit tests for admin AJAX views"""

from unittest.mock import patch

from django.test.testcases import TestCase
from rest_framework import status

from urllib.parse import urlencode

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_harvester_app.views.admin import ajax as admin_views_ajax
from tests.mocks import MockRequest


class TestDownloadXmlBuildReq(TestCase):
    """Unit tests for `download_xml_build_req`"""

    def test_incorrect_session_returns_400(self):
        """test_incorrect_session_returns_400"""
        mock_request = MockRequest()
        mock_request.user = create_mock_user(1, is_staff=True)
        mock_request.session = {}

        response = admin_views_ajax.download_xml_build_req(mock_request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("core_oaipmh_harvester_app.views.admin.ajax.XSDTree")
    def test_success_returns_200(self, mock_xsd_tree):
        """test_success_returns_200"""
        mock_xsd_tree.build_tree.return_value = None
        mock_xsd_tree.tostring.return_value = None

        mock_request = MockRequest()
        mock_request.user = create_mock_user(1, is_staff=True)
        mock_request.session = {"xmlStringOAIPMH": "mock_xml_string"}

        response = admin_views_ajax.download_xml_build_req(mock_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDeactivateRegistry(TestCase):
    """Unit tests for `deactivate_registry`"""

    def setUp(self):
        """setUp"""
        self.staff_user = create_mock_user(1, is_staff=True)

    def test_get_not_allowed(self):
        """test_get_not_allowed"""
        response = RequestMock.do_request_get(
            admin_views_ajax.deactivate_registry, self.staff_user
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @patch.object(admin_views_ajax.oai_registry_api, "upsert")
    @patch.object(admin_views_ajax.oai_registry_api, "get_by_id")
    def test_post_allowed(self, mock_get_by_id, mock_upsert):
        """test_post_allowed"""
        mock_registry = mock_get_by_id.return_value

        response = RequestMock.do_request_post(
            admin_views_ajax.deactivate_registry,
            self.staff_user,
            data=urlencode({"id": "1"}),
            content_type="application/x-www-form-urlencoded",
        )

        mock_get_by_id.assert_called_with("1")
        self.assertFalse(mock_registry.is_activated)
        mock_upsert.assert_called_with(mock_registry)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestActivateRegistry(TestCase):
    """Unit tests for `activate_registry`"""

    def setUp(self):
        """setUp"""
        self.staff_user = create_mock_user(1, is_staff=True)

    def test_get_not_allowed(self):
        """test_get_not_allowed"""
        response = RequestMock.do_request_get(
            admin_views_ajax.activate_registry, self.staff_user
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @patch.object(admin_views_ajax.oai_registry_api, "upsert")
    @patch.object(admin_views_ajax.oai_registry_api, "get_by_id")
    def test_post_allowed(self, mock_get_by_id, mock_upsert):
        """test_post_allowed"""
        mock_registry = mock_get_by_id.return_value

        response = RequestMock.do_request_post(
            admin_views_ajax.activate_registry,
            self.staff_user,
            data=urlencode({"id": "1"}),
            content_type="application/x-www-form-urlencoded",
        )

        mock_get_by_id.assert_called_with("1")
        self.assertTrue(mock_registry.is_activated)
        mock_upsert.assert_called_with(mock_registry)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDeleteRegistry(TestCase):
    """Unit tests for `delete_registry`"""

    def setUp(self):
        """setUp"""
        self.staff_user = create_mock_user(1, is_staff=True)

    def test_get_not_allowed(self):
        """test_get_not_allowed"""
        response = RequestMock.do_request_get(
            admin_views_ajax.delete_registry, self.staff_user
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @patch.object(admin_views_ajax.oai_registry_api, "delete")
    @patch.object(admin_views_ajax.oai_registry_api, "get_by_id")
    def test_post_allowed(self, mock_get_by_id, mock_delete):
        """test_post_allowed"""
        mock_registry = mock_get_by_id.return_value

        response = RequestMock.do_request_post(
            admin_views_ajax.delete_registry,
            self.staff_user,
            data=urlencode({"id": "1"}),
            content_type="application/x-www-form-urlencoded",
        )

        mock_get_by_id.assert_called_with("1")
        mock_delete.assert_called_with(mock_registry)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCheckRegistry(TestCase):
    """Unit tests for `check_registry`"""

    def setUp(self):
        """setUp"""
        self.staff_user = create_mock_user(1, is_staff=True)

    def test_get_not_allowed(self):
        """test_get_not_allowed"""
        response = RequestMock.do_request_get(
            admin_views_ajax.check_registry, self.staff_user
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @patch.object(admin_views_ajax.oai_verb_api, "identify")
    def test_post_allowed(self, mock_identify):
        """test_post_allowed"""
        mock_identify.return_value = ({}, status.HTTP_200_OK)
        mock_registry_url = "http://registry.example.com"  # noqa

        response = RequestMock.do_request_post(
            admin_views_ajax.check_registry,
            self.staff_user,
            data=urlencode({"url": mock_registry_url}),
            content_type="application/x-www-form-urlencoded",
        )

        mock_identify.assert_called_with(mock_registry_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUpdateRegistry(TestCase):
    """Unit tests for `update_registry`"""

    def setUp(self):
        """setUp"""
        self.staff_user = create_mock_user(1, is_staff=True)

    def test_get_not_allowed(self):
        """test_get_not_allowed"""
        response = RequestMock.do_request_get(
            admin_views_ajax.update_registry, self.staff_user
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @patch.object(admin_views_ajax.oai_registry_api, "update_registry_info")
    @patch.object(admin_views_ajax.oai_registry_api, "get_by_id")
    def test_post_allowed(self, mock_get_by_id, mock_update_registry_info):
        """test_post_allowed"""
        mock_registry = mock_get_by_id.return_value

        response = RequestMock.do_request_post(
            admin_views_ajax.update_registry,
            self.staff_user,
            data=urlencode({"id": "1"}),
            content_type="application/x-www-form-urlencoded",
        )

        mock_get_by_id.assert_called_with("1")
        # update_registry_info is called with registry and request; we only assert registry arg
        self.assertTrue(mock_update_registry_info.called)
        called_registry = mock_update_registry_info.call_args[0][0]
        self.assertIs(called_registry, mock_registry)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestHarvestRegistry(TestCase):
    """Unit tests for `harvest_registry`"""

    def setUp(self):
        """setUp"""
        self.staff_user = create_mock_user(1, is_staff=True)

    def test_get_not_allowed(self):
        """test_get_not_allowed"""
        response = RequestMock.do_request_get(
            admin_views_ajax.harvest_registry, self.staff_user
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @patch.object(admin_views_ajax.oai_registry_api, "harvest_registry")
    @patch.object(admin_views_ajax.oai_registry_api, "get_by_id")
    def test_post_allowed(self, mock_get_by_id, mock_harvest_registry):
        """test_post_allowed"""
        mock_registry = mock_get_by_id.return_value

        response = RequestMock.do_request_post(
            admin_views_ajax.harvest_registry,
            self.staff_user,
            data=urlencode({"id": "1"}),
            content_type="application/x-www-form-urlencoded",
        )

        mock_get_by_id.assert_called_with("1")
        mock_harvest_registry.assert_called_with(mock_registry)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetData(TestCase):
    """Unit tests for `get_data`"""

    def setUp(self):
        """setUp"""
        self.staff_user = create_mock_user(1, is_staff=True)

    def test_get_not_allowed(self):
        """test_get_not_allowed"""
        response = RequestMock.do_request_get(
            admin_views_ajax.get_data, self.staff_user
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @patch.object(admin_views_ajax, "_read_file_content")
    @patch.object(admin_views_ajax, "xsl_transform")
    @patch.object(admin_views_ajax.finders, "find")
    @patch.object(admin_views_ajax.oai_verb_api, "get_data")
    def test_post_allowed(
        self,
        mock_get_data,
        mock_find,
        mock_xsl_transform,
        mock_read_file_content,
    ):
        """test_post_allowed"""
        mock_get_data.return_value.data = "<record/>"
        mock_find.return_value = "/dummy/xml2html.xsl"
        mock_read_file_content.return_value = "<xsl/>"
        mock_xsl_transform.return_value = "<html/>"

        response = RequestMock.do_request_post(
            admin_views_ajax.get_data,
            self.staff_user,
            data=urlencode(
                {
                    "url": "http://registry.example.com",  # noqa
                    "args_url": "{}",
                }
            ),
            content_type="application/x-www-form-urlencoded",
        )

        mock_get_data.assert_called_once()
        # The view reads POST data, so we just check it was called
        self.assertEqual(response.status_code, status.HTTP_200_OK)
