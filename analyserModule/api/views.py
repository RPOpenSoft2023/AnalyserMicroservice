from django.shortcuts import render
import pickle
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .Helpers import Sources, Loans, Info, PaymentStat
from .Helpers.processTransactions import preprocessing, processing, processingMonthWiseTransactions, getMonth, getYear
from .models import monthWiseAnalytics
import pandas as pd
from django.conf import settings
import requests


@api_view(['GET'])
def bank_analysis(request):
    try:
        data = request.GET
        startMonth, startYear, endMonth, endYear = map(int, [data['start_month'], data['start_year'], data['end_month'], data['end_year']])
        accountNumber = int(data['account_number'])
        token = request.headers.get('Authorization')

        if(token):
            response = requests.get(settings.USER_MICROSERVICE,
                                        headers = { 'Authorization': token }
                                    )
            if(response.status_code != 200):
                return Response({"message": "not logged in"}, status=401)

        iterMonth, iterYear = startMonth, startYear

        analytics = []
        while((iterYear < endYear) or ((iterYear == endYear) and (iterMonth <= endMonth)) ):
            currData = monthWiseAnalytics.objects.filter(accountNumber=accountNumber, month=iterMonth, year=iterYear).values()
            if(len(currData) == 0):
                return Response({"message": "analysis failed due to insufficient data"}, status=400)
            curr = currData[0]
            analytics.append(curr)
            if(iterMonth == 11):
                iterYear += 1
                iterMonth = 0
            else:
                iterMonth += 1
        return Response({"analytics": analytics})

    except Exception as e:
        return Response({"Error": str(e)}, status=400)

@api_view(['POST'])
def bank_account_init(request):
    try:
        file = request.data['file']        
        token = request.headers.get('Authorization')
        accountNumber = request.data.get('account_number')

        if(token):
            response = requests.get(settings.USERS_MICROSERVICE_LINK,
                                        headers = { 'Authorization': token }
                                    )
            if(response.status_code != 200):
                return Response({"message": "not logged in"}, status=401)
        if(not accountNumber):
            return Response({"message": "account number required"}, status=400)

        transactions = pd.read_csv(file)
        transactions = preprocessing(transactions)
        transactions['month'] = transactions['Date'].apply(getMonth)
        transactions['year'] = transactions['Date'].apply(getYear)
        for val in processing(transactions, accountNumber):
            monthWiseTransactions = val[2]
            currAnalDict = processingMonthWiseTransactions(monthWiseTransactions, val[0], val[1])
            currAnal = monthWiseAnalytics(**currAnalDict, accountNumber=accountNumber)
            currAnal.save()
        return Response(status=200)
    except Exception as e:
        return Response({"Error": str(e)}, status=400)
    
@api_view(['POST'])
def bank_statement_analyse(request):
    try:
        file = request.data.get('file')

        transactions = pd.read_csv(file)
        transactions = preprocessing(transactions)
        transactions['month'] = transactions['Date'].apply(getMonth)
        transactions['year'] = transactions['Date'].apply(getYear)

        accountNumber = -1
        analytics = []
        for val in processing(transactions, accountNumber):
            monthWiseTransactions = val[2]
            currAnalDict = processingMonthWiseTransactions(monthWiseTransactions, val[0], val[1])
            analytics.append(currAnalDict)
        return Response({"analytics": analytics}, status=200)
    except Exception as e:
        return Response({"Error": str(e)}, status=400)

