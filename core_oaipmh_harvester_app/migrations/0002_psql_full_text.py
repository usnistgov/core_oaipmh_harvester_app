# Generated by Django 3.2.10 on 2022-03-08 15:39

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations

from core_main_app.settings import MONGODB_INDEXING
from core_main_app.utils.databases.backend import uses_postgresql_backend


class Migration(migrations.Migration):

    dependencies = [
        ("core_oaipmh_harvester_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="oairecord",
            name="vector_column",
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name="oairecord",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["vector_column"], name="core_oaipmh_vector__7042d7_gin"
            ),
        ),
    ]
    if uses_postgresql_backend() and not MONGODB_INDEXING:
        operations.append(
            migrations.RunSQL(
                sql="""
                  CREATE TRIGGER oai_vector_column_trigger
                  BEFORE INSERT OR UPDATE OF xml_file, vector_column
                  ON core_oaipmh_harvester_app_oairecord
                  FOR EACH ROW EXECUTE PROCEDURE
                  tsvector_update_trigger(
                    vector_column, 'pg_catalog.english', xml_file
                  );

                  UPDATE core_oaipmh_harvester_app_oairecord SET vector_column = NULL;
                """,
                reverse_sql="""
                  DROP TRIGGER IF EXISTS oai_vector_column_trigger
                  ON core_oaipmh_harvester_app_oairecord;
                """,
            )
        )
