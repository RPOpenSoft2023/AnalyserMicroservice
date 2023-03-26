from django.shortcuts import render
import pickle
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import render
# from .Helpers import Sources, Loans, Info, PaymentStat
from .Helpers.processTransactions import preprocessing, processing, processingMonthWiseTransactions, getMonth, getYear, getTaxCaution, getRTGSCaution, getATMFCaution, getEqualDebitCredit, getNegativeBalanceCaution, getHolidayChequeList, getCashCaution, getHighHolidayCredit, getComputeBalanceError
from .models import monthWiseAnalytics
import pandas as pd
from django.conf import settings
import requests


@api_view(['GET'])
def bank_analysis(request):
    try:
        data = request.GET
        startMonth, startYear, endMonth, endYear = map(
            int, [data['start_month'], data['start_year'], data['end_month'], data['end_year']])
        accountNumber = int(data['account_number'])
        token = request.headers.get('Authorization')
        if (token):
            response = requests.get(settings.USER_MICROSERVICE + "verify_token",
                                    headers={'Authorization': token}
                                    )
            if (response.status_code != 200):
                return Response({"message": "not logged in"}, status=401)
        else:
            return Response({"message": "not logged in"}, status=401)

        iterMonth, iterYear = startMonth, startYear

        analytics = []
        taxFaults = []
        rtgsFaults = []
        atmFaults = []
        cashFaults = []
        negativeComputedBalance = []
        equalDebitCredit = []
        chequeInHolidayCaution = []
        highHolidayCredit = []
        computedBalanceError = []
        while ((iterYear < endYear) or ((iterYear == endYear) and (iterMonth <= endMonth))):
            currData = monthWiseAnalytics.objects.filter(
                accountNumber=accountNumber, month=iterMonth, year=iterYear).values()
            if (len(currData) == 0):
                return Response({"message": "analysis failed due to insufficient data"}, status=400)
            curr = currData[0]
            analytics.append(curr)
            if (iterMonth == 11):
                iterYear += 1
                iterMonth = 0
            else:
                iterMonth += 1

            isEqualDebitCredit = getEqualDebitCredit(curr)
            if (isEqualDebitCredit[0]):
                equalDebitCredit.append(
                    (isEqualDebitCredit[1], isEqualDebitCredit[2]))

            taxFaults += getTaxCaution(curr)
            rtgsFaults += getRTGSCaution(curr)
            atmFaults += getATMFCaution(curr)
            cashFaults += getCashCaution(curr)
            negativeComputedBalance += getNegativeBalanceCaution(curr)
            chequeInHolidayCaution += getHolidayChequeList(curr)
            highHolidayCredit += getHighHolidayCredit(curr)
            computedBalanceError += getComputeBalanceError(curr)

        Cautions = {
            "taxFlag": (len(taxFaults), taxFaults),
            "rtgsFlag": (len(rtgsFaults), rtgsFaults),
            "atmFlag": (len(atmFaults), atmFaults),
            "negativeComputedBalanceFlag": (len(negativeComputedBalance), negativeComputedBalance),
            "equalDebitCreditFlag": (len(equalDebitCredit), equalDebitCredit),
            "chequeInHolidayFlag": (len(chequeInHolidayCaution), chequeInHolidayCaution),
            "highCashCreditFlag": (len(cashFaults), cashFaults),
            "highHolidayCredit": (len(highHolidayCredit), highHolidayCredit),
            "computedBalanceError": (len(computedBalanceError), computedBalanceError)
        }
        # print(cautions)
        return Response({"analytics": analytics, "Cautions": Cautions})
    except Exception as e:
        return Response({"Error": str(e)}, status=400)


@api_view(['POST'])
def bank_account_init(request):
    try:
        file = request.data['file']
        token = request.headers.get('Authorization')
        accountNumber = request.data.get('account_number')

        if (token):
            response = requests.get(getattr(settings, "USER_MICROSERVICE", None) + "verify_token",
                                    headers={'Authorization': token}
                                    )
            if (response.status_code != 200):
                return Response({"message": "not logged in"}, status=401)
        else:
            return Response({"message": "not logged in"}, status=401)

        if (not accountNumber):
            return Response({"message": "account number required"}, status=400)

        transactions = pd.read_csv(file)
        transactions = preprocessing(transactions)
        transactions['month'] = transactions['Date'].apply(getMonth)
        transactions['year'] = transactions['Date'].apply(getYear)
        lastBalance = 0
        for val in processing(transactions, accountNumber, token):
            monthWiseTransactions = val[2]
            currAnalDict = processingMonthWiseTransactions(
                monthWiseTransactions, val[0], val[1], lastBalance)
            cautionData = currAnalDict['storedCautionData']
            lastBalance = cautionData['lastBalance']
            currAnal = monthWiseAnalytics(
                **currAnalDict, accountNumber=accountNumber)
            currAnal.save()
        return Response({"message": "statement added successfully"}, status=200)
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
        transactions = transactions.reset_index()
        accountNumber = -1
        lastBalance = 0
        analytics = []
        taxFaults = []
        rtgsFaults = []
        atmFaults = []
        cashFaults = []
        negativeComputedBalance = []
        equalDebitCredit = []
        chequeInHolidayCaution = []
        highHolidayCredit = []
        computedBalanceError = []
        for val in processing(transactions, accountNumber):
            monthWiseTransactions = val[2]
            currAnalDict = processingMonthWiseTransactions(
                monthWiseTransactions, val[0], val[1], lastBalance)
            cautionData = currAnalDict['storedCautionData']
            lastBalance = cautionData['lastBalance']
            analytics.append(currAnalDict)
            isEqualDebitCredit = getEqualDebitCredit(currAnalDict)
            if (isEqualDebitCredit[0]):
                equalDebitCredit.append(
                    (isEqualDebitCredit[1], isEqualDebitCredit[2]))

            taxFaults += getTaxCaution(currAnalDict)
            rtgsFaults += getRTGSCaution(currAnalDict)
            atmFaults += getATMFCaution(currAnalDict)
            cashFaults += getCashCaution(currAnalDict)
            negativeComputedBalance += getNegativeBalanceCaution(currAnalDict)
            chequeInHolidayCaution += getHolidayChequeList(currAnalDict)
            highHolidayCredit += getHighHolidayCredit(currAnalDict)
            computedBalanceError += getComputeBalanceError(currAnalDict)

        Cautions = {
            "taxFlag": (len(taxFaults), taxFaults),
            "rtgsFlag": (len(rtgsFaults), rtgsFaults),
            "atmFlag": (len(atmFaults), atmFaults),
            "negativeComputedBalanceFlag": (len(negativeComputedBalance), negativeComputedBalance),
            "equalDebitCreditFlag": (len(equalDebitCredit), equalDebitCredit),
            "chequeInHolidayFlag": (len(chequeInHolidayCaution), chequeInHolidayCaution),
            "highCashCreditFlag": (len(cashFaults), cashFaults),
            "highHolidayCredit": (len(highHolidayCredit), highHolidayCredit),
            "computedBalanceError": (len(computedBalanceError), computedBalanceError)
        }
        return Response({"analytics": analytics, "Cautions": Cautions}, status=200)
    except Exception as e:
        return Response({"Error": str(e)}, status=400)


@api_view(['PUT'])
def edit_transaction(request):
    try:
        token = request.headers.get('Authorization')
        req_fields = ['transaction_id', 'category']
        data = {}
        for field in req_fields:
            if not field in request.data:
                raise ValidationError({field: f'{field} is required'})
            else:
                data[field] = request.data.get(field)

        response = requests.get(settings.BANKING_MICROSERVICE + "get_transaction/",
                                data={
                                    'transaction_id': data['transaction_id']},
                                headers={'Authorization': token})
        if not response.ok:
            raise ValidationError(response.json())
        transaction = response.json()
        # transaction = {"id": 12323, "date": "2020-01-01", "category": "travelling", "credit": 12, "debit": 0, "account_number": 123}
        # data = {"category": "shoppingAndFood"}
        # print(transaction['date'])
        date = transaction.date
        analytics = monthWiseAnalytics.objects.filter(year=int(str(date).split(
            '-')[0]), month=int(str(date).split('-')[1]) - 1, accountNumber=transaction.get('account'))[0]
        categorizedData = analytics.categorizedData

        # update transaction types count
        old_category = transaction.category
        # categorizedData[old_category]['transaction_types'][get_type(transaction['description'])] -=1
        # categorizedData[data['category']]['transaction_types'][get_type(transaction['category'])] +=1
        keywords = ['upi', 'cheque', 'neft', 'rdgs']
        typeDict = {}
        present = 0
        for val in keywords:
            curr = val in transaction.description
            typeDict[val] = 1 if curr else 0
            present = present | curr
        typeDict["others"] = present ^ 1

        for val in typeDict:
            categorizedData[old_category]['transactionTypes'][val] -= typeDict[val]
        for val in typeDict:
            categorizedData[data['category']
                            ]['transactionTypes'][val] += typeDict[val]

        # category totals
        categorizedData[old_category]['totalSectorMonthIncome'] -= transaction['credit']
        categorizedData[data['category']
                        ]['totalSectorMonthIncome'] += transaction['credit']
        categorizedData[old_category]['totalSectorMonthExpense'] -= transaction['debit']
        categorizedData[data['category']
                        ]['totalSectorMonthExpense'] += transaction['debit']

        response = requests.put(settings.BANKING_MICROSERVICE + "edit_transaction/",
                                data={
                                    'transaction_id': data['transaction_id'],
                                    'category': data['category'],
                                    'note': request.data.get('note', None),
                                },
                                headers={'Authorization': token})
        if not response.ok:
            raise ValidationError(response.json())

        analytics.categorizedData = categorizedData
        analytics.save()

        return Response({"message": "transaction updated"})

    except Exception as e:
        return Response({"Error": str(e)}, status=400)
