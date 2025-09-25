from django.urls import path

from invoicing import views


urlpatterns = [
    path("homes/", views.homes_dashboard, name="homes_dashboard"),
    path("invoice/", views.invoice_list, name="invoice_list"),
    path("invoice/new/", views.invoice_create, name="invoice_create"),
    path("invoice/<int:id>/", views.invoice_detail, name="invoice_detail"),
    path("invoice/<int:id>/edit/", views.invoice_update, name="invoice_update"),
    path("invoice/<int:id>/delete/", views.invoice_delete, name="invoice_delete"),
    path("invoice/monthly/", views.invoice_monthly_totals, name="invoice_monthly_totals"),

    path("rental/", views.rental_property_list, name="rental_property_list"),
    path("rental/new/", views.rental_property_create, name="rental_property_create"),
    path("rental/<int:id>/", views.rental_property_detail, name="rental_property_detail"),
    path("rental/<int:id>/edit/", views.rental_property_update, name="rental_property_update"),
    path("rental/<int:id>/delete/", views.rental_property_delete, name="rental_property_delete"),
]


