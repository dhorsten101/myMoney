from django.db import models


class HistoryRecord(models.Model):
    CATEGORY_CHOICES = [
        ("crypto", "Crypto"),
        ("assets", "Assets"),
        ("expenses", "Expenses"),
    ]

    total_value = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_category_display()} Total: {self.total_value} at {self.timestamp}"
