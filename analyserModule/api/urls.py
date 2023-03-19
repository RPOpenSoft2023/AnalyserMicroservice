from django.urls import path
from api import views

urlpatterns = [
    path('bank-analysis', views.bank_analysis),
    path('bank-statement-analysis', views.bank_statement_analysis),
    path('dashboard/gross-summary', views.gross_summary),
    path('dashboard/<str:bankName>', views.bank_name),
]
