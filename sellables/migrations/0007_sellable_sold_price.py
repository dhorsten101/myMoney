# Generated by Django 5.1.1 on 2024-09-29 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sellables", "0006_remove_sellable_sold_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="sellable",
            name="sold_price",
            field=models.DecimalField(decimal_places=12, max_digits=20, null=True),
        ),
    ]
