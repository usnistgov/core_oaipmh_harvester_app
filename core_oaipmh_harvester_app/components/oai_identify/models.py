"""
OaiIdentify model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class OaiIdentify(models.Model):
    """Represents an identify object for Oai-Pmh Harvester"""

    admin_email = models.CharField(blank=True, null=True, max_length=200)
    base_url = models.URLField(unique=True)
    repository_name = models.CharField(blank=True, null=True, max_length=200)
    deleted_record = models.CharField(blank=True, null=True, max_length=200)
    delimiter = models.CharField(blank=True, null=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    earliest_datestamp = models.CharField(blank=True, null=True, max_length=200)
    granularity = models.CharField(blank=True, null=True, max_length=200)
    oai_identifier = models.CharField(blank=True, null=True, max_length=200)
    protocol_version = models.CharField(blank=True, null=True, max_length=200)
    repository_identifier = models.CharField(blank=True, null=True, max_length=200)
    sample_identifier = models.CharField(blank=True, null=True, max_length=200)
    scheme = models.CharField(blank=True, null=True, max_length=200)
    raw = models.JSONField(blank=True, null=True)
    registry = models.OneToOneField(OaiRegistry, on_delete=models.CASCADE, unique=True)

    class Meta:
        """Meta"""

        verbose_name = "Oai identify"
        verbose_name_plural = "Oai identify"

    @staticmethod
    def get_by_registry_id(registry_id):
        """Return an OaiIdentify by its registry id.

        Args:
            registry_id:  The registry id.

        Returns:
            OaiIdentify instance.

        Raises:
            DoesNotExist: The OaiIdentify doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiIdentify.objects.get(registry=str(registry_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))
