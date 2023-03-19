from django.shortcuts import render
import pickle
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .serializers import BankAnalyserSerializer, GrossSummarySerializer, ParticularBankSerializer
from .Helpers import Sources, Loans


class BankAnalysisResponseBody():
    def __init__(self,
                 bankName,
                 totalCreditDeposit=0,
                 volatilityScore=0.1,
                 avgMonthlySpending=0,
                 percentMonthlySpending=0,
                 SourcesOfLargeCredit=[],
                 SourcesOfLargeDebit=[],
                 frequencyOfCreditPayments=0,
                 frequencyOfDebitPayments=0,
                 frequencyOfPayment=0,
                 spendingToIncomeRatio=0,
                 daysToSpend50Percent=0,
                 daysToSpend80Percent=0,
                 recurringPayment=0
                 ):
        self.totalCreditDeposit = totalCreditDeposit
        self.volatilityScore = volatilityScore
        self.bankName = bankName
        self.avgMonthlySpending = avgMonthlySpending
        self.percentMonthlySpending = percentMonthlySpending
        self.SourcesOfLargeCredit = SourcesOfLargeCredit
        self.SourcesOfLargeDebit = SourcesOfLargeDebit
        self.frequencyOfCreditPayments = frequencyOfCreditPayments
        self.frequencyOfDebitPayments = frequencyOfDebitPayments
        self.frequencyOfPayment = frequencyOfPayment
        self.spendingToIncomeRatio = spendingToIncomeRatio
        self.daysToSpend50Percent = daysToSpend50Percent
        self.daysToSpend80Percent = daysToSpend80Percent
        self.recurringPayment = recurringPayment


class GrossSummaryResponseBody():
    def __init__(self, avgBalance):
        self.avgBalance = avgBalance


class ParticularBankDetails():
    def __init__(self, bankName):
        self.bankName = bankName


@api_view(['GET'])
def bank_analysis(request):
    temp = (request.body.decode('utf-8'))
    temp = json.loads(temp)
    print(temp['messsage'])
    resObj = BankAnalysisResponseBody(33, "AXIS")
    serializer = BankAnalyserSerializer(resObj)
    return Response(serializer.data)


@api_view(['GET'])
def bank_statement_analysis(request):
    temp = (request.body.decode('utf-8'))
    temp = json.loads(temp)
    startDate = temp["start_date"]
    endDate = temp["end_date"]
    bankStatement = temp["bank_statement"]
    BankName = temp["bank_name"]
    totalCreditDeposits = Sources.total_credit_deposits(
        startDate, endDate, bankStatement)
    LoanInfo = Loans.getLoanInfo(startDate, endDate, bankStatement)
    resObj = BankAnalysisResponseBody(
        totalCreditDeposits=totalCreditDeposits, bankName=BankName)
    serializer = BankAnalyserSerializer(resObj)
    return Response(serializer.data)


@api_view(['GET'])
def gross_summary(request):
    temp = (request.body.decode('utf-8'))
    temp = json.loads(temp)
    resObj = GrossSummaryResponseBody(100)
    serializer = GrossSummarySerializer(resObj)
    return Response(serializer.data)


@api_view(['GET'])
def bank_name(request, bankName):
    temp = (request.body.decode('utf-8'))
    temp = json.loads(temp)
    resObj = ParticularBankDetails(bankName)
    serializer = ParticularBankSerializer(resObj)
    return Response(serializer.data)

# Create your views here.