from django.contrib import admin

from horsten_homes.models import Invoice, Property, Door, DoorPipeline, RentalAgent, EstateAgent, ManagingAgent, Tenant, PropertyImage, Attorney


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
	list_display = ("name", "property_type", "created_at")
	search_fields = ("name",)


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
	list_display = ("property", "uploaded_at")
	search_fields = ("property__name",)


@admin.register(Attorney)
class AttorneyAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "phone")
	search_fields = ("name", "email", "phone")


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
	list_display = ("name", "door", "move_in_date", "move_out_date", "email", "phone")
	list_filter = ("move_in_date", "move_out_date")
	search_fields = ("name", "email", "phone", "door__name")
