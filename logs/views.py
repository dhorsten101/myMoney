from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .models import SlowQueryLog


@staff_member_required
def slow_queries_view(request):
	page_obj = SlowQueryLog.objects.all()[:50]
	return render(request, 'slow_queries.html', {'page_obj': page_obj})
