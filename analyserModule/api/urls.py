from django.urls import path
from api import views

urlpatterns = [
    path('bank-analysis', views.bank_analysis),
    path('add-statement', views.bank_account_init),
    path('statement-analyse', views.bank_statement_analyse),
    path('edit-transaction', views.edit_transaction),
    # TODO: add transaction
]
