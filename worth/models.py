from django.db import models


class Worth(models.Model):
	CATEGORY_CHOICES = [
		("real_estate", "Real Estate"),
		("cash", "Cash"),
		("investments", "Investments"),
		("shares", "Shares"),
		("valuables", "Valuables"),
		("crypto", "Crypto"),
	]
	
	name = models.CharField(max_length=100)
	quick_value = models.DecimalField(max_digits=20, decimal_places=2)
	real_value = models.DecimalField(max_digits=20, decimal_places=2)
	notes = models.TextField()
	category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.name}"
