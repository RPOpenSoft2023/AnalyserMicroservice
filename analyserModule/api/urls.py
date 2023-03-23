from django.urls import path
from api import views

urlpatterns = [
    path('bank-analysis', views.bank_analysis),
    path('add-statement', views.bank_account_init),
    path('statement-analyse', views.bank_statement_analyse)
]
