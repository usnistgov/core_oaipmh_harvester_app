""" Mongoengine OaiRecord model
"""
import logging

from django.db.models.signals import post_save, post_delete

from core_main_app.commons.exceptions import CoreError
from core_main_app.settings import (
    MONGODB_INDEXING,
    SEARCHABLE_DATA_OCCURRENCES_LIMIT,
    MONGODB_ASYNC_SAVE,
)
from core_main_app.utils import xml as xml_utils
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.tasks import (
    index_mongo_oai_record,
    delete_mongo_oai_record,
)

logger = logging.getLogger(__name__)


try:
    if MONGODB_INDEXING:
        from mongoengine import Document, DoesNotExist
        from mongoengine import fields as mongo_fields
        from core_main_app.utils.databases.mongo.pymongo_database import init_text_index
        from core_main_app.components.mongo.models import AbstractMongoData

        class MongoOaiRecord(AbstractMongoData):
            identifier = mongo_fields.StringField()
            deleted = mongo_fields.BooleanField()
            _harvester_sets_ids = mongo_fields.ListField(db_field="harvester_sets")
            _harvester_metadata_format_id = mongo_fields.IntField(
                db_field="harvester_metadata_format"
            )
            _registry_id = mongo_fields.IntField(db_field="registry")
            _xml_content = None

            @property
            def harvester_metadata_format(self):
                return OaiHarvesterMetadataFormat.get_by_id(
                    self._harvester_metadata_format_id
                )

            @property
            def xml_content(self):
                """Get xml content - read from data.

                Returns:

                """
                if not self._xml_content:
                    self._xml_content = OaiRecord.get_by_id(self.data_id).xml_content
                return self._xml_content

            @xml_content.setter
            def xml_content(self, value):
                """Set xml content - to be saved as a file.

                Args:
                    value:

                Returns:

                """
                self._xml_content = value

            @staticmethod
            def execute_query(query, order_by_field):
                """Executes a query on the OaiRecord collection.

                Args:
                    query: Query to execute.
                    order_by_field: Order by Data field

                Returns:
                    Results of the query.

                """
                return MongoOaiRecord.objects(__raw__=query).order_by(*order_by_field)

            @staticmethod
            def aggregate(pipeline):
                """Execute an aggregate on the Data collection.

                Args:
                    pipeline:

                Returns:

                """
                return MongoOaiRecord.objects.aggregate(*pipeline)

            @staticmethod
            def init_mongo_oai_record(oai_record):
                """Initialize mongo oai_record from OaiRecord

                Args:
                    oai_record:

                Returns:

                """
                try:
                    # check if oai_record already exists in mongo
                    mongo_oai_record = MongoOaiRecord.objects.get(pk=oai_record.id)
                except DoesNotExist:
                    # create new mongo oai_record otherwise
                    mongo_oai_record = MongoOaiRecord()

                mongo_oai_record.data_id = oai_record.id
                mongo_oai_record.title = oai_record.title
                mongo_oai_record.dict_content = xml_utils.raw_xml_to_dict(
                    oai_record.xml_content,
                    xml_utils.post_processor,
                    list_limit=SEARCHABLE_DATA_OCCURRENCES_LIMIT,
                )
                mongo_oai_record.creation_date = oai_record.creation_date
                mongo_oai_record.last_modification_date = (
                    oai_record.last_modification_date
                )
                mongo_oai_record.last_change_date = oai_record.last_change_date

                mongo_oai_record.identifier = oai_record.identifier
                mongo_oai_record.deleted = oai_record.deleted
                mongo_oai_record._harvester_sets_ids = list(
                    oai_record.harvester_sets.values_list("id", flat=True)
                )
                mongo_oai_record._harvester_metadata_format_id = (
                    oai_record.harvester_metadata_format.id
                    if oai_record.harvester_metadata_format
                    else None
                )
                mongo_oai_record._registry_id = (
                    oai_record.registry.id if oai_record.registry else None
                )

                return mongo_oai_record

            @staticmethod
            def post_save_data(sender, instance, **kwargs):
                """Method executed after a saving of a Data object.
                Args:
                    sender: Class.
                    instance: Data document.
                    **kwargs: Args.

                """
                if MONGODB_ASYNC_SAVE:
                    index_mongo_oai_record.apply_async((str(instance.id),))
                else:
                    mongo_oai_record = MongoOaiRecord.init_mongo_oai_record(instance)
                    mongo_oai_record.save()

            @staticmethod
            def post_delete_data(sender, instance, **kwargs):
                """Method executed after a deleting of a Data object.
                Args:
                    sender: Class.
                    instance: Data document.
                    **kwargs: Args.

                """
                if MONGODB_ASYNC_SAVE:
                    delete_mongo_oai_record.apply_async((str(instance.id),))
                else:
                    try:
                        # check if data already exists in mongo
                        mongo_oai_record = MongoOaiRecord.objects.get(
                            data_id=instance.id
                        )
                        mongo_oai_record.delete()
                    except DoesNotExist:
                        logger.warning(
                            f"Trying to delete {str(instance.id)} but document was not found."
                        )
                    except Exception as e:
                        logger.error(f"An unexpected error occurred: {str(e)}")

        # Initialize text index
        init_text_index(MongoOaiRecord)
        # connect sync method to OaiRecord post save
        post_save.connect(MongoOaiRecord.post_save_data, sender=OaiRecord)
        # connect sync method to OaiRecord post delete
        post_delete.connect(MongoOaiRecord.post_delete_data, sender=OaiRecord)
except ImportError as e:
    raise CoreError(
        "Mongoengine needs to be installed when MongoDB indexing is enabled. "
        "Install required python packages (see requirements.mongo.txt) "
        "or disable MongoDB indexing (MONGODB_INDEXING=False). "
    )
