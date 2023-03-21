from django.db import models


# Create your models here.
class monthWiseAnalytics(models.Model): 
    accountNumber = models.BigIntegerField()
    phoneNumber = models.BigIntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    # analysis = models.TextField()
    # analysis for current month
    largeCreditSources = models.JSONField()
    largeDebitSources = models.JSONField()
    avgSpending = models.DecimalField(decimal_places=2, max_digits=10)
    avgBalance = models.DecimalField(decimal_places=2, max_digits=10)
    spendingIncomeRatio = models.DecimalField(decimal_places=2, max_digits=10)
    monthlyLoan = models.BigIntegerField()