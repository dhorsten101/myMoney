from django.db import models


class CryptoStats(models.Model):
	total_value = models.DecimalField(max_digits=20, decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True)
