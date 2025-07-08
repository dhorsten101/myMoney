from django.shortcuts import render

from .models import IntegrityScanLog


def system(request):
	return render(request, 'system.html', {})


# @staff_member_required
def integrity_scan_log_view(request):
	logs = IntegrityScanLog.objects.all()
	return render(request, 'scan_logs.html', {'logs': logs})
