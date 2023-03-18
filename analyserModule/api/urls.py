from django.urls import path
from api import views

urlpatterns = [
    path('',views.bank_analysis),
    path('',views.bank_statement_analysis),
    path('',views.gross_summary),
    path('',views.bank_name),
]