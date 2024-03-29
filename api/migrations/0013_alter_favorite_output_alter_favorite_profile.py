# Generated by Django 4.2.1 on 2023-06-23 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0012_favorite_timestamp_profile_favorites"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favorite",
            name="output",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.output"
            ),
        ),
        migrations.AlterField(
            model_name="favorite",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.profile"
            ),
        ),
    ]
