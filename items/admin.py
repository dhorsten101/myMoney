from django.contrib import admin

from items.models import Item, SkuCatalog


@admin.register(SkuCatalog)
class SkuCatalogAdmin(admin.ModelAdmin):
	list_display = ("sku", "description", "model", "updated_at")
	search_fields = ("sku", "description", "model")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ("name", "sku", "model", "quantity", "is_active", "user", "updated_at")
	list_filter = ("is_active",)
	search_fields = ("name", "notes", "user__username", "user__email")
