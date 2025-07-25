# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404

from .forms import TargetForm
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
