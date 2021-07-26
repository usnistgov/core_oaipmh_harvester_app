"""
OaiRegistry model
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions


class OaiRegistry(Document):
    """A registry object for Oai-Pmh Harvester"""

    name = fields.StringField()
    url = fields.URLField(unique=True)
    harvest_rate = fields.IntField(blank=True)
    description = fields.StringField(blank=True)
    harvest = fields.BooleanField(default=False)
    last_update = fields.DateTimeField(blank=True)
    is_harvesting = fields.BooleanField(default=False)
    is_updating = fields.BooleanField(default=False)
    is_activated = fields.BooleanField(default=True)
    is_queued = fields.BooleanField(default=False)

    @staticmethod
    def get_by_id(oai_registry_id):
        """Get an OaiRegistry by its id

        Args:
            oai_registry_id: OaiRegistry id.

        Returns: The OaiRegistry instance.

        Raises:
            DoesNotExist: The registry doesn't exist
            ModelError: Internal error during the process

        """
        try:
            return OaiRegistry.objects().get(pk=str(oai_registry_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_by_name(oai_registry_name):
        """Get an OaiRegistry by its name.

        Args:
            oai_registry_name: OaiRegistry name.

        Returns: The OaiRegistry instance.

        Raises:
            DoesNotExist: The registry doesn't exist
            ModelError: Internal error during the process

        """
        try:
            return OaiRegistry.objects().get(name=oai_registry_name)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_all():
        """Return all OaiRegistry

        Returns:
            List of OaiRegistry

        """
        return OaiRegistry.objects().all()

    @staticmethod
    def get_all_by_is_activated(is_activated, order_by_field=None):
        """Return all OaiRegistry by their is_activated field

        Params:
            is_activated: True or False.
            order_by_field: Field to order on.

        Returns:
            List of OaiRegistry

        """
        return OaiRegistry.objects(is_activated=is_activated).order_by(order_by_field)

    @staticmethod
    def check_registry_url_already_exists(oai_registry_url):
        """Check if an OaiRegistry with the given url already exists.

        Params:
            oai_registry_url: URL to check.

        Returns:
            Yes or No (bool).

        """
        return OaiRegistry.objects(url__exact=oai_registry_url).count() > 0
