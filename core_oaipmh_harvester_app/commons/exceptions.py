""" OAI-PMH Exceptions
"""

from rest_framework.response import Response
from core_oaipmh_harvester_app.commons.messages import OaiPmhMessage
from rest_framework import status


class OAIAPIException(Exception):
    """ OAIAPIException.
    """
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return repr(self.message)

    def response(self):
        return Response(self.message, status=self.status_code)


class OAIAPILabelledException(OAIAPIException):
    """ Labelled OAIAPIException.
    """
    def response(self):
        return Response(OaiPmhMessage.get_message_labelled(self.message), status=self.status_code)


class OAIAPISerializeLabelledException(OAIAPIException):
    """ Labelled OAIAPIException used by serialized error.
    """
    def __init__(self, status_code, errors=None,
                 message="Error while attempting to retrieve params values. Please check your entries."):
        super(OAIAPISerializeLabelledException, self).__init__(message, status_code)
        if errors is None:
            errors = []
        self.errors = errors

    def response(self):
        return Response(OaiPmhMessage.get_message_serialize_labelled(self.message, self.errors),
                        status=self.status_code)


class OAIAPINotUniqueError(OAIAPIException):
    """ OAIAPINotUniqueError.
    """
    def __init__(self, message, status_code=status.HTTP_409_CONFLICT):
        super(OAIAPINotUniqueError, self).__init__(message, status_code=status_code)
