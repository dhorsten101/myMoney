# Generated by Django 5.1.1 on 2024-09-28 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sellables", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sellable",
            name="balance",
            field=models.DecimalField(decimal_places=6, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
