from django.contrib import admin

from contractors.models import Contractor


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
	list_display = ("name", "company", "service_category", "email", "phone", "created_at")
	search_fields = ("name", "company", "service_category", "email", "phone")
