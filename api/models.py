from django.db import models


class LunoPrice(models.Model):
    pair = models.CharField(max_length=10)
    ask_price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_trade = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pair} - {self.last_trade}"


class CryptoBalance(models.Model):
    exchange = models.CharField(max_length=50)
    account_id = models.CharField(max_length=255, null=True, blank=True)
    asset = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=20, decimal_places=8)
    converted_zar = models.DecimalField(max_digits=20, decimal_places=2)
    converted_usd = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exchange} - {self.asset} - {self.balance}"
