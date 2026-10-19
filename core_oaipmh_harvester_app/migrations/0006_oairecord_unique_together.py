from django.db import migrations


class Migration(migrations.Migration):
    """Adds the unique_together constraint on (identifier, harvester_metadata_format).
    Must be run after `0005_dedupe_oairecord_identifier_metadata_format` to prevent
    duplicate rows.
    """

    dependencies = [
        (
            "core_oaipmh_harvester_app",
            "0005_dedupe_oairecord_identifier_metadata_format",
        ),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="oairecord",
            unique_together={("identifier", "harvester_metadata_format")},
        ),
    ]
