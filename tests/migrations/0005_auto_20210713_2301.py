# Generated by Django 3.2.4 on 2021-06-19 08:26

from django.db import migrations, models

import tag_fields.managers


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0004_auto_20210619_0826"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderedModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tags",
                    tag_fields.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="tag_fields.TaggedItem",
                        to="tag_fields.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
        ),
    ]
