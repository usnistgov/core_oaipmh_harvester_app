""" Unit Test oai_verbs
"""
from unittest.case import TestCase
from unittest.mock import patch

import requests
from rest_framework import status

from core_oaipmh_common_app.commons import exceptions as oai_pmh_exceptions
import core_oaipmh_harvester_app.components.oai_verbs.api as oai_verbs_api
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_harvester_set.models import (
    OaiHarvesterSet,
)
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify
from tests.components.oai_registry.fixtures.fixtures import OaiPmhMock
from tests.test_settings import SSL_CERTIFICATES_DIR


class TestIdentifyAsObject(TestCase):
    """Test Identify As Object"""

    @patch.object(
        oai_verbs_api.transform_operations,
        "transform_dict_identifier_to_oai_identifier",
    )
    @patch.object(oai_verbs_api, "identify")
    def test_identify_as_object_return_object_and_ok_status(
        self, mock_identify, mock_transform
    ):
        """test_identify_as_object_return_object_and_ok_status"""

        # Arrange
        mock_identify.return_value = [], status.HTTP_200_OK
        mock_transform.return_value = OaiIdentify()

        # Act
        data, status_code = oai_verbs_api.identify_as_object("")

        # Assert
        self.assertIsInstance(data, OaiIdentify)
        self.assertEqual(status_code, status.HTTP_200_OK)


class TestListMetadataFormatsAsObject(TestCase):
    """Test List Metadata Formats As Object"""

    @patch.object(
        oai_verbs_api.transform_operations,
        "transform_dict_metadata_format_to_oai_harvester_metadata_format",
    )
    @patch.object(oai_verbs_api, "list_metadata_formats")
    def test_list_metadata_formats_as_object_return_object_and_ok_status(
        self, mock_metadata_format, mock_transform
    ):
        """test_list_metadata_formats_as_object_return_object_and_ok_status"""

        # Arrange
        mock_metadata_format.return_value = [], status.HTTP_200_OK
        mock_transform.return_value = [
            OaiHarvesterMetadataFormat(),
            OaiHarvesterMetadataFormat(),
        ]

        # Act
        data, status_code = oai_verbs_api.list_metadata_formats_as_object("")

        # Assert
        self.assertTrue(
            all(isinstance(item, OaiHarvesterMetadataFormat) for item in data)
        )
        self.assertEqual(status_code, status.HTTP_200_OK)


class TestListSetsAsObject(TestCase):
    """Test List Sets As Object"""

    @patch.object(
        oai_verbs_api.transform_operations, "transform_dict_set_to_oai_harvester_set"
    )
    @patch.object(oai_verbs_api, "list_sets")
    def test_list_sets_as_object_return_object_and_ok_status(
        self, mock_set, mock_transform
    ):
        """test_list_sets_as_object_return_object_and_ok_status"""

        # Arrange
        mock_set.return_value = [], status.HTTP_200_OK
        mock_transform.return_value = [OaiHarvesterSet(), OaiHarvesterSet()]

        # Act
        data, status_code = oai_verbs_api.list_sets_as_object("")

        # Assert
        self.assertTrue(all(isinstance(item, OaiHarvesterSet) for item in data))
        self.assertEqual(status_code, status.HTTP_200_OK)


class TestListRecordsParameter(TestCase):
    """TestListRecordsParameter"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.url = "http://dummy_url.com"
        self.metadata_prefix = "oai_prefix"
        self.set = "oai_set"
        self.from_ = "2017-04-24T02:00:00Z"
        self.until = "2018-04-24T02:00:00Z"

    @patch.object(requests, "get")
    def test_harvest_params(self, mock_get):
        """test_harvest_params"""

        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = OaiPmhMock.mock_oai_response_list_records()
        expected_params = {
            "verb": "ListRecords",
            "metadataPrefix": self.metadata_prefix,
            "set": self.set,
            "from": self.from_,
            "until": self.until,
        }

        # Act
        oai_verbs_api.list_records(
            url=self.url,
            metadata_prefix=self.metadata_prefix,
            set_h=self.set,
            from_date=self.from_,
            until_date=self.until,
        )

        # Assert
        mock_get.assert_called_with(
            self.url, expected_params, verify=SSL_CERTIFICATES_DIR
        )

    @patch.object(requests, "get")
    def test_harvest_params_with_resumption_token(self, mock_get):
        """test_harvest_params_with_resumption_token"""

        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = OaiPmhMock.mock_oai_response_list_records()
        resumption_token = "h34fh"
        expected_params = {"verb": "ListRecords", "resumptionToken": "h34fh"}

        # Act
        oai_verbs_api.list_records(
            url=self.url,
            metadata_prefix=self.metadata_prefix,
            set_h=self.set,
            from_date=self.from_,
            until_date=self.until,
            resumption_token=resumption_token,
        )

        # Asset
        mock_get.assert_called_with(
            self.url, expected_params, verify=SSL_CERTIFICATES_DIR
        )

    @patch.object(requests, "get")
    def test_harvest_params_returns_error_if_not_200_OK(self, mock_get):
        """test_harvest_params_returns_error_if_not_200_OK"""

        # Arrange
        error = "An error occurred while trying to get data from the server."
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_get.return_value.status_code = status_code
        mock_get.return_value.text = "Error."

        # Act
        result, resumption_token = oai_verbs_api.list_records(self.url)

        # Assert
        self.assertEqual(result.data[oai_pmh_exceptions.OaiPmhMessage.label], error)
        self.assertEqual(result.status_code, status_code)

    @patch.object(requests, "get")
    def test_harvest_params_returns_error_if_404_not_found(self, mock_get):
        """test_harvest_params_returns_error_if_404_not_found"""

        # Arrange
        error = "Impossible to get data from the server. Server not found"
        status_code = status.HTTP_404_NOT_FOUND
        mock_get.return_value.status_code = status_code
        mock_get.return_value.text = "Error."

        # Act
        result, resumption_token = oai_verbs_api.list_records(self.url)

        # Assert
        self.assertEqual(result.data[oai_pmh_exceptions.OaiPmhMessage.label], error)
        self.assertEqual(result.status_code, status_code)

    @patch.object(requests, "get")
    def test_harvest_params_returns_serialized_data_and_resumption_token(
        self, mock_get
    ):
        """test_harvest_params_returns_serialized_data_and_resumption_token"""

        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = OaiPmhMock.mock_oai_response_list_records()
        resumption_token = "h34fh"

        # Act
        result, resumption_token = oai_verbs_api.list_records(
            url=self.url,
            metadata_prefix=self.metadata_prefix,
            set_h=self.set,
            from_date=self.from_,
            until_date=self.until,
            resumption_token=resumption_token,
        )

        # Asset
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertNotEqual(resumption_token, None)
        self.assertTrue(len(result.data), 1)
