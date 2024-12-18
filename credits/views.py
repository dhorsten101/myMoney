from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

from credits.forms import CreditForm
from credits.models import Credit


@login_required
def credit_list(request):
    credits = Credit.objects.all()
    total_balance = (
        credits.aggregate(Sum("balance"))["balance__sum"] or 0
    )  # Sum up all the balances
    return render(
        request,
        "credit_list.html",
        {"credits": credits, "total_balance": total_balance},
    )


@login_required
def credit_create(request):
    if request.method == "POST":
        form = CreditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("credit_list")
    else:
        form = CreditForm()
    return render(request, "credit_form.html", {"form": form})


@login_required
def credit_update(request, id):
    credit = get_object_or_404(Credit, id=id)
    if request.method == "POST":
        form = CreditForm(request.POST, instance=credit)
        if form.is_valid():
            form.save()
            return redirect("credit_list")
    else:
        form = CreditForm(instance=credit)
    return render(request, "credit_form.html", {"form": form})


@login_required
def credit_delete(request, id):
    credit = get_object_or_404(Credit, id=id)
    if request.method == "POST":
        credit.delete()
        return redirect("credit_list")
    return render(request, "credit_confirm_delete.html", {"credit": credit})
