# Generated by Django 5.1.7 on 2025-03-30 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ideas", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="idea",
            name="description",
            field=models.TextField(max_length=200),
        ),
    ]
