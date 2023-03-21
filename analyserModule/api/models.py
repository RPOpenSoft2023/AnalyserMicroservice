from django.db import models


# Create your models here.
class monthWiseAnalytics(models.Model): 
    accountNumber = models.BigIntegerField()
    phoneNumber = models.BigIntegerField()
    month = models.IntegerField()
    year = models.IntegerField()