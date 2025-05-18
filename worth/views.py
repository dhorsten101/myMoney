from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render

from worth.forms import WorthForm
from .models import Worth


def worth_list(request):
	worth_qs = Worth.objects.all().order_by("category")
	
	total_values = worth_qs.aggregate(
		total_real_value=Sum("real_value"),
		total_quick_value=Sum("quick_value")
	)
	
	grouped = defaultdict(list)
	category_totals = {}
	
	for item in worth_qs:
		grouped[item.category].append(item)
	
	for category_key, items in grouped.items():
		display_name = dict(Worth.CATEGORY_CHOICES).get(
			category_key,
			category_key.replace('_', ' ').title()
		)
		category_totals[display_name] = {
			"items": items,
			"total_real": sum(i.real_value or 0 for i in items),
			"total_quick": sum(i.quick_value or 0 for i in items),
		}
	
	return render(
		request,
		"worth_list.html",
		{
			"category_totals": category_totals,
			"total_real_value": total_values["total_real_value"] or 0,
			"total_quick_value": total_values["total_quick_value"] or 0,
		},
	)


@login_required
def worth_create(request):
	if request.method == "POST":
		form = WorthForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("worth_list")
	else:
		form = WorthForm()
	return render(request, "worth_form.html", {"form": form})


@login_required
def worth_update(request, id):
	worth = get_object_or_404(Worth, id=id)
	if request.method == "POST":
		form = WorthForm(request.POST, instance=worth)
		if form.is_valid():
			form.save()
			return redirect("worth_list")
	else:
		form = WorthForm(instance=worth)
	return render(request, "worth_form.html", {"form": form})


@login_required
def worth_delete(request, id):
	worth = get_object_or_404(Worth, id=id)
	if request.method == "POST":
		worth.delete()
		return redirect("worth_list")
	return render(request, "worth_confirm_delete.html", {"worth": worth})
