from django.db import models


# Create your models here.
class monthWiseAnalytics(models.Model): 
    accountNumber = models.BigIntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    analysis = models.TextField()