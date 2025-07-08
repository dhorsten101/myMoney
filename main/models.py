from django.db import models
from django.utils.timezone import now
from django_common.auth_backends import User


# Create your models here.

class ErrorLog(models.Model):
	method = models.CharField(max_length=10)
	status_code = models.IntegerField(null=True, blank=True)
	message = models.TextField()
	path = models.CharField(max_length=255)
	severity = models.CharField(max_length=10, choices=[("INFO", "Info"), ("ERROR", "Error"), ("CRITICAL", "Critical")])
	level = models.CharField(max_length=50)
	pathname = models.TextField(null=True, blank=True)
	lineno = models.IntegerField(null=True, blank=True)
	func_name = models.CharField(max_length=255, null=True, blank=True)
	module = models.CharField(max_length=100, blank=True, null=True)
	exception = models.TextField(blank=True, null=True)
	object_id = models.CharField(max_length=128, blank=True, null=True)
	exception_type = models.CharField(max_length=255, blank=True, null=True)
	exception_value = models.TextField(blank=True, null=True)
	traceback = models.TextField(blank=True, null=True)
	user = models.CharField(max_length=255, blank=True, null=True)
	ip_address = models.GenericIPAddressField(blank=True, null=True)
	user_agent = models.TextField(blank=True, null=True)
	view_name = models.CharField(max_length=255, blank=True, null=True)
	request_body = models.TextField(blank=True, null=True)
	headers = models.TextField(blank=True, null=True)
	
	timestamp = models.DateTimeField(default=now)
	created_at = models.DateTimeField(default=now)
	
	def __str__(self):
		return f"{self.level}: {self.message[:50]}"


class ExternalServiceLog(models.Model):
	name = models.CharField(max_length=100, help_text="Service name (e.g. ZenQuotes)")
	url = models.URLField(max_length=500)
	method = models.CharField(max_length=10, default='GET')
	status_code = models.IntegerField(null=True, blank=True)
	response_time_ms = models.FloatField(null=True, blank=True)
	execution_time_ms = models.FloatField(null=True, blank=True)
	response_success = models.BooleanField(default=False)
	error_message = models.TextField(blank=True, null=True)
	timestamp = models.DateTimeField(default=now)
	
	def __str__(self):
		return f"{self.name} - {self.status_code} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class AuditLog(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	action = models.CharField(max_length=100)
	model_name = models.CharField(max_length=100)
	object_id = models.PositiveIntegerField()
	timestamp = models.DateTimeField(auto_now_add=True)
	object_repr = models.TextField(blank=True, null=True)
	changes = models.JSONField(null=True, blank=True)
	remote_ip = models.GenericIPAddressField(null=True, blank=True)
	user_agent = models.TextField(null=True, blank=True)
	view_name = models.CharField(max_length=255, blank=True, null=True)
	request_method = models.CharField(max_length=10, null=True, blank=True)
	referrer = models.URLField(null=True, blank=True)
	session_key = models.CharField(max_length=100, blank=True, null=True)
	is_manual_action = models.BooleanField(default=True)
	
	def __str__(self):
		return f"{self.model_name}: {self.user}"


class UMLTool(models.Model):
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name = "Generate UML Diagram"
		verbose_name_plural = "UML Diagram Generator"
	
	def __str__(self):
		return "UML Diagram Trigger"
