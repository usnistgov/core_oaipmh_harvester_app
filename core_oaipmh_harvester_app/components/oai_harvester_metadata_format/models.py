"""
OaiHarvesterMetadataFormat model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_oaipmh_common_app.components.oai_metadata_format.models import (
    OaiMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class OaiHarvesterMetadataFormat(OaiMetadataFormat):
    """Represents a metadata format for Oai-Pmh Harvester"""

    raw = models.JSONField()
    template = models.ForeignKey(
        Template, on_delete=models.SET_NULL, blank=True, null=True
    )
    registry = models.ForeignKey(OaiRegistry, on_delete=models.CASCADE)
    hash = models.CharField(blank=False, max_length=200)
    harvest = models.BooleanField(default=False)
    last_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        """Meta"""

        unique_together = ("registry", "metadata_prefix")

    @staticmethod
    def get_by_id(oai_harvester_metadata_format_id):
        try:
            return OaiHarvesterMetadataFormat.objects.get(
                pk=oai_harvester_metadata_format_id
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_all_by_registry_id(registry_id, order_by_field=None):
        """Return a list of OaiHarvesterMetadataFormat by registry id. Possibility to order_by the list

        Args:
            registry_id: The registry id.
            order_by_field: Order by field.

        Returns:
            List of OaiHarvesterMetadataFormat

        """
        queryset = OaiHarvesterMetadataFormat.objects.filter(registry=str(registry_id))

        if order_by_field is not None:
            queryset.order_by(order_by_field)

        return queryset

    @staticmethod
    def get_all_by_list_registry_ids(list_registry_ids, order_by_field=None):
        """Return a list of OaiHarvesterMetadataFormat by a list of registry ids. Possibility to order_by the list

        Args:
            list_registry_ids: List of registry ids.
            order_by_field: Order by field.

        Returns:
            List of OaiHarvesterMetadataFormat.

        """
        queryset = OaiHarvesterMetadataFormat.objects.filter(
            registry__in=list_registry_ids
        )

        if order_by_field is not None:
            queryset.order_by(order_by_field)

        return queryset

    @staticmethod
    def get_all_by_registry_id_and_harvest(registry_id, harvest, order_by_field=None):
        """

        Args:
            registry_id: The registry id.
            harvest: Harvest (True/False).
            order_by_field: Order by field.

        Returns:
            List of OaiHarvesterMetadataFormat.

        """
        queryset = OaiHarvesterMetadataFormat.objects.filter(
            registry=str(registry_id), harvest=harvest
        )

        if order_by_field is not None:
            queryset.order_by(order_by_field)

        return queryset

    @staticmethod
    def get_by_metadata_prefix_and_registry_id(metadata_prefix, registry_id):
        """Return an OaiHarvesterMetadataFormat by metadata_prefix and registry id.

        Args:
            metadata_prefix: The metadata prefix.
            registry_id:  The registry id.

        Returns:
            OaiHarvesterMetadataFormat instance.

        Raises:
            DoesNotExist: The OaiHarvesterMetadataFormat doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiHarvesterMetadataFormat.objects.get(
                metadata_prefix=metadata_prefix, registry=str(registry_id)
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def delete_all_by_registry_id(registry_id):
        """Delete all OaiHarvesterMetadataFormat used by a registry.

        Args:
            registry_id: The registry id.

        """
        OaiHarvesterMetadataFormat.get_all_by_registry_id(registry_id).delete()

    @staticmethod
    def update_for_all_harvest_by_registry_id(registry_id, harvest):
        """Update the harvest for all OaiHarvesterMetadataFormat used by the registry.

        Args:
            registry_id: The registry id.
            harvest: Harvest (True/False).

        """
        OaiHarvesterMetadataFormat.get_all_by_registry_id(registry_id).update(
            set__harvest=harvest
        )

    @staticmethod
    def update_for_all_harvest_by_list_ids(list_oai_metadata_format_ids, harvest):
        """Update the harvest for all OaiHarvesterMetadataFormat by a list of ids.

        Args:
            list_oai_metadata_format_ids: List of OaiHarvesterMetadataFormat ids.
            harvest: Harvest (True/False)

        """
        OaiHarvesterMetadataFormat.get_all_by_list_ids(
            list_oai_metadata_format_ids
        ).update(set__harvest=harvest)

    def get_display_name(self):
        """Return harvester metadata format name to display.

        Returns:

        """
        # Use the metadata prefix name
        display_name = self.metadata_prefix
        # If a template corresponds to this metadata prefix, we add the template name
        if self.template:
            display_name += " - {0}".format(self.template.display_name)

        return display_name
