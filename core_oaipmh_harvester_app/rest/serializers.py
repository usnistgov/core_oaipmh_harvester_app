"""
    Serializers used throughout the Rest API
"""
from rest_framework import serializers
from rest_framework_mongoengine.serializers import MongoEngineModelSerializer
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry

class AddRegistrySerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    harvest_rate = serializers.IntegerField(required=True)
    harvest = serializers.BooleanField(required=True)


class RegistryIdSerializer(serializers.Serializer):
    registry_id = serializers.CharField(required=True)


class RegistrySerializer(MongoEngineModelSerializer):
    class Meta:
        model = OaiRegistry
        

class UpdateRegistrySerializer(serializers.Serializer):
    registry_id = serializers.CharField(required=True)
    harvest_rate = serializers.IntegerField(required=True)
    harvest = serializers.BooleanField(required=True)
