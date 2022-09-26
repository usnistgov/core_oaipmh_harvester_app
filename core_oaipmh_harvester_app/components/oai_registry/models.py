"""
OaiRegistry model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions


class OaiRegistry(models.Model):
    """A registry object for Oai-Pmh Harvester"""

    name = models.CharField(blank=False, max_length=200)
    url = models.URLField(unique=True)
    harvest_rate = models.IntegerField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default="")
    harvest = models.BooleanField(default=False)
    last_update = models.DateTimeField(blank=True, null=True)
    is_harvesting = models.BooleanField(default=False)
    is_updating = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)
    is_queued = models.BooleanField(default=False)

    class Meta:
        """Meta"""

        verbose_name = "Oai registry"
        verbose_name_plural = "Oai registries"

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
            return OaiRegistry.objects.get(pk=str(oai_registry_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

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
            return OaiRegistry.objects.get(name=oai_registry_name)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_all():
        """Return all OaiRegistry

        Returns:
            List of OaiRegistry

        """
        return OaiRegistry.objects.all()

    @staticmethod
    def get_all_by_is_activated(is_activated, order_by_field=None):
        """Return all OaiRegistry by their is_activated field

        Params:
            is_activated: True or False.
            order_by_field: Field to order on.

        Returns:
            List of OaiRegistry

        """
        queryset = OaiRegistry.objects.filter(is_activated=is_activated)
        if order_by_field:
            queryset.order_by(order_by_field)
        return queryset

    @staticmethod
    def check_registry_url_already_exists(oai_registry_url):
        """Check if an OaiRegistry with the given url already exists.

        Params:
            oai_registry_url: URL to check.

        Returns:
            Yes or No (bool).

        """
        return (
            OaiRegistry.objects.filter(url__exact=oai_registry_url).count() > 0
        )
