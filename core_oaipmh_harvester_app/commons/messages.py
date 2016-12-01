""" OAI-PMH Messages
"""


class OaiPmhMessage(object):
    """ Const values
    """
    label = 'message'
    errors = 'errors'

    @staticmethod
    def get_message_labelled(message):
        """ Get the given message labelled.

        Args:
            message: Message to label.

        Returns:
            The message.

        """
        return {OaiPmhMessage.label: message}

    @staticmethod
    def get_message_serialize_labelled(message, errors=None):
        """ Get the given message labelled. Used by a serialized error.

        Args:
            message: Message to label.
            errors: List of errors.

        Returns:
            The message.

        """
        if errors is None:
            errors = []
        return {OaiPmhMessage.label: message, OaiPmhMessage.errors: errors}
