# Generated by Django 5.1.1 on 2024-09-28 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sellables", "0002_sellable_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sellable",
            name="sold_price",
            field=models.DecimalField(decimal_places=12, max_digits=20, null=True),
        ),
    ]