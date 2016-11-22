"""
OaiRegistry API
"""


from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


def upsert(oai_registry):
    """ Create or update an OaiRegistry.

    Args:
        oai_registry: The OaiRegistry to create or update

    Returns: The OaiRegistry instance.

    """
    return oai_registry.save()


def get_by_id(oai_registry_id):
    """ Get an OaiRegistry by its id

    Args:
        oai_registry_id: OaiRegistry id.

    Returns: The OaiRegistry instance.

    Raises:
        DoesNotExist: The registry doesn't exist
        ModelError: Internal error during the process

    """
    return OaiRegistry.get_by_id(oai_registry_id)


def get_by_name(oai_registry_name):
    """ Get an OaiRegistry by its name.

    Args:
        oai_registry_name: OaiRegistry name.

    Returns: The OaiRegistry instance.

    Raises:
        DoesNotExist: The registry doesn't exist
        ModelError: Internal error during the process

    """
    return OaiRegistry.get_by_name(oai_registry_name=oai_registry_name)


def get_all():
    """ Return all OaiRegistry

    Returns:
        List of OaiRegistry

    """
    return OaiRegistry.get_all()


def get_all_activated_registry(order_by_field=None):
    """ Return all activated OaiRegistry.

        Returns:
            List of OaiRegistry

        """
    return OaiRegistry.get_all_by_is_deactivated(is_deactivated=False, order_by_field=order_by_field)


def check_registry_url_already_exists(oai_registry_url):
    """ Check if an OaiRegistry with the given url already exists.

    Returns:
        Yes or No (bool).

    """
    return OaiRegistry.check_registry_url_already_exists(oai_registry_url=oai_registry_url)
