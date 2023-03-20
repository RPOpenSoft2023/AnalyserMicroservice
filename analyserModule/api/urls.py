from django.urls import path
from api import views

urlpatterns = [
    path('bank_analysis', views.bank_analysis),
    path('upload-statement', views.upload_statement),
]
