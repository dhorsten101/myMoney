# Register your models here.
# admin.py

from django.contrib import admin

from .models import ErrorLog, AuditLog


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
	list_display = ('method', 'path', 'status_code', 'timestamp')
	search_fields = ('path', 'message')
	ordering = ('-timestamp',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
	list_display = ('user', 'model_name', 'timestamp')
	search_fields = ('model_name', 'action')
	ordering = ('-timestamp',)
