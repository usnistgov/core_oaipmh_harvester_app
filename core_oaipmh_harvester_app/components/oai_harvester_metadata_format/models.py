"""
OaiHarvesterMetadataFormat model
"""

from django_mongoengine import fields
from mongoengine.queryset.base import PULL
from core_oaipmh_common_app.components.oai_metadata_format.models import OaiMetadataFormat
from core_main_app.components.template.models import Template


class OaiHarvesterMetadataFormat(OaiMetadataFormat):
    """Represents a metadata format for Oai-Pmh Harvester"""
    raw = fields.DictField()
    template = fields.ReferenceField(Template, reverse_delete_rull=PULL, blank=True)
    registry_id = fields.StringField(unique=True)
    hash = fields.StringField(blank=True)
    harvest = fields.StringField(blank=True)
    lastUpdate = fields.DateTimeField(blank=True)

    @staticmethod
    def get_all_by_registry_id(registry_id, order_by_field=None):
        """
        Return a list of OaiHarvesterMetadataFormat by registry id. Possibility to order_by the list
        :param registry_id:
        :param order_by_field:
        :return:
        """
        return OaiHarvesterMetadataFormat.objects(registry_id=str(registry_id)).order_by(order_by_field)

    @staticmethod
    def get_all_by_list_registry_ids(list_registry_ids, order_by_field=None):
        """
        Return a list of OaiHarvesterMetadataFormat by a list of registry ids. Possibility to order_by the list
        :param list_registry_ids:
        :param order_by_field:
        :return:
        """
        return OaiHarvesterMetadataFormat.objects(registry_id__in=list_registry_ids).order_by(order_by_field)

    @staticmethod
    def get_all_by_registry_id_and_harvest(registry_id, harvest, order_by_field=None):
        """
        Return a list of OaiHarvesterMetadataFormat by registry id and harvest. Possibility to order_by the list
        :param registry_id:
        :param harvest:
        :param order_by_field:
        :return:
        """
        return OaiHarvesterMetadataFormat.objects(registry_id=str(registry_id), harvest=harvest).\
            order_by(order_by_field)

    @staticmethod
    def get_by_metadata_prefix_and_registry_id(metadata_prefix, registry_id):
        """
        Return a OaiHarvesterMetadataFormat by metadata_prefix and registry id.
        :param metadata_prefix:
        :param registry_id:
        :return:
        """
        return OaiHarvesterMetadataFormat.objects().get(metadataPrefix=metadata_prefix, registry_id=str(registry_id))

    @staticmethod
    def delete_all_by_registry_id(registry_id):
        """
        Delete all OaiHarvesterMetadataFormat used by a registry
        :param registry_id:
        :return:
        """
        OaiHarvesterMetadataFormat.get_all_by_registry_id(str(registry_id)).delete()

    @staticmethod
    def update_for_all_harvest_by_registry_id(registry_id, harvest):
        """
        Update the harvest for all OaiHarvesterMetadataFormat used by the registry
        :param registry_id:
        :param harvest:
        :return:
        """
        OaiHarvesterMetadataFormat.get_all_by_registry_id(registry_id).update(set__harvest=harvest)

    @staticmethod
    def update_for_all_harvest_by_list_ids(list_oai_metadata_format_ids, harvest):
        """
        Update the harvest for all OaiHarvesterMetadataFormat by a list of ids
        :param list_oai_metadata_format_ids:
        :param harvest:
        :return:
        """
        OaiHarvesterMetadataFormat.get_all_by_list_ids(list_oai_metadata_format_ids).update(set__harvest=harvest)
