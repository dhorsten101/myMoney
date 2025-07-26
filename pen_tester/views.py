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
			'docker', 'run', '--rm', '--network=host', 'kali-scanner', subnet
		]
		result = subprocess.run(docker_cmd, capture_output=True, text=True)
		
		try:
			raw_output = result.stdout.strip()
			lines = raw_output.splitlines()
			json_start = next((i for i, line in enumerate(lines) if line.startswith('[')), None)
			
			if json_start is not None:
				cleaned_json = '\n'.join(lines[json_start:])
				ip_list = json.loads(cleaned_json)
				job.results = ip_list
				job.finished = True
				job.save()
				return redirect('discovery_result', job_id=job.id)
			else:
				raise ValueError("No valid JSON found in output.")
		
		except Exception as e:
			job.results = [f"Error parsing results: {str(e)}"]
			job.finished = True
			job.save()
			return render(request, 'endpoint_discovery.html', {
				'error': f"Parsing error: {str(e)}",
				'job': job
			})
	
	return render(request, 'endpoint_discovery.html')


def discovery_result(request, job_id):
	job = get_object_or_404(DiscoveryJob, id=job_id)
	return render(request, 'discovery_result.html', {'job': job})
