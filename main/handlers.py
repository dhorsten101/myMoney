import logging

from django.apps import apps


class DBLogHandler(logging.Handler):
	def emit(self, record):
		try:
			ErrorLog = apps.get_model('main', 'ErrorLog')  # ✅ Delayed import
			ErrorLog.objects.create(
				level=record.levelname,
				message=self.format(record),
				module=record.module,
				exception=str(record.exc_info) if record.exc_info else ''
			)
		except Exception:
			import traceback
			print("Logging error to DB failed:")
			print(traceback.format_exc())
