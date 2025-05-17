from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render

from worth.forms import WorthForm
from .models import Worth


@login_required
def worth_list(request):
	worth_qs = Worth.objects.all().order_by("category")
	
	# Grand totals
	totals = worth_qs.aggregate(
		total_real_value=Sum("real_value"),
		total_quick_value=Sum("quick_value")
	)
	
	# Grouped by category
	grouped_worth = defaultdict(list)
	category_totals = {}
	
	for item in worth_qs:
		grouped_worth[item.category].append(item)
	
	# Calculate per-category totals
	for category, items in grouped_worth.items():
		total_real = sum(i.real_value or 0 for i in items)
		total_quick = sum(i.quick_value or 0 for i in items)
		category_totals[category] = {
			"items": items,
			"total_real": total_real,
			"total_quick": total_quick
		}
	
	return render(
		request,
		"worth_list.html",
		{
			"category_totals": category_totals,
			"total_real_value": totals["total_real_value"] or 0,
			"total_quick_value": totals["total_quick_value"] or 0,
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
