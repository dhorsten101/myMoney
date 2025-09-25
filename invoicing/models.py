from decimal import Decimal, ROUND_HALF_UP
from django.db import models, transaction


class RentalProperty(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    capital_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    flow_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cost_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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
        
        # Always compute tax at 15% of subtotal (rounded to 2 decimals)
        computed_tax = (self.subtotal or Decimal("0")) * Decimal("0.15")
        self.tax = computed_tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        # Ensure total is always subtotal + tax
        self.total = (self.subtotal or Decimal("0")) + (self.tax or Decimal("0"))
        
        super().save(*args, **kwargs)


