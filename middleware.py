# middleware.py in your app folder

import traceback

from main.models import ErrorLog


class ErrorLoggingMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
	
	def __call__(self, request):
		try:
			return self.get_response(request)
		except Exception as e:
			ErrorLog.objects.create(
				path=request.path,
				method=request.method,
				message=traceback.format_exc(),
				status_code=500
			)
			raise  # Re-raise to preserve Django’s default error behavior
