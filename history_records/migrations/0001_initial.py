# Generated by Django 5.1.1 on 2024-09-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HistoryRecord",
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
                ("total_value", models.DecimalField(decimal_places=2, max_digits=20)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("crypto", "Crypto"),
                            ("assets", "Assets"),
                            ("expenses", "Expenses"),
                        ],
                        max_length=50,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]