from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoicing", "0018_rentalproperty_cost_of_money_monthly"),
    ]

    operations = [
        migrations.AddField(
            model_name="rentalproperty",
            name="appreciation_monthly",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="rentalproperty",
            name="total_income",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]


