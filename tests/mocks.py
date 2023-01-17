""" Mock objects for core_oaipmh_harvester_app
"""
from unittest.mock import Mock


class MockObject(Mock):
    id = "mock_id"


class MockMongoOaiRecord(MockObject):
    dict_content = "mock_dict_content"


class MockRequest:
    user = None
    session: dict = None
