# Generated by Django 5.1.7 on 2025-04-02 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0004_alter_asset_converted_usd_alter_asset_converted_zar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="balance",
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
    ]
