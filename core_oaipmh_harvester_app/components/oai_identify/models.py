"""
OaiIdentify model
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors
from mongoengine.queryset.base import CASCADE

from core_main_app.commons import exceptions
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry


class OaiIdentify(Document):
    """Represents an identify object for Oai-Pmh Harvester"""

    admin_email = fields.StringField(blank=True)
    base_url = fields.URLField(unique=True)
    repository_name = fields.StringField(blank=True)
    deleted_record = fields.StringField(blank=True)
    delimiter = fields.StringField(blank=True)
    description = fields.StringField(blank=True)
    earliest_datestamp = fields.StringField(blank=True)
    granularity = fields.StringField(blank=True)
    oai_identifier = fields.StringField(blank=True)
    protocol_version = fields.StringField(blank=True)
    repository_identifier = fields.StringField(blank=True)
    sample_identifier = fields.StringField(blank=True)
    scheme = fields.StringField(blank=True)
    raw = fields.DictField(blank=True)
    registry = fields.ReferenceField(
        OaiRegistry, reverse_delete_rule=CASCADE, unique=True
    )

    @staticmethod
    def get_by_registry_id(registry_id):
        """Return an OaiIdentify by its registry id.

        Args:
            registry_id:  The registry id.

        Returns:
            OaiIdentify instance.

        Raises:
            DoesNotExist: The OaiIdentify doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiIdentify.objects().get(registry=str(registry_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))
