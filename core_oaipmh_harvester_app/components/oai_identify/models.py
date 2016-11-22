"""
OaiIdentify model
"""

from django_mongoengine import fields, Document


class OaiIdentify(Document):
    """Represents an identify object for Oai-Pmh Harvester"""
    admin_email = fields.StringField(required=False)
    base_url = fields.URLField(required=True, unique=True)
    repository_name = fields.StringField(required=False)
    deleted_record = fields.StringField(required=False)
    delimiter = fields.StringField(required=False)
    description = fields.StringField(required=False)
    earliest_datestamp = fields.StringField(required=False)
    granularity = fields.StringField(required=False)
    oai_identifier = fields.StringField(required=False)
    protocol_version = fields.StringField(required=False)
    repository_identifier = fields.StringField(required=False)
    sample_identifier = fields.StringField(required=False)
    scheme = fields.StringField(required=False)
    raw = fields.DictField(required=False)
