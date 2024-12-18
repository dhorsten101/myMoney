from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

from incomes.forms import IncomeForm
from incomes.models import Income


@login_required
def income_list(request):
    incomes = Income.objects.all()
    total_balance = (
        incomes.aggregate(Sum("balance"))["balance__sum"] or 0
    )  # Sum up all the balances
    return render(
        request,
        "income_list.html",
        {"incomes": incomes, "total_balance": total_balance},
    )


@login_required
def income_create(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("income_list")
    else:
        form = IncomeForm()
    return render(request, "income_form.html", {"form": form})


@login_required
def income_update(request, id):
    income = get_object_or_404(Income, id=id)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect("income_list")
    else:
        form = IncomeForm(instance=income)
    return render(request, "income_form.html", {"form": form})


@login_required
def income_delete(request, id):
    income = get_object_or_404(Income, id=id)
    if request.method == "POST":
        income.delete()
        return redirect("income_list")
    return render(request, "income_confirm_delete.html", {"income": income})
