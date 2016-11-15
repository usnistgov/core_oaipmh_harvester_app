"""
OaiHarvesterSet model
"""

from django_mongoengine import fields
from core_oaipmh_common_app.components.oai_set.models import OaiSet


class OaiHarvesterSet(OaiSet):
    """Represents a set for Oai-Pmh Harvester"""
    raw = fields.DictField()
    registry = fields.StringField(unique=True)
    harvest = fields.BooleanField(blank=True)

    @staticmethod
    def get_all_by_registry(registry, order_by_field=None):
        """
        Return a list of OaiHarvesterSet by registry. Possibility to order_by the list
        :param registry:
        :param order_by_field:
        :return:
        """
        return OaiHarvesterSet.objects(registry=registry).order_by(order_by_field)

    @staticmethod
    def get_all_by_registry_and_harvest(registry, harvest, order_by_field=None):
        """
        Return a list of OaiHarvesterSet by registry and harvest. Possibility to order_by the list
        :param registry:
        :param harvest:
        :param order_by_field:
        :return:
        """
        return OaiHarvesterSet.objects(registry=registry, harvest=harvest).order_by(order_by_field)

    @staticmethod
    def get_by_set_spec_and_registry(set_spec, registry_id):
        """
        Return a OaiHarvesterSet by setSpec and registry.
        :param set_spec:
        :param registry_id:
        :return:
        """
        return OaiHarvesterSet.objects().get(setSpec=set_spec, registry=str(registry_id))

    @staticmethod
    def delete_all_by_registry(registry):
        """
        Delete all OaiHarvesterSet used by a registry
        :param registry:
        :return:
        """
        OaiHarvesterSet.get_all_by_registry(registry).delete()

    @staticmethod
    def update_for_all_harvest_by_registry(registry, harvest):
        """
        Update the harvest for all OaiHarvesterSet used by the registry
        :param registry:
        :param harvest:
        :return:
        """
        OaiHarvesterSet.get_all_by_registry(registry).update(set__harvest=harvest)

    @staticmethod
    def update_for_all_harvest_by_list_ids(list_oai_set_ids, harvest):
        """
        Update the harvest for all OaiHarvesterSet by a list of ids
        :param list_oai_set_ids:
        :param harvest:
        :return:
        """
        OaiHarvesterSet.get_all_by_list_ids(list_oai_set_ids).update(set__harvest=harvest)
