import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from weight.forms import WeightForm
from weight.models import Weight


def _admin_required(view_func):
	@login_required
	def _wrapped(request, *args, **kwargs):
		if request.user.is_superuser or request.user.groups.filter(name="admin").exists():
			return view_func(request, *args, **kwargs)
		raise PermissionDenied
	return _wrapped


@_admin_required
def weight_list(request):
	weights = Weight.objects.order_by('-created_at')
	latest_weight = weights.first()  # Gets the most recent one by date
	labels = [w.created_at.strftime('%Y-%m-%d') for w in weights]
	values = [float(w.weight) for w in weights]  # convert Decimal to float
	
	context = {
		'weight': weights,
		'labels': json.dumps(labels),
		'values': json.dumps(values),
		'latest_weight': latest_weight,
	}
	return render(request, 'weight_list.html', context)


@_admin_required
def weight_create(request):
	if request.method == "POST":
		form = WeightForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("weight_list")
	else:
		form = WeightForm()
	return render(request, "weight_form.html", {"form": form})


@_admin_required
def weight_update(request, id):
	weight = get_object_or_404(Weight, id=id)
	if request.method == "POST":
		form = WeightForm(request.POST, instance=weight)
		if form.is_valid():
			form.save()
			return redirect("weight_list")
	else:
		form = WeightForm(instance=weight)
	return render(request, "weight_form.html", {"form": form})


@_admin_required
def weight_delete(request, id):
	weight = get_object_or_404(Weight, id=id)
	if request.method == "POST":
		weight.delete()
		return redirect("weight_list")
	return render(request, "weight_confirm_delete.html", {"weight": weight})
