# Generated by Django 5.1.1 on 2024-09-14 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0011_alter_asset_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="balance",
            field=models.DecimalField(decimal_places=6, max_digits=10),
        ),
    ]