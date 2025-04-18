# Generated by Django 5.1.4 on 2025-01-25 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Asset",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "price",
                    models.DecimalField(decimal_places=8, max_digits=20, null=True),
                ),
                ("exchange", models.CharField(max_length=50)),
                ("balance", models.DecimalField(decimal_places=6, max_digits=10)),
                ("account_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "converted_zar",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                (
                    "converted_usd",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
