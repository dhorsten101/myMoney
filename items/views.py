from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from items.forms import ItemForm, SkuCatalogForm
from items.models import Item, SkuCatalog


def _item_queryset_for_user(user):
	return Item.objects.all() if user.is_superuser else Item.objects.filter(user=user)


@login_required
def item_list(request):
	items = _item_queryset_for_user(request.user).order_by("-updated_at", "-id")
	return render(request, "items/item_list.html", {"items": items})


@login_required
def item_detail(request, id):
	item = (
		get_object_or_404(Item, id=id)
		if request.user.is_superuser
		else get_object_or_404(Item, id=id, user=request.user)
	)
	return render(request, "items/item_detail.html", {"item": item})


@login_required
def item_create(request):
	if request.method == "POST":
		form = ItemForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.user = request.user
			if item.sku_catalog_id:
				item.sku = item.sku_catalog.sku
				item.model = item.sku_catalog.model
				item.sku_description = item.sku_catalog.description
				if not item.name:
					item.name = item.sku_description
			item.save()
			return redirect("item_detail", id=item.id)
	else:
		form = ItemForm()
	return render(request, "items/item_form.html", {"form": form})


@login_required
def item_update(request, id):
	item = (
		get_object_or_404(Item, id=id)
		if request.user.is_superuser
		else get_object_or_404(Item, id=id, user=request.user)
	)
	if request.method == "POST":
		form = ItemForm(request.POST, instance=item)
		if form.is_valid():
			updated = form.save(commit=False)
			# keep ownership stable for non-superusers
			if not request.user.is_superuser:
				updated.user = request.user
			if updated.sku_catalog_id:
				updated.sku = updated.sku_catalog.sku
				updated.model = updated.sku_catalog.model
				updated.sku_description = updated.sku_catalog.description
				if not updated.name:
					updated.name = updated.sku_description
			updated.save()
			return redirect("item_detail", id=updated.id)
	else:
		form = ItemForm(instance=item)
	return render(request, "items/item_form.html", {"form": form, "item": item})


@login_required
def item_delete(request, id):
	item = (
		get_object_or_404(Item, id=id)
		if request.user.is_superuser
		else get_object_or_404(Item, id=id, user=request.user)
	)
	if request.method == "POST":
		item.delete()
		return redirect("item_list")
	return render(request, "items/item_confirm_delete.html", {"item": item})


@login_required
def sku_catalog_list(request):
	items = SkuCatalog.objects.order_by("sku")
	return render(request, "items/sku_catalog_list.html", {"items": items})


@login_required
def sku_catalog_detail(request, id):
	item = get_object_or_404(SkuCatalog, id=id)
	return render(request, "items/sku_catalog_detail.html", {"item": item})


@login_required
def sku_catalog_create(request):
	if request.method == "POST":
		form = SkuCatalogForm(request.POST)
		if form.is_valid():
			item = form.save()
			return redirect("sku_catalog_detail", id=item.id)
	else:
		form = SkuCatalogForm()
	return render(request, "items/sku_catalog_form.html", {"form": form})


@login_required
def sku_catalog_update(request, id):
	item = get_object_or_404(SkuCatalog, id=id)
	if request.method == "POST":
		form = SkuCatalogForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save()
			return redirect("sku_catalog_detail", id=item.id)
	else:
		form = SkuCatalogForm(instance=item)
	return render(request, "items/sku_catalog_form.html", {"form": form, "item": item})


@login_required
def sku_catalog_delete(request, id):
	item = get_object_or_404(SkuCatalog, id=id)
	if request.method == "POST":
		item.delete()
		return redirect("sku_catalog_list")
	return render(request, "items/sku_catalog_confirm_delete.html", {"item": item})
