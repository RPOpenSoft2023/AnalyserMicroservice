from django.urls import path
from api import views

urlpatterns = [
    path('analyse/api/bank_analysis', views.bank_analysis),
    path('analyse/api/BankStatementAnalysis', views.bank_statement_analysis),
    path('analyse/api/dashboard/GrossSummary', views.gross_summary),
    path('analyse/api/dashboard/<str:bankName>', views.bank_name),
]
