"""
    Serializers used throughout the Rest API
"""
from rest_framework.serializers import Serializer, CharField, IntegerField, BooleanField
from rest_framework_mongoengine.serializers import DocumentSerializer
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class AddRegistrySerializer(Serializer):
    url = CharField(required=True)
    harvest_rate = IntegerField(required=True)
    harvest = BooleanField(required=True)


class RegistryIdSerializer(Serializer):
    registry_id = CharField(required=True)


class RegistrySerializer(DocumentSerializer):
    class Meta:
        model = OaiRegistry
        fields = "__all__"
        

class UpdateRegistrySerializer(Serializer):
    registry_id = CharField(required=True)
    harvest_rate = IntegerField(required=True)
    harvest = BooleanField(required=True)


class SelectRegistrySerializer(Serializer):
    registry_name = CharField(required=True)
