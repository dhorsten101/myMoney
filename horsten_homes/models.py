from decimal import Decimal, ROUND_HALF_UP

from django.db import models, transaction


class Property(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=255, blank=True)
	description = models.TextField(blank=True)
	# Aggregated totals over related doors/expenses
	total_capital_doors = models.DecimalField(max_digits=14, decimal_places=2, default=0)
	total_rooms = models.IntegerField(default=0)
	total_bathrooms = models.IntegerField(default=0)
	total_expense = models.DecimalField(max_digits=14, decimal_places=2, default=0)
	total_squares = models.IntegerField(default=0)
	total_income = models.DecimalField(max_digits=14, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def recalc_totals(self):
		from django.db.models import Sum
		# Doors aggregate
		doors = self.rental_properties.all()
		tot_cap = doors.aggregate(Sum("capital_value")).get("capital_value__sum") or 0
		tot_rooms = doors.aggregate(Sum("total_beds")).get("total_beds__sum") or 0
		tot_baths = doors.aggregate(Sum("total_toilets")).get("total_toilets__sum") or 0
		tot_squares = doors.aggregate(Sum("squares")).get("squares__sum") or 0
		tot_income = doors.aggregate(Sum("flow_value")).get("flow_value__sum") or 0
		# Expenses across all doors under this property
		try:
			from horsten_homes.models import MonthlyExpense
			exp_total = (
				MonthlyExpense.objects.filter(door__property_group=self)
				.aggregate(Sum("amount"))
				.get("amount__sum") or 0
			)
		except Exception:
			exp_total = 0
		self.total_capital_doors = Decimal(str(tot_cap)) if not isinstance(tot_cap, Decimal) else tot_cap
		self.total_rooms = int(tot_rooms)
		self.total_bathrooms = int(tot_baths)
		self.total_squares = int(tot_squares)
		self.total_income = Decimal(str(tot_income)) if not isinstance(tot_income, Decimal) else tot_income
		self.total_expense = Decimal(str(exp_total)) if not isinstance(exp_total, Decimal) else exp_total
		super().save(update_fields=[
			"total_capital_doors",
			"total_rooms",
			"total_bathrooms",
			"total_squares",
			"total_income",
			"total_expense",
			"updated_at",
		])


class Door(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=255)
	website = models.URLField(blank=True)
	property_group = models.ForeignKey('Property', null=True, blank=True, on_delete=models.SET_NULL, related_name='rental_properties')
	squares = models.IntegerField(default=0)
	total_beds = models.IntegerField(default=0)
	total_toilets = models.IntegerField(default=0)
	capital_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	flow_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	levies = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	rates_taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	water_electricity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	internet = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	other_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	cost_of_money_monthly = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	appreciation_monthly = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	agent = models.ForeignKey('RentalAgent', null=True, blank=True, on_delete=models.SET_NULL, related_name='properties')
	estate_agent = models.ForeignKey('EstateAgent', null=True, blank=True, on_delete=models.SET_NULL, related_name='estate_properties')
	managing_agent = models.ForeignKey('ManagingAgent', null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_properties')
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		# Ensure expenses reflect the sum of the four component costs
		from decimal import Decimal
		# Compute cost of money per month at 6% per annum on capital value FIRST
		monthly_rate = (Decimal("0.06") / Decimal("12"))
		self.cost_of_money_monthly = ((self.capital_value or Decimal("0")) * monthly_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
		total_expenses = (
				(self.levies or Decimal("0"))
				+ (self.rates_taxes or Decimal("0"))
				+ (self.internet or Decimal("0"))
				+ (self.water_electricity or Decimal("0"))
				+ (self.other_expenses or Decimal("0"))
			# + (self.cost_of_money_monthly or Decimal("0"))
		)
		self.total_expenses = total_expenses
		# Compute income = flow - total_expenses
		self.income = (self.flow_value or Decimal("0")) - (self.total_expenses or Decimal("0"))
		# Compute monthly appreciation from capital value at 5% p.a. compounded monthly
		monthly_app_rate = (Decimal("1.05") ** (Decimal("1") / Decimal("12"))) - Decimal("1")
		self.appreciation_monthly = ((self.capital_value or Decimal("0")) * monthly_app_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
		# Total income = rental income + appreciation
		self.total_income = (self.income or Decimal("0")) + (self.appreciation_monthly or Decimal("0"))
		super().save(*args, **kwargs)
		# After door save, update the linked property's aggregates
		if self.property_group_id:
			try:
				self.property_group.recalc_totals()
			except Exception:
				pass


class Invoice(models.Model):
	STATUS_DRAFT = "DRAFT"
	STATUS_SENT = "SENT"
	STATUS_PAID = "PAID"
	STATUS_OVERDUE = "OVERDUE"
	STATUS_CANCELLED = "CANCELLED"
	
	STATUS_CHOICES = [
		(STATUS_DRAFT, "Draft"),
		(STATUS_SENT, "Sent"),
		(STATUS_PAID, "Paid"),
		(STATUS_OVERDUE, "Overdue"),
		(STATUS_CANCELLED, "Cancelled"),
	]
	
	number = models.PositiveIntegerField(unique=True, editable=False)
	customer_name = models.CharField(max_length=200)
	customer_email = models.EmailField(blank=True)
	issue_date = models.DateField()
	due_date = models.DateField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
	
	door = models.ForeignKey(
		Door,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="invoices",
	)
	
	subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	
	notes = models.TextField(blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		if self.door:
			return f"Invoice {self.number} - {self.door.name}"
		return f"Invoice {self.number}"
	
	def save(self, *args, **kwargs):
		# Auto-assign sequential invoice number starting at 1
		if not self.number:
			with transaction.atomic():
				last = (
					type(self)
					.objects.select_for_update()
					.order_by("-number")
					.first()
				)
				self.number = 1 if last is None else last.number + 1
		
		# Compute amounts assuming UI enters Gross Total (incl. VAT)
		gross_total = self.total or Decimal("0")
		if gross_total > 0:
			# Back-calc net and tax from gross
			net = (gross_total / Decimal("1.15")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
			tax = (net * Decimal("0.15")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
			self.subtotal = net
			self.tax = tax
			self.total = (net + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
		else:
			# Fallback: compute from subtotal if gross wasn't provided
			computed_tax = (self.subtotal or Decimal("0")) * Decimal("0.15")
			self.tax = computed_tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
			self.total = (self.subtotal or Decimal("0")) + (self.tax or Decimal("0"))
		
		super().save(*args, **kwargs)


class DoorImage(models.Model):
	door = models.ForeignKey(Door, related_name="images", on_delete=models.CASCADE)
	image = models.ImageField(upload_to="rental_property_images/")
	uploaded_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"Image for {self.door.name}"


class DoorPipeline(models.Model):
	STATUS_CHOICES = [
		("interested", "Interested"),
		("not_interested", "Not Interested"),
		("sold", "Sold"),
	]
	
	url = models.URLField()
	title = models.CharField(max_length=255, blank=True)
	notes = models.TextField(blank=True)
	price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="interested")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.title or self.url


class DoorPipelineImage(models.Model):
	pipeline = models.ForeignKey(DoorPipeline, related_name="images", on_delete=models.CASCADE)
	image = models.ImageField(upload_to="rental_property_images/")
	uploaded_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"Image for pipeline {self.pipeline.id}"



class MonthlyExpense(models.Model):
	door = models.ForeignKey(Door, null=True, blank=True, on_delete=models.SET_NULL, related_name="monthly_expenses")
	date = models.DateField()
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		door = f" for {self.door.name}" if self.door else ""
		return f"Expense {self.date} - {self.amount}{door}"


class RentalAgent(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=50, blank=True)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name


class EstateAgent(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=50, blank=True)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name


class ManagingAgent(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=50, blank=True)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name


class Tenant(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=50, blank=True)
	move_in_date = models.DateField()
	move_out_date = models.DateField(null=True, blank=True)
	notes = models.TextField(blank=True)
	door = models.ForeignKey(Door, on_delete=models.SET_NULL, null=True, blank=True, related_name="tenants")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
