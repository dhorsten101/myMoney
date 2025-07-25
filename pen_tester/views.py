# pen_tester/views.py

import json
import subprocess

from django.shortcuts import render, redirect, get_object_or_404

from .forms import TargetForm
from .models import DiscoveryJob
from .models import Target


def pen_test_dashboard(request):
	form = TargetForm(request.POST or None)
	if form.is_valid():
		target = form.save()
		return redirect('report', target_id=target.id)
	
	targets = Target.objects.order_by('-submitted_at')
	return render(request, 'pen_test_dashboard.html', {
		'form': form,
		'targets': targets,
	})


def report(request, target_id):
	target = get_object_or_404(Target, id=target_id)
	return render(request, 'pen_test_report.html', {
		'target': target,
		'results': target.results.all(),
	})


def discovery_view(request):
	if request.method == 'POST':
		subnet = request.POST.get('subnet')
		job = DiscoveryJob.objects.create(subnet=subnet)
		
		docker_cmd = [
			'docker', 'run', '--rm', 'kali-scanner', subnet
		]
		result = subprocess.run(docker_cmd, capture_output=True, text=True)
		
		try:
			ip_list = json.loads(result.stdout)
			job.results = ip_list
			job.finished = True
			job.save()
			return redirect('discovery_result', job_id=job.id)
		except Exception as e:
			job.results = ['Error parsing results']
			job.save()
			return render(request, 'endpoint_discovery.html', {
				'error': str(e),
				'job': job
			})
	
	return render(request, 'endpoint_discovery.html')


def discovery_result(request, job_id):
	job = get_object_or_404(DiscoveryJob, id=job_id)
	return render(request, 'discovery_result.html', {'job': job})
