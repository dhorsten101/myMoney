from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from contractors.forms import ContractorForm
from contractors.models import Contractor


@login_required
def contractor_list(request):
	items = Contractor.objects.order_by("name")
	return render(request, "contractors/contractor_list.html", {"items": items})


@login_required
def contractor_create(request):
	if request.method == "POST":
		form = ContractorForm(request.POST)
		if form.is_valid():
			item = form.save()
			return redirect("contractor_detail", id=item.id)
	else:
		form = ContractorForm()
	return render(request, "contractors/contractor_form.html", {"form": form})


@login_required
def contractor_detail(request, id):
	item = get_object_or_404(Contractor, id=id)
	return render(request, "contractors/contractor_detail.html", {"item": item})


@login_required
def contractor_update(request, id):
	item = get_object_or_404(Contractor, id=id)
	if request.method == "POST":
		form = ContractorForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save()
			return redirect("contractor_detail", id=item.id)
	else:
		form = ContractorForm(instance=item)
	return render(request, "contractors/contractor_form.html", {"form": form, "item": item})


@login_required
def contractor_delete(request, id):
	item = get_object_or_404(Contractor, id=id)
	if request.method == "POST":
		item.delete()
		return redirect("contractor_list")
	return render(request, "contractors/contractor_confirm_delete.html", {"item": item})
