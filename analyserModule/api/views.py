from django.shortcuts import render
import pickle
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from .models import monthWiseAnalytics
from .serializers import MonthWiseAnalyticsSerializer


@api_view(['GET'])
def bank_analysis(request):
    analysis = monthWiseAnalytics.objects.all()
    serializer = MonthWiseAnalyticsSerializer(analysis, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_statement(request):
    file = request.data['file']
    print(file)
    
    