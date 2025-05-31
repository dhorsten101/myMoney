from django.apps import AppConfig


class MainConfig(AppConfig):
	default_auto_field = "django.db.models.BigAutoField"
	name = "main"
	
	def ready(self):
		from .signals import connect_signals
		connect_signals()
