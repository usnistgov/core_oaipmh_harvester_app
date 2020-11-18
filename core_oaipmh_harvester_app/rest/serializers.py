"""
    Serializers used throughout the Rest API
"""

from rest_framework.serializers import CharField, IntegerField, BooleanField, ListField
from rest_framework_mongoengine.serializers import DocumentSerializer

from core_main_app.commons.serializers import BasicSerializer
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_registry import api as oai_registry_api
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class RegistrySerializer(DocumentSerializer):
    class Meta(object):
        model = OaiRegistry
        fields = "__all__"

        read_only_fields = (
            "id",
            "name",
            "description",
            "last_update",
            "is_harvesting",
            "is_updating",
            "is_activated",
            "is_queued",
        )

    def create(self, validated_data):
        return oai_registry_api.add_registry_by_url(
            **validated_data, request=self.context["request"]
        )


class UpdateRegistrySerializer(BasicSerializer):
    def update(self, instance, validated_data):
        instance.harvest_rate = validated_data.get(
            "harvest_rate", instance.harvest_rate
        )
        instance.harvest = validated_data.get("harvest", instance.harvest)
        return oai_registry_api.upsert(instance)

    harvest_rate = IntegerField(required=True)
    harvest = BooleanField(required=True)


class HarvestSerializer(BasicSerializer):
    metadata_formats = ListField(child=CharField(), required=False)
    sets = ListField(child=CharField(), required=False)


class OaiRecordSerializer(DocumentSerializer):
    """OaiRecord serializer"""

    xml_content = CharField()

    class Meta(object):
        """Meta"""

        model = OaiRecord
        fields = [
            "identifier",
            "registry",
            "harvester_sets",
            "harvester_metadata_format",
            "title",
            "xml_content",
            "last_modification_date",
        ]
