from django.urls import path
from api import views

urlpatterns = [
    path('analyse/api/bank-analysis',views.bank_analysis),
    path('analyse/api/BankStatementAnalysis',views.bank_statement_analysis),
    path('',views.gross_summary),
    path('',views.bank_name),
]