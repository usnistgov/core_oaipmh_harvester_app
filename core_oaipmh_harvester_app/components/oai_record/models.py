"""
OaiRecord model
"""

from django_mongoengine import fields, Document
from mongoengine.queryset.base import PULL, CASCADE
from mongoengine import errors as mongoengine_errors
from pymongo import errors as pymongo_errors
from core_oaipmh_harvester_app.components.oai_harvester_set.models import OaiHarvesterSet
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import OaiHarvesterMetadataFormat
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
import re
from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_main_app.commons import exceptions


class OaiRecord(Document):
    """
        A record object
    """
    identifier = fields.StringField()
    datestamp = fields.DateTimeField()
    deleted = fields.BooleanField()
    harvester_sets = fields.ListField(fields.ReferenceField(OaiHarvesterSet, reverse_delete_rule=PULL), blank=True)
    harvester_metadata_format = fields.ReferenceField(OaiHarvesterMetadataFormat, reverse_delete_rule=CASCADE)
    metadata = fields.DictField(blank=True)
    raw = fields.DictField()
    registry = fields.ReferenceField(OaiRegistry, reverse_delete_rule=CASCADE)

    # TODO: Look for a better solution than a copy/paste of the save method.
    # Keep the XML order for the metadata field
    def save(self, metadata=None, force_insert=False, validate=True, clean=True,
             write_concern=None,  cascade=None, cascade_kwargs=None,
             _refs=None, **kwargs):
        """Save the :class:`~mongoengine.Document` to the database. If the
        document already exists, it will be updated, otherwise it will be
        created.

        :param force_insert: only try to create a new document, don't allow
            updates of existing documents
        :param validate: validates the document; set to ``False`` to skip.
        :param clean: call the document clean method, requires `validate` to be
            True.
        :param write_concern: Extra keyword arguments are passed down to
            :meth:`~pymongo.collection.Collection.save` OR
            :meth:`~pymongo.collection.Collection.insert`
            which will be used as options for the resultant
            ``getLastError`` command.  For example,
            ``save(..., write_concern={w: 2, fsync: True}, ...)`` will
            wait until at least two servers have recorded the write and
            will force an fsync on the primary server.
        :param cascade: Sets the flag for cascading saves.  You can set a
            default by setting "cascade" in the document __meta__
        :param cascade_kwargs: (optional) kwargs dictionary to be passed throw
            to cascading saves.  Implies ``cascade=True``.
        :param _refs: A list of processed references used in cascading saves

        .. versionchanged:: 0.5
            In existing documents it only saves changed fields using
            set / unset.  Saves are cascaded and any
            :class:`~bson.dbref.DBRef` objects that have changes are
            saved as well.
        .. versionchanged:: 0.6
            Added cascading saves
        .. versionchanged:: 0.8
            Cascade saves are optional and default to False.  If you want
            fine grain control then you can turn off using document
            meta['cascade'] = True.  Also you can pass different kwargs to
            the cascade save using cascade_kwargs which overwrites the
            existing kwargs with custom values.
        """
        if validate:
            self.validate(clean=clean)

        if write_concern is None:
            write_concern = {"w": 1}

        doc = self.to_mongo()
        doc['metadata'] = metadata

        created = ('_id' not in doc or self._created or force_insert)

        try:
            collection = self._get_collection()

            if created:
                if force_insert:
                    object_id = collection.insert(doc, **write_concern)
                else:
                    object_id = collection.save(doc, **write_concern)
            else:
                object_id = doc['_id']
                updates, removals = self._delta()
                # Need to add shard key to query, or you get an error
                select_dict = {'_id': object_id}
                shard_key = self.__class__._meta.get('shard_key', tuple())
                for k in shard_key:
                    actual_key = self._db_field_map.get(k, k)
                    select_dict[actual_key] = doc[actual_key]

                def is_new_object(last_error):
                    if last_error is not None:
                        updated = last_error.get("updatedExisting")
                        if updated is not None:
                            return not updated
                    return created

                update_query = {}

                if updates:
                    if 'metadata' not in removals:
                        updates['metadata'] = metadata
                    update_query["$set"] = updates
                if removals:
                    update_query["$unset"] = removals
                if updates or removals:
                    last_error = collection.update(select_dict, update_query,
                                                   upsert=True, **write_concern)
                    created = is_new_object(last_error)

            if cascade is None:
                cascade = self._meta.get('cascade', False) or cascade_kwargs is not None

            if cascade:
                kwargs = {
                    "force_insert": force_insert,
                    "validate": validate,
                    "write_concern": write_concern,
                    "cascade": cascade
                }
                if cascade_kwargs:  # Allow granular control over cascades
                    kwargs.update(cascade_kwargs)
                kwargs['_refs'] = _refs
                self.cascade_save(**kwargs)
        except pymongo_errors.DuplicateKeyError, err:
            message = u'Tried to save duplicate unique keys (%s)'
            raise mongoengine_errors.NotUniqueError(message % unicode(err))
        except pymongo_errors.OperationFailure, err:
            message = 'Could not save document (%s)'
            if re.match('^E1100[01] duplicate key', unicode(err)):
                # E11000 - duplicate key error index
                # E11001 - duplicate key on update
                message = u'Tried to save duplicate unique keys (%s)'
                raise mongoengine_errors.NotUniqueError(message % unicode(err))
            raise mongoengine_errors.OperationError(message % unicode(err))
        id_field = self._meta['id_field']
        if id_field not in self._meta.get('shard_key', []):
            self[id_field] = self._fields[id_field].to_python(object_id)

        self._clear_changed_fields()
        self._created = False
        return self

    @staticmethod
    def get_by_id(oai_record_id):
        """Get an OaiRecord by its id.

        Args:
            oai_record_id: Id of the OaiRecord.

        Returns: The OaiRecord instance.

        Raises:
            DoesNotExist: The OaiRecord doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiRecord.objects().get(pk=str(oai_record_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as e:
            raise exceptions.ModelError(e.message)

    @staticmethod
    def get_by_identifier_and_metadata_format(identifier, harvester_metadata_format):
        """Get an OaiRecord by its identifier and metadata format.

        Args:
            identifier: Identifier of the OaiRecord.
            harvester_metadata_format: harvester_metadata_format of the OaiRecord.

        Returns: The OaiRecord instance.

        Raises:
            DoesNotExist: The OaiRecord doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiRecord.objects().get(identifier=identifier, harvester_metadata_format=harvester_metadata_format)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as e:
            raise exceptions.ModelError(e.message)

    @staticmethod
    def get_all():
        """ Return all OaiRecord.

        Returns: List of OaiRecord.

        """
        return OaiRecord.objects().all()

    @staticmethod
    def get_all_by_registry_id(registry_id, order_by_field=None):
        """ Return a list of OaiRecord by registry id. Possibility to order_by the list.

        Args:
            registry_id: The registry id.
            order_by_field: Order field.

        Returns:
            List of OaiRecord.

        """
        return OaiRecord.objects(registry=str(registry_id)).order_by(order_by_field)

    @staticmethod
    def get_count_by_registry_id(registry_id):
        """ Return the number of OaiRecord by registry id.

        Args:
            registry_id: The registry id.

        Returns:
            Number of OaiRecord (int).

        """
        return OaiRecord.objects(registry=str(registry_id)).count()

    @staticmethod
    def delete_all_by_registry_id(registry_id):
        """ Delete all OaiRecord of a registry.

        Args:
            registry_id: The registry id.

        """
        OaiRecord.get_all_by_registry_id(registry_id).delete()

    @staticmethod
    def execute_full_text_query(text, list_metadata_format_id):
        """ Execute full text query on OaiRecord data collection.

        Args:
            text: Keywords.
            list_metadata_format_id: List of metadata format id to search on.

        Returns: List of OaiRecord.

        """
        full_text_query = get_full_text_query(text)
        # only no deleted records, add harvester_metadata_format criteria
        full_text_query.update({'deleted':  False}, {'harvester_metadata_format__id': {'$in': list_metadata_format_id}})

        return OaiRecord.objects.find(full_text_query)

    @staticmethod
    def execute_query(query):
        """Executes a query on the OaiRecord collection.

        Args:
            query: Query to execute.

        Returns:
            Results of the query.

        """
        return OaiRecord.objects(__raw__=query)
