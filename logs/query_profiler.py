import json
import time

from django.conf import settings
from django.db import connection
from django.utils.deprecation import MiddlewareMixin

from logs.models import SlowQueryLog  # see model below


class QueryProfilerMiddleware(MiddlewareMixin):
	def process_view(self, request, view_func, view_args, view_kwargs):
		request._start_time = time.time()
		return None
	
	def process_response(self, request, response):
		total_time = time.time() - getattr(request, '_start_time', time.time())
		threshold = getattr(settings, 'SLOW_QUERY_THRESHOLD', 1.0)  # seconds
		
		if total_time >= threshold:
			total_sql_time = sum(float(q.get('time', 0)) for q in connection.queries)
			SlowQueryLog.objects.create(
				path=request.path,
				duration=round(total_time, 3),
				sql_time=round(total_sql_time, 3),
				queries=json.dumps(connection.queries[:10])[:10000],  # cap size
			)
		return response
