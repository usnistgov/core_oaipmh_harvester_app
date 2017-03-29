"""
    Serializers used throughout the Rest API
"""
from rest_framework.serializers import Serializer, CharField, IntegerField, BooleanField
from rest_framework_mongoengine.serializers import DocumentSerializer
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class BasicSerializer(Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class AddRegistrySerializer(BasicSerializer):
    url = CharField(required=True)
    harvest_rate = IntegerField(required=True)
    harvest = BooleanField(required=True)


class RegistryIdSerializer(BasicSerializer):
    registry_id = CharField(required=True)


class RegistrySerializer(DocumentSerializer):
    class Meta:
        model = OaiRegistry
        fields = "__all__"
        

class UpdateRegistrySerializer(Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        instance.harvest_rate = validated_data.get('harvest_rate', instance.harvest_rate)
        instance.harvest = validated_data.get('harvest', instance.harvest)
        return instance

    registry_id = CharField(required=True)
    harvest_rate = IntegerField(required=True)
    harvest = BooleanField(required=True)


class SelectRegistrySerializer(BasicSerializer):
    registry_name = CharField(required=True)
