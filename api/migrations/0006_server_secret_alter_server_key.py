# Generated by Django 4.2.4 on 2023-08-05 12:47

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_rename_public_key_server_key"),
    ]

    operations = [
        migrations.AddField(
            model_name="server",
            name="secret",
            field=models.CharField(
                blank=True,
                default=api.models.generate_secret,
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="server",
            name="key",
            field=models.CharField(
                blank=True, default=api.models.generate_key, max_length=64, null=True
            ),
        ),
    ]