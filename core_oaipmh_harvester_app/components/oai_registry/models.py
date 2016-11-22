"""
OaiRegistry model
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions
from mongoengine.queryset.base import NULLIFY
from core_oaipmh_harvester_app.components.oai_identify.models import OaiIdentify


class OaiRegistry(Document):
    """ A registry object for Oai-Pmh Harvester"""
    name = fields.StringField()
    url = fields.URLField(unique=True)
    harvest_rate = fields.IntField(blank=True)
    identify = fields.ReferenceField(OaiIdentify, reverse_delete_rule=NULLIFY)
    description = fields.StringField(blank=True)
    harvest = fields.BooleanField()
    last_update = fields.DateTimeField(blank=True)
    is_harvesting = fields.BooleanField()
    is_updating = fields.BooleanField()
    is_deactivated = fields.BooleanField()
    is_queued = fields.BooleanField()

    @staticmethod
    def get_by_id(oai_registry_id):
        """ Get an OaiRegistry by its id

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
            raise exceptions.DoesNotExist(e.message)
        except Exception as e:
            raise exceptions.ModelError(e.message)

    @staticmethod
    def get_by_name(oai_registry_name):
        """ Get an OaiRegistry by its name.

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
            raise exceptions.DoesNotExist(e.message)
        except Exception as e:
            raise exceptions.ModelError(e.message)

    @staticmethod
    def get_all():
        """ Return all OaiRegistry

        Returns:
            List of OaiRegistry

        """
        return OaiRegistry.objects().all()

    @staticmethod
    def get_all_by_is_deactivated(is_deactivated, order_by_field=None):
        """ Return all OaiRegistry by their is_deactivated field

            Returns:
                List of OaiRegistry

            """
        return OaiRegistry.objects(is_deactivated=is_deactivated).order_by(order_by_field)

    @staticmethod
    def check_registry_url_already_exists(oai_registry_url):
        """ Check if an OaiRegistry with the given url already exists.

        Returns:
            Yes or No (bool).

        """
        return OaiRegistry.objects(url__exact=oai_registry_url).count() > 0
