# Generated by Django 5.1.1 on 2024-09-24 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("incomes", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="income",
            name="account_id",
        ),
    ]
