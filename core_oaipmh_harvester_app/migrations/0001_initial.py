# Generated by Django 3.2 on 2021-12-01 14:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core_main_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OaiHarvesterMetadataFormat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("metadata_prefix", models.CharField(max_length=200)),
                ("schema", models.CharField(max_length=200)),
                ("xml_schema", models.TextField(blank=True)),
                ("metadata_namespace", models.CharField(max_length=200)),
                ("raw", models.JSONField()),
                ("hash", models.CharField(max_length=200)),
                ("harvest", models.BooleanField(default=False)),
                ("last_update", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="OaiHarvesterSet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("set_spec", models.CharField(max_length=200)),
                ("set_name", models.CharField(max_length=200)),
                ("raw", models.JSONField()),
                ("harvest", models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="OaiRegistry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("url", models.URLField(unique=True)),
                (
                    "harvest_rate",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("description", models.TextField(blank=True, default="", null=True)),
                ("harvest", models.BooleanField(default=False)),
                ("last_update", models.DateTimeField(blank=True, null=True)),
                ("is_harvesting", models.BooleanField(default=False)),
                ("is_updating", models.BooleanField(default=False)),
                ("is_activated", models.BooleanField(default=True)),
                ("is_queued", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="OaiRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dict_content", models.JSONField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        max_length=200,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_title",
                                message="Title must not be empty or only whitespaces",
                                regex=".*\\S.*",
                            )
                        ],
                    ),
                ),
                ("xml_file", models.TextField()),
                (
                    "creation_date",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "last_modification_date",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "last_change_date",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("identifier", models.CharField(max_length=200)),
                ("deleted", models.BooleanField()),
                (
                    "harvester_metadata_format",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_oaipmh_harvester_app.oaiharvestermetadataformat",
                    ),
                ),
                (
                    "harvester_sets",
                    models.ManyToManyField(
                        blank=True, to="core_oaipmh_harvester_app.OaiHarvesterSet"
                    ),
                ),
                (
                    "registry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_oaipmh_harvester_app.oairegistry",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OaiIdentify",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "admin_email",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("base_url", models.URLField(unique=True)),
                (
                    "repository_name",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "deleted_record",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("delimiter", models.CharField(blank=True, max_length=200, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "earliest_datestamp",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "granularity",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "oai_identifier",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "protocol_version",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "repository_identifier",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "sample_identifier",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("scheme", models.CharField(blank=True, max_length=200, null=True)),
                ("raw", models.JSONField(blank=True, null=True)),
                (
                    "registry",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_oaipmh_harvester_app.oairegistry",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="oaiharvesterset",
            name="registry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core_oaipmh_harvester_app.oairegistry",
            ),
        ),
        migrations.AddField(
            model_name="oaiharvestermetadataformat",
            name="registry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core_oaipmh_harvester_app.oairegistry",
            ),
        ),
        migrations.AddField(
            model_name="oaiharvestermetadataformat",
            name="template",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core_main_app.template",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="oaiharvesterset",
            unique_together={("registry", "set_spec")},
        ),
        migrations.CreateModel(
            name="OaiHarvesterMetadataFormatSet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("last_update", models.DateTimeField(blank=True, null=True)),
                (
                    "harvester_metadata_format",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_oaipmh_harvester_app.oaiharvestermetadataformat",
                    ),
                ),
                (
                    "harvester_set",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_oaipmh_harvester_app.oaiharvesterset",
                    ),
                ),
            ],
            options={
                "unique_together": {("harvester_metadata_format", "harvester_set")},
            },
        ),
        migrations.AlterUniqueTogether(
            name="oaiharvestermetadataformat",
            unique_together={("registry", "metadata_prefix")},
        ),
    ]
