# Generated by Django 5.1.1 on 2024-09-28 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("incomes", "0005_delete_credit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="income",
            name="balance",
            field=models.DecimalField(decimal_places=12, max_digits=20),
        ),
    ]
