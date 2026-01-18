from django.conf import settings
from django.db import models


class SkuCatalog(models.Model):
	sku = models.CharField(max_length=64, unique=True)
	description = models.CharField(max_length=255)
	model = models.CharField(max_length=128, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["sku"]

	def __str__(self) -> str:
		return f"{self.sku} — {self.description}"


class Item(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="items",
	)
	name = models.CharField(max_length=200)
	sku_catalog = models.ForeignKey(SkuCatalog, null=True, blank=True, on_delete=models.SET_NULL, related_name="items")
	sku = models.CharField(max_length=64, blank=True)
	model = models.CharField(max_length=128, blank=True)
	sku_description = models.CharField(max_length=255, blank=True)
	quantity = models.PositiveIntegerField(default=0)
	notes = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["name", "-updated_at", "-id"]

	def __str__(self) -> str:
		return f"{self.name} ({self.quantity})"
