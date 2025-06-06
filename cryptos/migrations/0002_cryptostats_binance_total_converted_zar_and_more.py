# Generated by Django 5.1.7 on 2025-05-31 18:47

from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		("cryptos", "0001_initial"),
	]
	
	operations = [
		migrations.AddField(
			model_name="cryptostats",
			name="binance_total_converted_zar",
			field=models.DecimalField(
				blank=True, decimal_places=2, max_digits=20, null=True
			),
		),
		migrations.AddField(
			model_name="cryptostats",
			name="luno_total_converted_zar",
			field=models.DecimalField(
				blank=True, decimal_places=2, max_digits=20, null=True
			),
		),
	]
