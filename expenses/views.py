from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

from expenses.forms import ExpenseForm
from expenses.models import Expense


@login_required
def expense_list(request):
	expenses = Expense.objects.all()
	total_balance = (
			expenses.aggregate(Sum("balance"))["balance__sum"] or 0
	)  # Sum up all the balances
	return render(
		request,
		"expense_list.html",
		{"expenses": expenses, "total_balance": total_balance},
	)


@login_required
def expense_create(request):
	if request.method == "POST":
		form = ExpenseForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("expense_list")
	else:
		form = ExpenseForm()
	return render(request, "expense_form.html", {"form": form})


@login_required
def expense_update(request, id):
	expense = get_object_or_404(Expense, id=id)
	if request.method == "POST":
		form = ExpenseForm(request.POST, instance=expense)
		if form.is_valid():
			form.save()
			return redirect("expense_list")
	else:
		form = ExpenseForm(instance=expense)
	return render(request, "expense_form.html", {"form": form})


@login_required
def expense_delete(request, id):
	expense = get_object_or_404(Expense, id=id)
	if request.method == "POST":
		expense.delete()
		return redirect("expense_list")
	return render(request, "expense_confirm_delete.html", {"expense": expense})
