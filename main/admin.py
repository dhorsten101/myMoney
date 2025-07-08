import subprocess

from django.contrib import admin

from .models import ErrorLog, AuditLog
from .models import UMLTool


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


@admin.register(UMLTool)
class UMLToolAdmin(admin.ModelAdmin):
	change_list_template = "uml_change_list.html"
	
	def changelist_view(self, request, extra_context=None):
		if 'run' in request.GET:
			subprocess.call(["python", "manage.py", "generate_schema"])
			self.message_user(request, "✅ UML Diagram has been generated.")
		return super().changelist_view(request, extra_context=extra_context)
