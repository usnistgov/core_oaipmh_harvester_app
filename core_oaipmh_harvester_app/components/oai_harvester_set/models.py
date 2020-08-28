"""
OaiHarvesterSet model
"""

from django_mongoengine import fields
from mongoengine import errors as mongoengine_errors
from mongoengine.queryset.base import CASCADE

from core_main_app.commons import exceptions
from core_oaipmh_common_app.components.oai_set.models import OaiSet
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class OaiHarvesterSet(OaiSet):
    """Represents a set for Oai-Pmh Harvester"""

    raw = fields.DictField()
    registry = fields.ReferenceField(
        OaiRegistry, reverse_delete_rule=CASCADE, unique_with="set_spec"
    )
    harvest = fields.BooleanField(blank=True)

    @staticmethod
    def get_all_by_registry_id(registry_id, order_by_field=None):
        """Return a list of OaiHarvesterSet by registry id. Possibility to order_by the list

        Args:
            registry_id: The registry id.
            order_by_field: Order by field.

        Returns:
            List of OaiHarvesterSet.

        """
        return OaiHarvesterSet.objects(registry=str(registry_id)).order_by(
            order_by_field
        )

    @staticmethod
    def get_all_by_registry_id_and_harvest(registry_id, harvest, order_by_field=None):
        """Return a list of OaiHarvesterSet by registry and harvest. Possibility to order_by the list.

        Args:
            registry_id: The registry id.
            harvest: Harvest (True/False).
            order_by_field: Order by field.

        Returns:
            List of OaiHarvesterSet.

        """
        return OaiHarvesterSet.objects(
            registry=str(registry_id), harvest=harvest
        ).order_by(order_by_field)

    @staticmethod
    def get_by_set_spec_and_registry_id(set_spec, registry_id):
        """Return a OaiHarvesterSet by set_spec and registry.

        Args:
            set_spec: The set spec
            registry_id: The registry id.

        Returns: OaiHarvesterSet instance.

        Raises:
            DoesNotExist: The OaiHarvesterSet doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiHarvesterSet.objects().get(
                set_spec=set_spec, registry=str(registry_id)
            )
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def delete_all_by_registry_id(registry_id):
        """Delete all OaiHarvesterSet used by a registry.

        Args:
            registry_id: The registry id.

        """
        OaiHarvesterSet.get_all_by_registry_id(registry_id).delete()

    @staticmethod
    def update_for_all_harvest_by_registry_id(registry_id, harvest):
        """Update the harvest for all OaiHarvesterSet used by the registry.

        Args:
            registry_id: The registry id.
            harvest: Harvest (True/False).

        """
        OaiHarvesterSet.get_all_by_registry_id(registry_id).update(set__harvest=harvest)

    @staticmethod
    def update_for_all_harvest_by_list_ids(list_oai_set_ids, harvest):
        """Update the harvest for all OaiHarvesterSet by a list of ids.

        Args:
            list_oai_set_ids: List of OaiHarvesterSet ids.
            harvest: Harvest (True/False)

        """
        OaiHarvesterSet.get_all_by_list_ids(list_oai_set_ids).update(
            set__harvest=harvest
        )
