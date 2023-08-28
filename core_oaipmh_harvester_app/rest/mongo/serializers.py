""" Serializers for MongoDB
"""
from rest_framework import serializers

from core_main_app.rest.data.serializers import ContentField
from core_main_app.settings import BACKWARD_COMPATIBILITY_DATA_XML_CONTENT


class MongoOaiRecordSerializer(serializers.Serializer):
    """MongoOaiRecord serializer"""

    identifier = serializers.CharField()
    registry = serializers.SerializerMethodField()
    harvester_sets = serializers.SerializerMethodField()
    harvester_metadata_format = serializers.SerializerMethodField()
    title = serializers.CharField()
    last_modification_date = serializers.DateTimeField()

    if BACKWARD_COMPATIBILITY_DATA_XML_CONTENT:
        xml_content = ContentField()
    else:
        content = ContentField()

    class Meta:
        """Meta"""

        fields = [
            "identifier",
            "registry",
            "harvester_sets",
            "harvester_metadata_format",
            "title",
            "last_modification_date",
        ]

        if BACKWARD_COMPATIBILITY_DATA_XML_CONTENT:
            fields.append("xml_content")
        else:
            fields.append("content")

    def get_registry(self, obj):
        return obj._registry_id

    def get_harvester_sets(self, obj):
        return obj._harvester_sets_ids

    def get_harvester_metadata_format(self, obj):
        return obj._harvester_metadata_format_id

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
