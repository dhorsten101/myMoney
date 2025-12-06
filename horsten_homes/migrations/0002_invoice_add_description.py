from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("horsten_homes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="description",
            field=models.CharField(max_length=255, blank=True),
        ),
    ]




