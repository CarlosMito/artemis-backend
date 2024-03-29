# Generated by Django 4.2.1 on 2023-06-03 14:28

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Input",
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
                ("prompt", models.TextField()),
                ("negative_prompt", models.TextField(blank=True, null=True)),
                ("image_dimensions", models.CharField(max_length=32)),
                ("num_outputs", models.IntegerField()),
                ("num_inference_steps", models.PositiveIntegerField()),
                ("guidance_scale", models.FloatField()),
                ("scheduler", models.CharField(max_length=128)),
                ("seed", models.BigIntegerField()),
                ("style", models.CharField(blank=True, max_length=64, null=True)),
                ("saturation", models.CharField(blank=True, max_length=64, null=True)),
                ("value", models.CharField(blank=True, max_length=64, null=True)),
                ("color", models.CharField(blank=True, max_length=64, null=True)),
                ("replicate_id", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("username", models.CharField(max_length=512)),
                ("password", models.CharField(max_length=512)),
                ("email", models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name="Output",
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
                ("image", models.ImageField(upload_to=api.models.Output.upload_to)),
                ("is_public", models.BooleanField(default=False)),
                ("favorite_count", models.IntegerField(default=0)),
                (
                    "input",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="outputs",
                        to="api.input",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="input",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="api.user"
            ),
        ),
    ]
