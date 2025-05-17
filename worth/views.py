from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

from worth.forms import WorthForm
from worth.models import Worth


@login_required
def worth_list(request):
	worth = Worth.objects.all()
	total_real_value = (
			worth.aggregate(Sum("real_value"))["real_value__sum"] or 0
	)  # Sum up all the balances
	
	return render(
		request,
		"worth_list.html",
		{"worth": worth, "total_real_value": total_real_value},
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
