# Generated by Django 4.2.1 on 2023-06-03 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="input",
            name="version",
            field=models.CharField(
                default="db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                max_length=128,
            ),
            preserve_default=False,
        ),
    ]
