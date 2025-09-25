from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay
from django.shortcuts import render, get_object_or_404, redirect

from invoicing.forms import InvoiceForm, RentalPropertyForm
from invoicing.models import Invoice, RentalProperty


@login_required
def invoice_list(request):
    invoices = Invoice.objects.order_by("-issue_date", "-id")

    # Chart data: current month PAID totals by day
    from datetime import date
    today = date.today()
    month_start = today.replace(day=1)
    paid_this_month = (
        Invoice.objects
        .filter(status=Invoice.STATUS_PAID, issue_date__gte=month_start, issue_date__lte=today)
        .annotate(day=TruncDay("issue_date"))
        .values("day")
        .annotate(total=Sum("total"))
        .order_by("day")
    )
    chart_labels = [d["day"].strftime("%d %b") for d in paid_this_month]
    chart_values = [float(d["total"]) for d in paid_this_month]

    return render(request, "invoicing/invoice_list.html", {
        "invoices": invoices,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
    })


@login_required
def invoice_detail(request, id):
	invoice = get_object_or_404(Invoice, id=id)
	return render(request, "invoicing/invoice_detail.html", {"invoice": invoice})


@login_required
def invoice_create(request):
	if request.method == "POST":
		form = InvoiceForm(request.POST)
		if form.is_valid():
			invoice = form.save()
			return redirect("invoice_detail", id=invoice.id)
	else:
		form = InvoiceForm()
	return render(request, "invoicing/invoice_form.html", {"form": form})


@login_required
def invoice_update(request, id):
	invoice = get_object_or_404(Invoice, id=id)
	if request.method == "POST":
		form = InvoiceForm(request.POST, instance=invoice)
		if form.is_valid():
			invoice = form.save()
			return redirect("invoice_detail", id=invoice.id)
	else:
		form = InvoiceForm(instance=invoice)
	return render(request, "invoicing/invoice_form.html", {"form": form, "invoice": invoice})


@login_required
def invoice_delete(request, id):
	invoice = get_object_or_404(Invoice, id=id)
	if request.method == "POST":
		invoice.delete()
		return redirect("invoice_list")
	return render(request, "invoicing/invoice_confirm_delete.html", {"invoice": invoice})


@login_required
def invoice_monthly_totals(request):
    # Group PAID invoices by month they were issued
    paid = (
        Invoice.objects
        .filter(status=Invoice.STATUS_PAID)
        .order_by("-issue_date", "-id")
    )

    groups_by_month = {}
    for inv in paid:
        month_date = inv.issue_date.replace(day=1)
        if month_date not in groups_by_month:
            groups_by_month[month_date] = {
                "month": month_date,
                "label": month_date.strftime("%b %Y"),
                "invoices": [],
                "total": Decimal("0.00"),
            }
        groups_by_month[month_date]["invoices"].append(inv)
        groups_by_month[month_date]["total"] += inv.total

    # Sort months desc
    groups = [groups_by_month[k] for k in sorted(groups_by_month.keys(), reverse=True)]
    grand_total = sum((g["total"] for g in groups), Decimal("0.00"))

    return render(request, "invoicing/invoice_monthly_totals.html", {
        "groups": groups,
        "grand_total": grand_total,
    })


@login_required
def homes_dashboard(request):
    totals = Invoice.objects.aggregate(
        total_all=Sum("total"),
        total_paid=Sum("total", filter=models.Q(status=Invoice.STATUS_PAID)),
        total_unpaid=Sum("total", filter=~models.Q(status=Invoice.STATUS_PAID)),
    )
    totals = {k: v or Decimal("0.00") for k, v in totals.items()}

    # Recent invoices
    recent = Invoice.objects.order_by("-issue_date", "-id")[:10]

    return render(request, "invoicing/homes_dashboard.html", {
        "totals": totals,
        "recent": recent,
    })


# RentalProperty CRUD
@login_required
def rental_property_list(request):
    props = RentalProperty.objects.order_by("name")
    return render(request, "invoicing/rental_property_list.html", {"properties": props})


@login_required
def rental_property_detail(request, id):
    prop = get_object_or_404(RentalProperty, id=id)
    return render(request, "invoicing/rental_property_detail.html", {"property": prop})


@login_required
def rental_property_create(request):
    if request.method == "POST":
        form = RentalPropertyForm(request.POST)
        if form.is_valid():
            prop = form.save()
            return redirect("rental_property_detail", id=prop.id)
    else:
        form = RentalPropertyForm()
    return render(request, "invoicing/rental_property_form.html", {"form": form})


@login_required
def rental_property_update(request, id):
    prop = get_object_or_404(RentalProperty, id=id)
    if request.method == "POST":
        form = RentalPropertyForm(request.POST, instance=prop)
        if form.is_valid():
            prop = form.save()
            return redirect("rental_property_detail", id=prop.id)
    else:
        form = RentalPropertyForm(instance=prop)
    return render(request, "invoicing/rental_property_form.html", {"form": form, "property": prop})


@login_required
def rental_property_delete(request, id):
    prop = get_object_or_404(RentalProperty, id=id)
    if request.method == "POST":
        prop.delete()
        return redirect("rental_property_list")
    return render(request, "invoicing/rental_property_confirm_delete.html", {"property": prop})
