"""MongoOaiRecord api
"""
from core_main_app.access_control import api as main_access_control_api
from core_main_app.access_control.decorators import access_control
from core_main_app.settings import DATA_SORTING_FIELDS, MONGODB_INDEXING

if MONGODB_INDEXING:
    from core_oaipmh_harvester_app.components.mongo.models import (
        MongoOaiRecord,
    )


@access_control(main_access_control_api.can_anonymous_access_public_data)
def execute_mongo_query(query, user, order_by_field=DATA_SORTING_FIELDS):
    """Executes a query on the OaiRecord collection.

    Args:
        query: Query to execute.
        user: User executing the query
        order_by_field: Order by Data field

    Returns:
        Results of the query.

    """
    return MongoOaiRecord.execute_query(query, order_by_field=order_by_field)


@access_control(main_access_control_api.can_anonymous_access_public_data)
def aggregate(pipeline, user):
    """Execute an aggregate on the OaiRecord collection.

    Args:
        pipeline:

    Returns:

    """
    return MongoOaiRecord.aggregate(pipeline)
