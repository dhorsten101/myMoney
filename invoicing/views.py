from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay
from django.shortcuts import render, get_object_or_404, redirect
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from invoicing.forms import InvoiceForm, RentalPropertyForm, RentalPropertyImageForm, RentalPropertyPipelineForm, MonthlyExpenseForm, RentalAgentForm, EstateAgentForm, ManagingAgentForm, RentalPropertyPipelineImageForm
from invoicing.models import Invoice, RentalProperty, RentalPropertyPipeline, MonthlyExpense, RentalAgent, EstateAgent, ManagingAgent, RentalPropertyPipelineImage


@login_required
def accounts_home(request):
	# Invoice revenue totals
	totals = Invoice.objects.aggregate(
		total_all=Sum("total"),
		total_paid=Sum("total", filter=models.Q(status=Invoice.STATUS_PAID)),
		total_unpaid=Sum("total", filter=~models.Q(status=Invoice.STATUS_PAID)),
	)
	totals = {k: v or Decimal("0.00") for k, v in totals.items()}

	# Expense totals (all-time, this month, last month)
	from datetime import date, timedelta
	# Optional selected end month for chart window
	selected_month_param = (request.GET.get("month") or "").strip()
	# Default end date is today; if month=YYYY-MM provided, use last day of that month
	if selected_month_param:
		try:
			year, mon = selected_month_param.split("-")
			year = int(year)
			mon = int(mon)
			end_month_start = date(year, mon, 1)
			# compute end-of-month by jumping to next month start - 1 day
			if mon == 12:
				next_month_start = date(year + 1, 1, 1)
			else:
				next_month_start = date(year, mon + 1, 1)
			selected_end_date = next_month_start - timedelta(days=1)
		except Exception:
			selected_end_date = date.today()
	else:
		selected_end_date = date.today()

	today = selected_end_date
	month_start = today.replace(day=1)
	last_month_end = month_start - timedelta(days=1)
	last_month_start = last_month_end.replace(day=1)

	expense_total_all = MonthlyExpense.objects.aggregate(Sum("amount")).get("amount__sum") or Decimal("0.00")
	expense_this_month = (
		MonthlyExpense.objects
		.filter(date__gte=month_start, date__lte=today)
		.aggregate(Sum("amount"))
		.get("amount__sum") or Decimal("0.00")
	)
	expense_last_month = (
		MonthlyExpense.objects
		.filter(date__gte=last_month_start, date__lte=last_month_end)
		.aggregate(Sum("amount"))
		.get("amount__sum") or Decimal("0.00")
	)

	expense_totals = {
		"total_all": expense_total_all,
		"this_month": expense_this_month,
		"last_month": expense_last_month,
	}

	# Build last 12 months labels and series for billed, paid, and expenses
	# Months list from 11 months ago up to selected month (inclusive)
	month_keys = []
	for i in range(11, -1, -1):
		m_index = (month_start.month - 1) - i
		year = month_start.year + (m_index // 12)
		month = (m_index % 12) + 1
		month_keys.append(date(year, month, 1))

	# Helper to normalize TruncMonth value to date
	def _norm_month(m):
		try:
			return m.date()
		except Exception:
			return m

	# Invoices billed per month (by issue_date)
	billed_qs = (
		Invoice.objects
		.filter(issue_date__gte=month_keys[0], issue_date__lte=today)
		.annotate(month=TruncMonth("issue_date"))
		.values("month")
		.annotate(total=Sum("total"))
	)
	billed_map = {_norm_month(r["month"]): float(r["total"]) for r in billed_qs}

	# Invoices PAID per month (by issue_date)
	paid_qs = (
		Invoice.objects
		.filter(status=Invoice.STATUS_PAID, issue_date__gte=month_keys[0], issue_date__lte=today)
		.annotate(month=TruncMonth("issue_date"))
		.values("month")
		.annotate(total=Sum("total"))
	)
	paid_map = {_norm_month(r["month"]): float(r["total"]) for r in paid_qs}

	# Expenses per month
	exp_qs = (
		MonthlyExpense.objects
		.filter(date__gte=month_keys[0], date__lte=today)
		.annotate(month=TruncMonth("date"))
		.values("month")
		.annotate(total=Sum("amount"))
	)
	exp_map = {_norm_month(r["month"]): float(r["total"]) for r in exp_qs}

	month_labels = [m.strftime("%Y-%m") for m in month_keys]
	billed_series = [billed_map.get(m, 0.0) for m in month_keys]
	paid_series = [paid_map.get(m, 0.0) for m in month_keys]
	expense_series = [exp_map.get(m, 0.0) for m in month_keys]

	return render(request, "invoicing/accounts.html", {
		"totals": totals,
		"expense_totals": expense_totals,
		"month_labels": month_labels,
		"billed_series": billed_series,
		"paid_series": paid_series,
		"expense_series": expense_series,
		"selected_month": month_start.strftime("%Y-%m"),
	})


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
def expense_list(request):
	expenses = MonthlyExpense.objects.order_by("-date", "-id")
	if request.method == "POST":
		form = MonthlyExpenseForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("expense_list")
	else:
		form = MonthlyExpenseForm()
	return render(request, "invoicing/expense_list.html", {"expenses": expenses, "form": form})


@login_required
def expense_update(request, id):
    expense = get_object_or_404(MonthlyExpense, id=id)
    if request.method == "POST":
        form = MonthlyExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = MonthlyExpenseForm(instance=expense)
    return render(request, "invoicing/expense_form.html", {"form": form, "expense": expense})


@login_required
def expense_delete(request, id):
    expense = get_object_or_404(MonthlyExpense, id=id)
    if request.method == "POST":
        expense.delete()
        return redirect("expense_list")
    return render(request, "invoicing/expense_confirm_delete.html", {"expense": expense})


@login_required
def expense_monthly_totals(request):
	from django.db.models.functions import TruncMonth
	qs = (
		MonthlyExpense.objects
		.annotate(month=TruncMonth("date"))
		.values("month")
		.annotate(total=Sum("amount"))
		.order_by("month")
	)
	return render(request, "invoicing/expense_monthly_totals.html", {"rows": qs})


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
	
	# Rental properties totals by month (sum across all properties)
	from django.db.models.functions import TruncMonth
	rental_monthly = (
		Invoice.objects
		.filter(status=Invoice.STATUS_PAID, rental_property__isnull=False)
		.annotate(month=TruncMonth("issue_date"))
		.values("month")
		.annotate(total=Sum("total"))
		.order_by("month")
	)
	rental_labels = [r["month"].strftime("%Y-%m") for r in rental_monthly]
	rental_totals = [float(r["total"]) for r in rental_monthly]
	
	# Aggregated projection across all rental properties (same rules as per-property earnings)
	from datetime import date
	capital_sum = RentalProperty.objects.aggregate(Sum("capital_value")).get("capital_value__sum") or Decimal("0")
	flow_sum = RentalProperty.objects.aggregate(Sum("flow_value")).get("flow_value__sum") or Decimal("0")
	
	# Growth rate from query param (defaults to 5%)
	try:
		rate_percent = Decimal(request.GET.get("rate", "5").strip())
	except Exception:
		rate_percent = Decimal("5")
	if rate_percent < 0:
		rate_percent = Decimal("0")
	growth_base = Decimal("1") + (rate_percent / Decimal("100"))
	
	agg_labels: list[str] = []
	agg_cumulative: list[float] = []
	agg_capital_line: list[float] = []
	agg_initial_capital_line: list[float] = []
	agg_coverage_line: list[float] = []
	payoff_flow_label_all = None
	payoff_growing_label_all = None
	months_to_payoff_flow_all = None
	months_to_payoff_growing_all = None
	
	if flow_sum > 0 and capital_sum > 0:
		start = date.today().replace(day=1)
		cumulative = Decimal("0")
		i = 0
		max_months = 600
		flow_annual_growth = float(growth_base)  # stepwise annual increase
		capital_annual_growth = float(growth_base)  # monthly compounding
		while i < max_months:
			# Cap overall projection window to 10 years
			if i >= 120:
				break
			years_elapsed = i // 12
			flow_factor = flow_annual_growth ** years_elapsed
			cap_factor = capital_annual_growth ** (i / 12.0)
			month_flow = (flow_sum * Decimal(str(flow_factor))).quantize(Decimal("0.01"))
			capital_current = (capital_sum * Decimal(str(cap_factor))).quantize(Decimal("0.01"))
			
			m_index = (start.month - 1 + i)
			year = start.year + (m_index // 12)
			month = (m_index % 12) + 1
			label = f"{year:04d}-{month:02d}"
			
			cumulative += month_flow
			agg_labels.append(label)
			agg_cumulative.append(float(cumulative))
			agg_capital_line.append(float(capital_current))
			agg_initial_capital_line.append(float(capital_sum))
			
			appreciation = capital_current - capital_sum
			coverage = cumulative + appreciation
			agg_coverage_line.append(float(coverage))
			
			if payoff_flow_label_all is None and cumulative >= capital_sum:
				payoff_flow_label_all = label
				months_to_payoff_flow_all = len(agg_labels)
			if payoff_growing_label_all is None and coverage >= capital_sum:
				payoff_growing_label_all = label
				months_to_payoff_growing_all = len(agg_labels)
			i += 1
	
	return render(request, "invoicing/homes_dashboard.html", {
		"totals": totals,
		"recent": recent,
		"rental_labels": rental_labels,
		"rental_totals": rental_totals,
		# Aggregated projection context
		"agg_labels": agg_labels,
		"agg_cumulative": agg_cumulative,
		"agg_capital_line": agg_capital_line,
		"agg_initial_capital_line": agg_initial_capital_line,
		"agg_coverage_line": agg_coverage_line,
		"payoff_flow_label_all": payoff_flow_label_all,
		"payoff_growing_label_all": payoff_growing_label_all,
		"months_to_payoff_flow_all": months_to_payoff_flow_all,
		"months_to_payoff_growing_all": months_to_payoff_growing_all,
		"growth_rate_percent": float(rate_percent),
	})


@login_required
def money_dashboard(request):
	# Reuse the same data as homes_dashboard
	totals = Invoice.objects.aggregate(
		total_all=Sum("total"),
		total_paid=Sum("total", filter=models.Q(status=Invoice.STATUS_PAID)),
		total_unpaid=Sum("total", filter=~models.Q(status=Invoice.STATUS_PAID)),
	)
	totals = {k: v or Decimal("0.00") for k, v in totals.items()}

	# Recent invoices
	recent = Invoice.objects.order_by("-issue_date", "-id")[:10]

	# Rental properties totals by month (sum across all properties)
	from django.db.models.functions import TruncMonth
	rental_monthly = (
		Invoice.objects
		.filter(status=Invoice.STATUS_PAID, rental_property__isnull=False)
		.annotate(month=TruncMonth("issue_date"))
		.values("month")
		.annotate(total=Sum("total"))
		.order_by("month")
	)
	rental_labels = [r["month"].strftime("%Y-%m") for r in rental_monthly]
	rental_totals = [float(r["total"]) for r in rental_monthly]

	# Aggregated projection across all rental properties (same rules as per-property earnings)
	from datetime import date
	capital_sum = RentalProperty.objects.aggregate(Sum("capital_value")).get("capital_value__sum") or Decimal("0")
	flow_sum = RentalProperty.objects.aggregate(Sum("flow_value")).get("flow_value__sum") or Decimal("0")

	# Growth rate from query param (defaults to 5%)
	try:
		rate_percent = Decimal(request.GET.get("rate", "5").strip())
	except Exception:
		rate_percent = Decimal("5")
	if rate_percent < 0:
		rate_percent = Decimal("0")
	growth_base = Decimal("1") + (rate_percent / Decimal("100"))

	agg_labels: list[str] = []
	agg_cumulative: list[float] = []
	agg_capital_line: list[float] = []
	agg_initial_capital_line: list[float] = []
	agg_coverage_line: list[float] = []
	payoff_flow_label_all = None
	payoff_growing_label_all = None
	months_to_payoff_flow_all = None
	months_to_payoff_growing_all = None

	if flow_sum > 0 and capital_sum > 0:
		start = date.today().replace(day=1)
		cumulative = Decimal("0")
		i = 0
		max_months = 600
		flow_annual_growth = float(growth_base)  # stepwise annual increase
		capital_annual_growth = float(growth_base)  # monthly compounding
		while i < max_months:
			# Cap overall projection window to 10 years
			if i >= 120:
				break
			years_elapsed = i // 12
			flow_factor = flow_annual_growth ** years_elapsed
			cap_factor = capital_annual_growth ** (i / 12.0)
			month_flow = (flow_sum * Decimal(str(flow_factor))).quantize(Decimal("0.01"))
			capital_current = (capital_sum * Decimal(str(cap_factor))).quantize(Decimal("0.01"))

			m_index = (start.month - 1 + i)
			year = start.year + (m_index // 12)
			month = (m_index % 12) + 1
			label = f"{year:04d}-{month:02d}"

			cumulative += month_flow
			agg_labels.append(label)
			agg_cumulative.append(float(cumulative))
			agg_capital_line.append(float(capital_current))
			agg_initial_capital_line.append(float(capital_sum))

			appreciation = capital_current - capital_sum
			coverage = cumulative + appreciation
			agg_coverage_line.append(float(coverage))

			if payoff_flow_label_all is None and cumulative >= capital_sum:
				payoff_flow_label_all = label
				months_to_payoff_flow_all = len(agg_labels)
			if payoff_growing_label_all is None and coverage >= capital_sum:
				payoff_growing_label_all = label
				months_to_payoff_growing_all = len(agg_labels)
			i += 1

	return render(request, "invoicing/money_dashboard.html", {
		"totals": totals,
		"recent": recent,
		"rental_labels": rental_labels,
		"rental_totals": rental_totals,
		"agg_labels": agg_labels,
		"agg_cumulative": agg_cumulative,
		"agg_capital_line": agg_capital_line,
		"agg_initial_capital_line": agg_initial_capital_line,
		"agg_coverage_line": agg_coverage_line,
		"payoff_flow_label_all": payoff_flow_label_all,
		"payoff_growing_label_all": payoff_growing_label_all,
		"months_to_payoff_flow_all": months_to_payoff_flow_all,
		"months_to_payoff_growing_all": months_to_payoff_growing_all,
		"growth_rate_percent": float(rate_percent),
	})


@login_required
def rental_pipeline_list(request):
	status_filter = request.GET.get("status", "interested").strip()
	if status_filter not in {"interested", "sold", "not_interested"}:
		status_filter = "interested"
	items = (
		RentalPropertyPipeline.objects
		.filter(status=status_filter)
		.prefetch_related("images")
		.order_by("-created_at")
	)
	if request.method == "POST":
		form = RentalPropertyPipelineForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("rental_pipeline_list")
	else:
		form = RentalPropertyPipelineForm()
	return render(request, "invoicing/rental_property_pipeline_list.html", {"items": items, "form": form, "status_filter": status_filter})


@login_required
def rental_pipeline_update_status(request, id, status):
	item = get_object_or_404(RentalPropertyPipeline, id=id)
	if status in dict(RentalPropertyPipeline.STATUS_CHOICES).keys():
		item.status = status
		item.save()
	return redirect("rental_pipeline_list")


@login_required
def rental_pipeline_edit(request, id):
    item = get_object_or_404(RentalPropertyPipeline, id=id)
    if request.method == "POST":
        form = RentalPropertyPipelineForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("rental_pipeline_list")
    else:
        form = RentalPropertyPipelineForm(instance=item)
    image_form = RentalPropertyPipelineImageForm()
    return render(request, "invoicing/rental_property_pipeline_form.html", {"form": form, "item": item, "image_form": image_form})


@login_required
def rental_pipeline_detail(request, id):
    item = get_object_or_404(RentalPropertyPipeline, id=id)
    image_form = RentalPropertyPipelineImageForm()
    return render(request, "invoicing/rental_property_pipeline_detail.html", {"item": item, "image_form": image_form})


# Rental Agent CRUD
@login_required
def agent_list(request):
	agents = RentalAgent.objects.order_by("name")
	estate_agents = EstateAgent.objects.order_by("name")
	managing_agents = ManagingAgent.objects.order_by("name")
	return render(request, "invoicing/agent_list.html", {"agents": agents, "estate_agents": estate_agents, "managing_agents": managing_agents})


@login_required
def agent_create(request):
	if request.method == "POST":
		form = RentalAgentForm(request.POST)
		if form.is_valid():
			agent = form.save()
			return redirect("agent_detail", id=agent.id)
	else:
		form = RentalAgentForm()
	return render(request, "invoicing/agent_form.html", {"form": form})


@login_required
def agent_update(request, id):
	agent = get_object_or_404(RentalAgent, id=id)
	if request.method == "POST":
		form = RentalAgentForm(request.POST, instance=agent)
		if form.is_valid():
			agent = form.save()
			return redirect("agent_detail", id=agent.id)
	else:
		form = RentalAgentForm(instance=agent)
	return render(request, "invoicing/agent_form.html", {"form": form, "agent": agent})


@login_required
def agent_detail(request, id):
	agent = get_object_or_404(RentalAgent, id=id)
	return render(request, "invoicing/agent_detail.html", {"agent": agent})


@login_required
def agent_delete(request, id):
	agent = get_object_or_404(RentalAgent, id=id)
	if request.method == "POST":
		agent.delete()
		return redirect("agent_list")
	return render(request, "invoicing/agent_confirm_delete.html", {"agent": agent})


# EstateAgent CRUD
@login_required
def estate_agent_list(request):
    agents = EstateAgent.objects.order_by("name")
    return render(request, "invoicing/estate_agent_list.html", {"agents": agents})


@login_required
def estate_agent_create(request):
    if request.method == "POST":
        form = EstateAgentForm(request.POST)
        if form.is_valid():
            agent = form.save()
            return redirect("estate_agent_detail", id=agent.id)
    else:
        form = EstateAgentForm()
    return render(request, "invoicing/estate_agent_form.html", {"form": form})


@login_required
def estate_agent_update(request, id):
    agent = get_object_or_404(EstateAgent, id=id)
    if request.method == "POST":
        form = EstateAgentForm(request.POST, instance=agent)
        if form.is_valid():
            agent = form.save()
            return redirect("estate_agent_detail", id=agent.id)
    else:
        form = EstateAgentForm(instance=agent)
    return render(request, "invoicing/estate_agent_form.html", {"form": form, "agent": agent})


@login_required
def estate_agent_detail(request, id):
    agent = get_object_or_404(EstateAgent, id=id)
    return render(request, "invoicing/estate_agent_detail.html", {"agent": agent})


@login_required
def estate_agent_delete(request, id):
    agent = get_object_or_404(EstateAgent, id=id)
    if request.method == "POST":
        agent.delete()
        return redirect("estate_agent_list")
    return render(request, "invoicing/estate_agent_confirm_delete.html", {"agent": agent})


# ManagingAgent CRUD
@login_required
def managing_agent_list(request):
    agents = ManagingAgent.objects.order_by("name")
    return render(request, "invoicing/managing_agent_list.html", {"agents": agents})


@login_required
def managing_agent_create(request):
    if request.method == "POST":
        form = ManagingAgentForm(request.POST)
        if form.is_valid():
            agent = form.save()
            return redirect("managing_agent_detail", id=agent.id)
    else:
        form = ManagingAgentForm()
    return render(request, "invoicing/managing_agent_form.html", {"form": form})


@login_required
def managing_agent_update(request, id):
    agent = get_object_or_404(ManagingAgent, id=id)
    if request.method == "POST":
        form = ManagingAgentForm(request.POST, instance=agent)
        if form.is_valid():
            agent = form.save()
            return redirect("managing_agent_detail", id=agent.id)
    else:
        form = ManagingAgentForm(instance=agent)
    return render(request, "invoicing/managing_agent_form.html", {"form": form, "agent": agent})


@login_required
def managing_agent_detail(request, id):
    agent = get_object_or_404(ManagingAgent, id=id)
    return render(request, "invoicing/managing_agent_detail.html", {"agent": agent})


@login_required
def managing_agent_delete(request, id):
    agent = get_object_or_404(ManagingAgent, id=id)
    if request.method == "POST":
        agent.delete()
        return redirect("managing_agent_list")
    return render(request, "invoicing/managing_agent_confirm_delete.html", {"agent": agent})


@login_required
def preview_images_from_url(request):
    src_url = request.GET.get("url", "").strip()
    images = []
    error = None
    if src_url:
        try:
            resp = requests.get(src_url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for img in soup.find_all("img"):
                src = img.get("src") or img.get("data-src")
                if not src:
                    continue
                full = urljoin(src_url, src)
                images.append(full)
        except Exception as e:
            error = str(e)
    return render(request, "invoicing/url_image_preview.html", {"images": images, "src_url": src_url, "error": error})


# RentalProperty CRUD
@login_required
def rental_property_list(request):
	props = RentalProperty.objects.order_by("name")
	totals = props.aggregate(
		total_capital=Sum("capital_value"),
		total_flow=Sum("flow_value"),
		total_expenses=Sum("total_expenses"),
	)
	return render(request, "invoicing/rental_property_list.html", {
		"properties": props,
		"totals": totals,
	})


@login_required
def rental_property_detail(request, id):
    prop = get_object_or_404(RentalProperty, id=id)
    image_form = RentalPropertyImageForm()
    return render(request, "invoicing/rental_property_detail.html", {"property": prop, "image_form": image_form})


@login_required
def rental_property_upload_image(request, id):
	prop = get_object_or_404(RentalProperty, id=id)
	if request.method == "POST":
		form = RentalPropertyImageForm(request.POST, request.FILES)
		if form.is_valid():
			img = form.save(commit=False)
			img.property = prop
			img.save()
	return redirect("rental_property_detail", id=prop.id)


@login_required
def rental_pipeline_upload_image(request, id):
    item = get_object_or_404(RentalPropertyPipeline, id=id)
    if request.method == "POST":
        form = RentalPropertyPipelineImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.pipeline = item
            img.save()
    return redirect("rental_pipeline_edit", id=item.id)


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


@login_required
def rental_property_earnings(request, id):
	prop = get_object_or_404(RentalProperty, id=id)
	# Paid invoices linked to this property, grouped by month
	qs = (
		Invoice.objects
		.filter(status=Invoice.STATUS_PAID, rental_property=prop)
		.annotate(month=TruncMonth("issue_date"))
		.values("month")
		.annotate(total=Sum("total"))
		.order_by("month")
	)
	labels = [r["month"].strftime("%Y-%m") for r in qs]
	values = [float(r["total"]) for r in qs]
	
	grand_total = sum(values) if values else 0
	
	# Projection to payoff: use capital_value and monthly flow_value
	from datetime import date
	
	capital = prop.capital_value or Decimal("0")
	monthly_flow = prop.flow_value or Decimal("0")
	# Use income (flow - expenses) for flow-only charts
	monthly_income = prop.income or Decimal("0")
	monthly_expenses_dec = prop.total_expenses or Decimal("0")
	# Growth rate (percent) can be overridden via ?rate= on the query string; defaults to 5%
	try:
		rate_percent = Decimal(request.GET.get("rate", "5").strip())
	except Exception:
		rate_percent = Decimal("5")
	if rate_percent < 0:
		rate_percent = Decimal("0")
	growth_base = Decimal("1") + (rate_percent / Decimal("100"))

	# Appreciation rate (percent) for asset growth (?app=), defaults to 5%
	try:
		appreciation_rate_percent = Decimal(request.GET.get("app", "5").strip())
	except Exception:
		appreciation_rate_percent = Decimal("5")
	if appreciation_rate_percent < 0:
		appreciation_rate_percent = Decimal("0")

	# Projection horizon in years (?horizon=), supports decimals (e.g., 2.5)
	# Default 10, clamped to [0.5, 50], converted to months (int)
	try:
		horizon_years_raw = (request.GET.get("horizon", "10") or "10").strip()
		horizon_years_dec = Decimal(horizon_years_raw)
	except Exception:
		horizon_years_dec = Decimal("10")
	if horizon_years_dec < Decimal("0.5"):
		horizon_years_dec = Decimal("0.5")
	if horizon_years_dec > Decimal("50"):
		horizon_years_dec = Decimal("50")
	months_cap = min(int((horizon_years_dec * Decimal("12")).to_integral_value(rounding='ROUND_HALF_UP')), 600)
	horizon_years = float(horizon_years_dec)
	months_to_payoff = None  # displayed months-to-payoff (will use growing payoff)
	proj_labels = []
	proj_values = []  # cumulative
	proj_capital_line = []
	proj_remaining_initial_capital_line = []
	proj_remaining_adjusted_line = []  # remaining considering appreciation (will be removed)
	proj_monthly_flow_exp_line = []  # monthly flow with smooth exponential growth
	proj_monthly_flow_step_line = []  # monthly flow with 5% stepwise yearly increase
	proj_remaining_growing_capital_line = []  # remaining vs initial considering appreciation
	projected_payoff_date = None
	payoff_growing_label = None
	payoff_flow_label = None
	months_to_payoff_flow = None
	months_to_payoff_growing = None
	
	# Always compute monthly income series by growing FLOW and subtracting constant EXPENSES
	if True:
		start = date.today().replace(day=1)
		i = 0
		max_months = months_cap  # horizon-based safety cap
		flow_annual_growth = float(growth_base)  # stepwise annual increase
		while i < max_months:
			if i >= max_months:
				break
			years_elapsed = i // 12
			flow_factor = flow_annual_growth ** years_elapsed
			grown_flow = (monthly_flow * Decimal(str(flow_factor))).quantize(Decimal("0.01"))
			month_flow = (grown_flow - monthly_expenses_dec).quantize(Decimal("0.01"))
			# compute label
			m_index = (start.month - 1 + i)
			year = start.year + (m_index // 12)
			month = (m_index % 12) + 1
			label = f"{year:04d}-{month:02d}"
			proj_labels.append(label)
			proj_monthly_flow_step_line.append(float(month_flow))
			i += 1

	# Also compute a RAW FLOW series (not income) using monthly_flow, regardless of income
	proj_monthly_flow_step_line_raw: list[float] = []
	if monthly_flow > 0:
		start = date.today().replace(day=1)
		i = 0
		max_months = months_cap
		flow_annual_growth = float(growth_base)  # stepwise annual increase
		while i < max_months:
			if i >= max_months:
				break
			years_elapsed = i // 12
			flow_factor = flow_annual_growth ** years_elapsed
			month_flow_val = (monthly_flow * Decimal(str(flow_factor))).quantize(Decimal("0.01"))
			# compute/ensure label
			m_index = (start.month - 1 + i)
			year = start.year + (m_index // 12)
			month = (m_index % 12) + 1
			label = f"{year:04d}-{month:02d}"
			if len(proj_labels) <= i:
				proj_labels.append(label)
			proj_monthly_flow_step_line_raw.append(float(month_flow_val))
			i += 1

	# Compute full projection only if we also have capital
	if monthly_flow > 0 and capital > 0:
		start = date.today().replace(day=1)
		cumulative = Decimal("0")
		i = 0
		max_months = months_cap
		flow_annual_growth = float(growth_base)
		capital_annual_growth = float(growth_base)
		while i < max_months:
			if i >= max_months:
				break
			years_elapsed = i // 12
			flow_factor = flow_annual_growth ** years_elapsed
			cap_factor = capital_annual_growth ** (i / 12.0)
			month_flow = (monthly_flow * Decimal(str(flow_factor))).quantize(Decimal("0.01"))
			flow_factor_exp = Decimal(str((float(growth_base)) ** (i / 12.0)))
			month_flow_exp = (monthly_flow * flow_factor_exp).quantize(Decimal("0.01"))
			capital_current = (capital * Decimal(str(cap_factor))).quantize(Decimal("0.01"))
			m_index = (start.month - 1 + i)
			year = start.year + (m_index // 12)
			month = (m_index % 12) + 1
			label = f"{year:04d}-{month:02d}"
			cumulative += month_flow
			if len(proj_labels) <= i:
				proj_labels.append(label)
			proj_values.append(float(cumulative))
			proj_capital_line.append(float(capital_current))
			proj_monthly_flow_exp_line.append(float(month_flow_exp))
			# Coverage vs initial capital including appreciation contribution (increasing series)
			appreciation = capital_current - capital
			coverage_growing = cumulative + appreciation
			if coverage_growing < 0:
				coverage_growing = Decimal("0")
			proj_remaining_growing_capital_line.append(float(coverage_growing))
			# Remaining against original capital (non-growing)
			remaining_initial = capital - cumulative
			if remaining_initial < 0:
				remaining_initial = Decimal("0")
			proj_remaining_initial_capital_line.append(float(remaining_initial))
			# Remaining to breakeven including appreciation: initial - (flow + appreciation)
			appreciation = capital_current - capital
			remaining_adjusted = capital - cumulative - appreciation
			if remaining_adjusted < 0:
				remaining_adjusted = Decimal("0")
			proj_remaining_adjusted_line.append(float(remaining_adjusted))
			# Capture payoff when cumulative flow meets/exceeds INITIAL capital (purchase value)
			if payoff_flow_label is None and cumulative >= capital:
				payoff_flow_label = label
				months_to_payoff_flow = len(proj_labels)
			if payoff_growing_label is None and (capital - cumulative - appreciation) <= 0:
				payoff_growing_label = label
				months_to_payoff_growing = len(proj_labels)
			i += 1
		
		# Use payoff based on growing capital (flow + appreciation breakeven)
		months_to_payoff = months_to_payoff_growing
		# If not paid off within cap, leave as None
		projected_payoff_date = payoff_growing_label if months_to_payoff else None
		payoff_years = (months_to_payoff // 12) if months_to_payoff else None
		payoff_months = (months_to_payoff % 12) if months_to_payoff else None
		# Flow-only breakdown
		projected_payoff_date_flow = payoff_flow_label if months_to_payoff_flow else None
		payoff_years_flow = (months_to_payoff_flow // 12) if months_to_payoff_flow else None
		payoff_months_flow = (months_to_payoff_flow % 12) if months_to_payoff_flow else None
	
	# Build initial capital flat line series matching projection length
	proj_initial_capital_line = [float(capital)] * len(proj_labels) if proj_labels else []
	
	return render(request, "invoicing/rental_property_earnings.html", {
		"property": prop,
		"labels": labels,
		"values": values,
		"grand_total": grand_total,
		"rows": qs,
		# Projection context
		"capital": float(capital),
		"monthly_flow": float(monthly_flow),
		"monthly_expenses": float(prop.total_expenses or Decimal("0")),
		"appreciation_rate_percent": float(appreciation_rate_percent),
		"appreciation_monthly": float(prop.appreciation_monthly or Decimal("0")),
		"total_income_monthly": float(prop.total_income or Decimal("0")),
		"months_to_payoff": months_to_payoff,
		"projected_payoff_date": projected_payoff_date,
		"growth_rate_percent": float(rate_percent),
		"payoff_years": payoff_years if 'payoff_years' in locals() else None,
		"payoff_months": payoff_months if 'payoff_months' in locals() else None,
		# Flow-only details
		"months_to_payoff_flow": months_to_payoff_flow,
		"projected_payoff_date_flow": projected_payoff_date_flow if 'projected_payoff_date_flow' in locals() else None,
		"payoff_years_flow": payoff_years_flow if 'payoff_years_flow' in locals() else None,
		"payoff_months_flow": payoff_months_flow if 'payoff_months_flow' in locals() else None,
		"proj_labels": proj_labels,
		"proj_values": proj_values,
		"proj_capital_line": proj_capital_line,
		"proj_initial_capital_line": proj_initial_capital_line,
		"proj_remaining_initial_capital_line": proj_remaining_initial_capital_line,
		"proj_monthly_flow_exp_line": proj_monthly_flow_exp_line,
		"proj_monthly_flow_step_line_raw": proj_monthly_flow_step_line_raw,
		"proj_monthly_flow_step_line": proj_monthly_flow_step_line,
		"proj_remaining_growing_capital_line": proj_remaining_growing_capital_line,
		"payoff_growing_label": payoff_growing_label,
		"payoff_flow_label": payoff_flow_label,
		"horizon_years": horizon_years,
	})
