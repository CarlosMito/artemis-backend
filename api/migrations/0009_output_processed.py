# Generated by Django 4.2.1 on 2023-06-12 20:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0008_alter_input_color_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="output",
            name="processed",
            field=models.BooleanField(default=False),
        ),
    ]
