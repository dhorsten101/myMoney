from django.apps import AppConfig


class InvoicingConfig(AppConfig):
	default_auto_field = "django.db.models.BigAutoField"
	name = "horsten_homes"

	def ready(self):
		from . import signals  # noqa
