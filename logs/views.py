from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .models import SlowQueryLog


@staff_member_required
def slow_queries_view(request):
	logs = SlowQueryLog.objects.all()[:100]
	return render(request, 'slow_queries.html', {'logs': logs})
