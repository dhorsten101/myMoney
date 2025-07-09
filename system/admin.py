from django.contrib import admin

from .models import DeploymentLog


@admin.register(DeploymentLog)
class DeploymentLogAdmin(admin.ModelAdmin):
	list_display = ('version', 'branch', 'commit', 'deployed_by', 'deployed_at')
	list_filter = ('branch', 'deployed_by')
	search_fields = ('version', 'message', 'commit')
