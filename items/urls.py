from django.urls import path

from items import views


urlpatterns = [
	path("items/", views.item_list, name="item_list"),
	path("items/new/", views.item_create, name="item_create"),
	path("items/<int:id>/", views.item_detail, name="item_detail"),
	path("items/<int:id>/edit/", views.item_update, name="item_update"),
	path("items/<int:id>/delete/", views.item_delete, name="item_delete"),

	path("items/sku-catalog/", views.sku_catalog_list, name="sku_catalog_list"),
	path("items/sku-catalog/new/", views.sku_catalog_create, name="sku_catalog_create"),
	path("items/sku-catalog/<int:id>/", views.sku_catalog_detail, name="sku_catalog_detail"),
	path("items/sku-catalog/<int:id>/edit/", views.sku_catalog_update, name="sku_catalog_update"),
	path("items/sku-catalog/<int:id>/delete/", views.sku_catalog_delete, name="sku_catalog_delete"),
]

