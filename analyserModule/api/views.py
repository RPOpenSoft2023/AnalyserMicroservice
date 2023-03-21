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



@api_view(['GET'])
def bank_analysis(request):
    try:
        data = request.data
        startMonth, startYear, endMonth, endYear = data['start_month'], data['start_year'], data['end_month'], data['end_year']
        accountNumber = data['account_number']
        iterMonth, iterYear = startMonth, startYear

        analytics = []
        while((iterYear < endYear) or ((iterYear == endYear) and (iterMonth <= endMonth)) ):
            curr = monthWiseAnalytics.objects.filter(accountNumber=accountNumber, month=iterMonth, year=iterYear).values()[0]
            analytics.append(curr)
            if(iterMonth == 11):
                iterYear += 1
                iterMonth = 0
            else:
                iterMonth += 1
        return Response({"analytics": analytics})

    except Exception as e:
        return Response({"Error": e}, status=400)

@api_view(['POST'])
def bank_account_init(request):
    try:
        file = request.data['file']
        transactions = pd.read_csv(file)
        transactions = preprocessing(transactions)
        transactions['month'] = transactions['Date'].apply(getMonth)
        transactions['year'] = transactions['Date'].apply(getYear)
        for val in processing(transactions):
            monthWiseTransactions = val[2]
            currAnalDict = processingMonthWiseTransactions(monthWiseTransactions, val[0], val[1])
            currAnal = monthWiseAnalytics(**currAnalDict, accountNumber=12)
            currAnal.save()
        return Response(status=200)
    except Exception as e:
        return Response({"Error": str(e)}, status=400)

