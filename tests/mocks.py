"""Mock objects for core_oaipmh_harvester_app"""

from unittest.mock import Mock

from rest_framework import status


class MockObject(Mock):
    id = "mock_id"


class MockMongoOaiRecord(MockObject):
    dict_content = "mock_dict_content"


class MockRequest:
    """Simple request mock with user and session.session_key."""

    def __init__(self, session_key=None, user=None):
        self.user = user
        self.session = Mock(session_key=session_key)


class MockMetadataFormat:
    """Mock OaiHarvesterMetadataFormat with schema and metadata_prefix."""

    def __init__(self, schema_url):
        self.schema = schema_url
        self.metadata_prefix = "test"


class MockProviderResponse:
    """Callable mock provider that returns 200 only when the correct sessionid is
    provided.
    """

    session_id_key = "mock-session-key"
    success_data = "<root></root>"
    not_found_text = "Not found or not accessible."

    def __init__(self, session_key=None):
        # Use class default if no session_key provided
        if session_key is not None:
            self.session_id_key = session_key

    def __call__(self, url, **kwargs):
        response = Mock()
        cookies = kwargs.get("cookies") or {}
        if cookies.get("sessionid") == self.session_id_key:
            response.status_code = status.HTTP_200_OK
            response.text = self.success_data
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            response.text = self.not_found_text
        return response
