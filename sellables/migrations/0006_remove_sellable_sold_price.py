# Generated by Django 5.1.1 on 2024-09-28 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sellables", "0005_remove_sellable_condition"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sellable",
            name="sold_price",
        ),
    ]