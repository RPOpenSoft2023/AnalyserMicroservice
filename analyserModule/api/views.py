from django.shortcuts import render
import pickle
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
<<<<<<< HEAD
from rest_framework import status
from .models import monthWiseAnalytics
from .serializers import MonthWiseAnalyticsSerializer
=======
from .Helpers import Sources, Loans
import pandas as pd
# class BankAnalysisResponseBody():
#     def __init__(self,
#                  bankName,
#                  totalCreditDeposit=0,
#                  volatilityScore=0.1,
#                  avgMonthlySpending=0,
#                  percentMonthlySpending=0,
#                  SourcesOfLargeCredit=[],
#                  SourcesOfLargeDebit=[],
#                  frequencyOfCreditPayments=0,
#                  frequencyOfDebitPayments=0,
#                  frequencyOfPayment=0,
#                  spendingToIncomeRatio=0,
#                  daysToSpend50Percent=0,
#                  daysToSpend80Percent=0,
#                  recurringPayment=0
#                  ):
#         self.totalCreditDeposit = totalCreditDeposit
#         self.volatilityScore = volatilityScore
#         self.bankName = bankName
#         self.avgMonthlySpending = avgMonthlySpending
#         self.percentMonthlySpending = percentMonthlySpending
#         self.SourcesOfLargeCredit = SourcesOfLargeCredit
#         self.SourcesOfLargeDebit = SourcesOfLargeDebit
#         self.frequencyOfCreditPayments = frequencyOfCreditPayments
#         self.frequencyOfDebitPayments = frequencyOfDebitPayments
#         self.frequencyOfPayment = frequencyOfPayment
#         self.spendingToIncomeRatio = spendingToIncomeRatio
#         self.daysToSpend50Percent = daysToSpend50Percent
#         self.daysToSpend80Percent = daysToSpend80Percent
#         self.recurringPayment = recurringPayment


# class GrossSummaryResponseBody():
#     def __init__(self, avgBalance):
#         self.avgBalance = avgBalance


# class ParticularBankDetails():
#     def __init__(self, bankName):
#         self.bankName = bankName
>>>>>>> b5d62d462a4e2851340ef081014a9f53fa3b608a


@api_view(['GET'])
def bank_analysis(request):
<<<<<<< HEAD
    analysis = monthWiseAnalytics.objects.all()
    serializer = MonthWiseAnalyticsSerializer(analysis, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_statement(request):
    file = request.data['file']
    print(file)
    
    
=======
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
        # LoanInfo = Loans.getLoanInfo(startDate, endDate, bankStatement)
        # resObj = BankAnalysisResponseBody(
        #     bankName=BankName, totalCreditDeposit=totalCreditDeposits)
        # serializer = BankAnalyserSerializer(resObj)
        bankJson = bankStatement.to_json(orient="table", index=False)
        return Response(
            {
                "keys": temp.keys(),
                # "bankStatement": bankJson,
                "startDate": startDate,
                "endDate": endDate,
                # "bankStatement": bankStatement,
                "bankName": BankName,
                "totalCreditDeposits": totalCreditDeposits,
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
>>>>>>> b5d62d462a4e2851340ef081014a9f53fa3b608a
