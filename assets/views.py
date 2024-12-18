# views.py
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AssetForm
from .models import Asset


@login_required
def asset_list(request):
    assets = Asset.objects.all()

    # Calculate totals for balance, converted_zar, and converted_usd
    total_balance = assets.aggregate(Sum("balance"))["balance__sum"] or 0
    total_converted_zar = (
        assets.aggregate(Sum("converted_zar"))["converted_zar__sum"] or 0
    )
    total_converted_usd = (
        assets.aggregate(Sum("converted_usd"))["converted_usd__sum"] or 0
    )

    context = {
        "assets": assets,
        "total_balance": total_balance,
        "total_converted_zar": total_converted_zar,
        "total_converted_usd": total_converted_usd,
    }

    return render(request, "asset_list.html", context)


@login_required
def asset_create(request):
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("asset_list")
    else:
        form = AssetForm()
    return render(request, "asset_form.html", {"form": form})


@login_required
def asset_update(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == "POST":
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect("asset_list")
    else:
        form = AssetForm(instance=asset)
    return render(request, "asset_form.html", {"form": form})


@login_required
def asset_delete(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == "POST":
        asset.delete()
        return redirect("asset_list")
    return render(request, "asset_confirm_delete.html", {"asset": asset})
