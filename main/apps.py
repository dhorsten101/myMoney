from django.apps import AppConfig

default_app_config = 'main.apps.UmlConfig'


class MainConfig(AppConfig):
	default_auto_field = "django.db.models.BigAutoField"
	name = "main"
	
	def ready(self):
		from .signals import connect_signals
		connect_signals()
