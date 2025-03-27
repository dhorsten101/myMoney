from django.db import models


class Weight(models.Model):
	weight = models.DecimalField(max_digits=20, decimal_places=2)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.weight}"
