from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("horsten_homes", "0003_merge_20251117_2152"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="previous_sold_value",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]


