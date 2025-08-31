from django.contrib import admin

from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
	list_display = ("title", "due_at", "severity", "is_active", "sent_at")
	list_filter = ("severity", "is_active")
	search_fields = ("title", "description", "source_app", "source_id")
	ordering = ("-due_at",)


