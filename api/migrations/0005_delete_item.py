# Generated by Django 5.1.1 on 2024-09-13 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_item"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Item",
        ),
    ]
