from django.db import models


# Create your models here.
class monthWiseAnalytics(models.Model):
    accountNumber = models.BigIntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    loanDetails = models.JSONField()
    transactionTypes = models.JSONField()
    averageDayWiseExpense = models.DecimalField(
        decimal_places=2, max_digits=10)
    averageDayWiseIncome = models.DecimalField(decimal_places=2, max_digits=10)
    creditDebitFrequency = models.JSONField()
    totalMonthIncome = models.BigIntegerField()
    totalMonthExpense = models.BigIntegerField()
    spendingExpenseRatio = models.DecimalField(decimal_places=2, max_digits=10)
    categorizedData = models.JSONField()
    storedCautionData = models.JSONField()
