# utils/logging_utils.py
import traceback

from django.utils.timezone import now

from main.models import ErrorLog


def log_error_to_db(exc, source="management", extra_info=None):
	tb_str = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
	
	ErrorLog.objects.create(
		timestamp=now(),
		level="ERROR",
		message=str(exc),
		exception_type=type(exc).__name__,
		exception_value=str(exc),
		traceback=tb_str,
		module=source,
		method=extra_info.get("method") if extra_info else None,
		path=extra_info.get("path") if extra_info else None,
		user=extra_info.get("user") if extra_info else None,
		ip_address=extra_info.get("ip") if extra_info else None,
	)
