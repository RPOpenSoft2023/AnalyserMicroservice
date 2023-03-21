from django.urls import path
from api import views

urlpatterns = [
    path('bank-analysis', views.bank_analysis)
]
