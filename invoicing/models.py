from decimal import Decimal, ROUND_HALF_UP

from django.db import models, transaction


class RentalProperty(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=255)
	website = models.URLField(blank=True)
	capital_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	flow_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	levies = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	rates_taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	water_electricity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	internet = models.DecimalField(max_digits=12, decimal_places=2, default=0)
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
	
	rental_property = models.ForeignKey(
		RentalProperty,
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
		return f"Invoice {self.number} - {self.customer_name}"
	
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


class RentalPropertyImage(models.Model):
	property = models.ForeignKey(RentalProperty, related_name="images", on_delete=models.CASCADE)
	image = models.ImageField(upload_to="rental_property_images/")
	uploaded_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"Image for {self.property.name}"


class RentalPropertyPipeline(models.Model):
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


class RentalPropertyPipelineImage(models.Model):
	pipeline = models.ForeignKey(RentalPropertyPipeline, related_name="images", on_delete=models.CASCADE)
	image = models.ImageField(upload_to="rental_property_images/")
	uploaded_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"Image for pipeline {self.pipeline.id}"


class MonthlyExpense(models.Model):
	property = models.ForeignKey(RentalProperty, null=True, blank=True, on_delete=models.SET_NULL, related_name="monthly_expenses")
	date = models.DateField()
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		prop = f" for {self.property.name}" if self.property else ""
		return f"Expense {self.date} - {self.amount}{prop}"


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
