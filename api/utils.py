import time
import traceback

import requests
from django.utils.timezone import now

from main.models import ErrorLog, ExternalServiceLog


# def log_error_to_db(exc, source="management", extra_info=None):
# 	tb_str = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
#
# 	ErrorLog.objects.create(
# 		timestamp=now(),
# 		level="ERROR",
# 		message=str(exc),
# 		exception_type=type(exc).__name__,
# 		exception_value=str(exc),
# 		traceback=tb_str,
# 		module=source,
# 		method=extra_info.get("method") if extra_info else None,
# 		path=extra_info.get("path") if extra_info else None,
# 		user=extra_info.get("user") if extra_info else None,
# 		ip_address=extra_info.get("ip") if extra_info else None,
# 	)


def log_error_to_db(
		exception,
		source="unknown",
		severity="ERROR",
		extra_info=None
):
	tb_str = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
	extra_info = extra_info or {}
	
	ErrorLog.objects.create(
		timestamp=now(),
		level="ERROR",
		severity=severity,
		message=str(exception),
		exception_type=type(exception).__name__,
		exception_value=str(exception),
		traceback=tb_str,
		module=source,
		method=extra_info.get("method"),
		status_code=extra_info.get("status_code"),
		path=extra_info.get("path"),
		pathname=extra_info.get("pathname"),
		lineno=extra_info.get("lineno"),
		func_name=extra_info.get("func_name"),
		object_id=extra_info.get("object_id"),
		user=extra_info.get("user"),
		ip_address=extra_info.get("ip"),
		user_agent=extra_info.get("user_agent"),
		view_name=extra_info.get("view_name"),
		request_body=extra_info.get("request_body"),
		headers=extra_info.get("headers"),
	)


def external_service_logger(name, url, method="GET"):
	def decorator(func):
		def wrapper(*args, **kwargs):
			start = time.time()
			status_code = None
			success = False
			error_message = ""
			response_time = None
			result = None
			
			try:
				result = func(*args, **kwargs)
				success = True
				status_code = 200  # Optional, override if available in func
				return result
			except requests.HTTPError as e:
				error_message = str(e)
				status_code = e.response.status_code if e.response else None
				log_error_to_db(e, source=name)
			except Exception as e:
				error_message = str(e)
				log_error_to_db(e, source=name)
			finally:
				response_time = (time.time() - start) * 1000
				ExternalServiceLog.objects.create(
					name=name,
					url=url,
					method=method,
					status_code=status_code,
					response_time_ms=response_time,
					execution_time_ms=response_time,
					response_success=success,
					error_message=error_message if not success else None,
				)
				return result or {}
		
		return wrapper
	
	return decorator
