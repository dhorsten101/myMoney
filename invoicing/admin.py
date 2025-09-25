from django.contrib import admin

from invoicing.models import Invoice, RentalProperty


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "customer_name", "issue_date", "due_date", "status", "total")
    list_filter = ("status", "issue_date", "due_date")
    search_fields = ("number", "customer_name", "customer_email")


@admin.register(RentalProperty)
class RentalPropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "capital_value", "flow_value", "cost_value")
    search_fields = ("name", "address")


