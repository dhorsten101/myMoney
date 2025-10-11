from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoicing", "0017_rentalpropertypipelineimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="rentalproperty",
            name="cost_of_money_monthly",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]


