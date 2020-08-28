"""
    Sickle serializers
"""

from rest_framework import serializers


class IdentifySerializer(serializers.Serializer):
    """Identify serializer."""

    adminEmail = serializers.CharField(required=False)
    baseURL = serializers.URLField(required=True)
    repositoryName = serializers.CharField(required=False)
    deletedRecord = serializers.CharField(required=False)
    delimiter = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    earliestDatestamp = serializers.CharField(required=False)
    granularity = serializers.CharField(required=False)
    oai_identifier = serializers.CharField(required=False)
    protocolVersion = serializers.CharField(required=False)
    repositoryIdentifier = serializers.CharField(required=True)
    sampleIdentifier = serializers.CharField(required=False)
    scheme = serializers.CharField(required=False)
    raw = serializers.CharField(required=False)


class SetSerializer(serializers.Serializer):
    """Set serializer."""

    setName = serializers.CharField()
    setSpec = serializers.CharField()
    raw = serializers.CharField()


class MetadataFormatSerializer(serializers.Serializer):
    """MetadataFormat serializer."""

    metadataPrefix = serializers.CharField()
    metadataNamespace = serializers.CharField()
    schema = serializers.CharField()
    raw = serializers.CharField()
