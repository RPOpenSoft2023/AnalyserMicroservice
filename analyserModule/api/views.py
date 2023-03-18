from django.shortcuts import render
import pickle
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

@api_view(['GET'])
def bank_analysis(request):
    return_data = {

    }
    return Response(return_data)

def bank_statement_analysis(request):
    return_data = {

    }
    return Response(return_data)

def gross_summary(request):
    return_data = {
        
    }
    return Response(return_data)

def bank_name(request):
    return_data = {

    }
    return Response(return_data)

# Create your views here.
