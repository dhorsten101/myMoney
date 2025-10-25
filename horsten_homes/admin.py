from django.contrib import admin

from horsten_homes.models import Invoice, Property, Door, DoorPipeline, RentalAgent, EstateAgent, ManagingAgent


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	list_display = ("number", "door", "issue_date", "due_date", "status", "total")
	list_filter = ("status", "issue_date", "due_date")
	search_fields = ("number", "door__name")


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
	list_display = ("name", "address", "website", "capital_value", "flow_value", "total_expenses", "income", "cost_of_money_monthly", "appreciation_monthly", "total_income",
		"agent", "estate_agent", "managing_agent")
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


@admin.register(DoorPipeline)
class DoorPipelineAdmin(admin.ModelAdmin):
	list_display = ("title", "url", "status", "created_at")
	list_filter = ("status",)
	search_fields = ("title", "url")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
	list_display = ("name", "created_at")
	search_fields = ("name",)
