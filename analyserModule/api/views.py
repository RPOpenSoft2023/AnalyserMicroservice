from django.shortcuts import render
import pickle
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .serializers import BankAnalyserSerializer, GrossSummarySerializer, ParticularBankSerializer


class BankAnalysisResponseBody():
    def __init__(self,
                 volatilityScore,
                 bankName,
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
    resObj = BankAnalysisResponseBody(33, "AXIS")
    serializer = BankAnalyserSerializer(resObj)
    return Response(serializer.data)


@api_view(['GET'])
def bank_statement_analysis(request):
    resObj = BankAnalysisResponseBody(54, "SBI")
    serializer = BankAnalyserSerializer(resObj)
    return Response(serializer.data)


@api_view(['GET'])
def gross_summary(request):
    resObj = GrossSummaryResponseBody(100)
    serializer = GrossSummarySerializer(resObj)
    return Response(serializer.data)


@api_view(['GET'])
def bank_name(request, bankName):
    resObj = ParticularBankDetails(bankName)
    serializer = ParticularBankSerializer(resObj)
    return Response(serializer.data)

# Create your views here.
