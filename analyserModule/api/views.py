from django.shortcuts import render
import pickle
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .Helpers import Sources, Loans, Info, PaymentStat
import pandas as pd


@api_view(['GET'])
def bank_analysis(request):
    try:
        temp = (request.body.decode('utf-8'))
        temp = json.loads(temp)
        bankAnalysis = temp["bankAnalysis"]
    # resObj = BankAnalysisResponseBody(33, "AXIS")
    # serializer = BankAnalyserSerializer(resObj)
    # return Response(serializer.data)
        return Response({"bankAnalysis": bankAnalysis})
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
            startMonth, startYear, endMonth, endYear, bankStatement)
        print(startMonth, endMonth)
        loan_info = Loans.storeLoanInfo(bankStatement)
        # print(type(startMonth))
        # print(type(endMonth))
        print(data)
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
                "bank_data": data,
                "loan_info": loan_info,
            },
            status=200
        )
    except Exception as e:
        return Response({"Error": e}, status=400)


@ api_view(['GET'])
def gross_summary(request):
    try:
        temp = (request.body.decode('utf-8'))
        temp = json.loads(temp)
        avgBal = temp["avgBal"]
        # resObj = GrossSummaryResponseBody(temp["avgBal"])
        # serializer = GrossSummarySerializer(resObj)
        return Response({
            "avgBal": avgBal
        }, status=200)
    except Exception as e:
        return Response({"Error": e}, status=400)


@ api_view(['GET'])
def bank_name(request, bankName):
    try:
        temp = (request.body.decode('utf-8'))
        temp = json.loads(temp)
        # resObj = ParticularBankDetails(bankName)
        # serializer = ParticularBankSerializer(resObj)

        return Response({
            "bankName": bankName
        }, status=200)
    except Exception as e:
        return Response({"Error": e}, status=400)

# Create your views here.
