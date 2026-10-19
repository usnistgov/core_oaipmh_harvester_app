"""Dedupe OaiRecord rows sharing (identifier, harvester_metadata_format).

Required before the next migration (`0006_oairecord_unique_together`) can add a
unique_together constraint on those fields. For each duplicate group, keeps the row with
the latest last_modification_date (falling back to the highest pk) and deletes the rest.
"""

from django.db import migrations


def dedupe_oai_records(apps, schema_editor):
    OaiRecord = apps.get_model("core_oaipmh_harvester_app", "OaiRecord")

    seen = {}
    for record in OaiRecord.objects.all().order_by(
        "identifier",
        "harvester_metadata_format_id",
        "-last_modification_date",
        "-pk",
    ):
        key = (record.identifier, record.harvester_metadata_format_id)
        if key in seen:
            record.delete()
        else:
            seen[key] = record.pk


def noop_reverse(apps, schema_editor):
    """No-op: deleted duplicate rows can't be restored."""


class Migration(migrations.Migration):

    dependencies = [
        ("core_oaipmh_harvester_app", "0004_file_history"),
    ]

    operations = [
        migrations.RunPython(dedupe_oai_records, noop_reverse),
    ]
