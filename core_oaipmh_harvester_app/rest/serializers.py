"""
    Serializers used throughout the Rest API
"""
from rest_framework import serializers

from core_main_app.commons.serializers import BasicSerializer
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_registry import (
    api as oai_registry_api,
)
from core_oaipmh_harvester_app.components.oai_registry.models import (
    OaiRegistry,
)


class RegistrySerializer(serializers.ModelSerializer):
    """Registry Serializer"""

    class Meta:
        """Meta"""

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
        """create

        Args:
            validated_data:

        Returns:

        """
        return oai_registry_api.add_registry_by_url(
            **validated_data, request=self.context["request"]
        )


class UpdateRegistrySerializer(BasicSerializer):
    """Update Registry Serializer"""

    def update(self, instance, validated_data):
        """update

        Args:
            instance
            validated_data:

        Returns:

        """
        instance.harvest_rate = validated_data.get(
            "harvest_rate", instance.harvest_rate
        )
        instance.harvest = validated_data.get("harvest", instance.harvest)
        return oai_registry_api.upsert(instance)

    harvest_rate = serializers.IntegerField(required=True)
    harvest = serializers.BooleanField(required=True)


class HarvestSerializer(BasicSerializer):
    """Harvest Serializer"""

    metadata_formats = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    sets = serializers.ListField(child=serializers.CharField(), required=False)


class OaiRecordSerializer(serializers.ModelSerializer):
    """OaiRecord serializer"""

    xml_content = serializers.CharField()

    class Meta:
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
