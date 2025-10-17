from django.contrib import admin

from invoicing.models import Invoice, RentalProperty, RentalPropertyPipeline, RentalAgent, EstateAgent, ManagingAgent


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	list_display = ("number", "rental_property", "issue_date", "due_date", "status", "total")
	list_filter = ("status", "issue_date", "due_date")
	search_fields = ("number", "rental_property__name")


@admin.register(RentalProperty)
class RentalPropertyAdmin(admin.ModelAdmin):
	list_display = ("name", "address", "website", "capital_value", "flow_value", "total_expenses", "income", "cost_of_money_monthly", "appreciation_monthly", "total_income", "agent", "estate_agent", "managing_agent")
	search_fields = ("name", "address")
@admin.register(RentalAgent)
class RentalAgentAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "phone")
	search_fields = ("name", "email", "phone")

@admin.register(EstateAgent)
class EstateAgentAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "phone")
	search_fields = ("name", "email", "phone")

@admin.register(ManagingAgent)
class ManagingAgentAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "phone")
	search_fields = ("name", "email", "phone")


@admin.register(RentalPropertyPipeline)
class RentalPropertyPipelineAdmin(admin.ModelAdmin):
	list_display = ("title", "url", "status", "created_at")
	list_filter = ("status",)
	search_fields = ("title", "url")
