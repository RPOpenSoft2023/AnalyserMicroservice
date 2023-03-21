from django.shortcuts import render
import pickle
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .Helpers import Sources, Loans, Info, PaymentStat
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


@api_view(['GET'])
def bank_statement_analysis(request):
    try:
        temp = (request.body.decode('utf-8'))
        temp = json.loads(temp)
        bankStatement = pd.DataFrame(temp["bank_statement"])
        startDate = temp["start_date"]
        endDate = temp["end_date"]
        # bankStatement = temp["bank_statement"]
        BankName = temp["bank_name"]
        totalCreditDeposits = Sources.total_credit_deposits(
            startDate, endDate, bankStatement)
        income = Info.IncomeCalculator(startDate, endDate, bankStatement)
        totalIncome = Info.TotalIncomeCalculator(bankStatement)
        # LoanInfo = Loans.getLoanInfo(startDate, endDate, bankStatement)
        # resObj = BankAnalysisResponseBody(
        #     bankName=BankName, totalCreditDeposit=totalCreditDeposits)
        # serializer = BankAnalyserSerializer(resObj)
        # bankJson = bankStatement.to_json(orient="table", index=False)
        largeCreditSources = Sources.LargeCredSources(
            startDate, endDate, bankStatement)
        # print(largeCreditSources)
        largeDebitSources = Sources.LargeDebitSources(
            startDate, endDate, bankStatement)
        startList = str(startDate).split('-')
        endList = str(endDate).split('-')
        startMonth = int(startList[1])
        startYear = int(startList[0])
        endMonth = int(endList[1])
        endYear = int(endList[0])

        data = PaymentStat.given_month_data(
            startMonth, endMonth, startYear, endYear)
        # print(type(startMonth))
        # print(type(endMonth))
        return Response(
            {
                "keys": temp.keys(),
                # "bankStatement": bankJson,
                "start_date": startDate,
                "end_date": endDate,
                # "bankStatement": bankStatement,
                "bank_name": BankName,
                "total_credit_deposits": totalCreditDeposits,
                "specific_income": income,
                "total_income": totalIncome,
                "large_credit_sources": largeCreditSources,
                "large_debit_sources": largeDebitSources,
                "start_month": startMonth,
                "start_year": startYear,
                "end_month": endMonth,
                "end_year": endYear,
                # "bank_data": data,
            },
            status=200
        )
    except Exception as e:
        return Response({"Error": e}, status=400)