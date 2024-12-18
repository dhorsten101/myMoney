# model.py

from django.db import models


class Sellable(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	price = models.DecimalField(max_digits=20, decimal_places=12, default=0)
	sold_price = models.DecimalField(max_digits=20, decimal_places=12, null=True, default=0)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.name} - {self.price}"


class SellableImage(models.Model):
	sellable = models.ForeignKey(Sellable, related_name="images", on_delete=models.CASCADE)
	image = models.ImageField(upload_to="sellable_images/")
	uploaded_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"Image for {self.sellable.name}"
