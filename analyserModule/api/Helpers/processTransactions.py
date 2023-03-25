import numpy as np
import pandas as pd
import re
import json
from ..models import monthWiseAnalytics
import requests
from django.conf import settings
import os
import holidays
import datetime


def preprocessing(transactions):
    # removing rows with date as empty cell
    transactions = transactions.dropna(
        axis=0, subset=['Date', 'Particulars', 'Balance'])
    transactions = transactions.replace(np.nan, 0)  # replacing NaN with 0.0
    requiredColumnslist = ['Date', 'Particulars', 'Debit',
                           'Credit', 'Balance']  # Columns list we need
    transactions = transactions[requiredColumnslist]
    return transactions


def getStartDate(transactions):
    date = dict()
    date['month'] = transactions['month'].iloc[0]
    date['year'] = transactions['year'].iloc[0]
    return date


def getEndDate(transactions):
    date = dict()
    date['month'] = transactions['month'].iloc[-1]
    date['year'] = transactions['year'].iloc[-1]
    return date


def processing(transactions, accountNumber, token=None):
    disjointList = []
    month = getStartDate(transactions).get('month')
    year = getStartDate(transactions).get('year')
    endMonth = getEndDate(transactions).get('month')
    endYear = getEndDate(transactions).get('year')
    mergedTransactions = pd.DataFrame()
    while (1):
        if (year > endYear) or ((year == endYear) and (month > endMonth)):
            break
        else:
            # check with backend if that exists, if it does't
            if (len(monthWiseAnalytics.objects.filter(month=month, year=year, accountNumber=accountNumber).values()) == 0):
                queriedTransactions = (transactions['month'] == month) & (
                    transactions['year'] == year)

                currTransactions = transactions[queriedTransactions]

                # update this to banking microservice, and process this only when it's successfully updated
                if (token):
                    if mergedTransactions.empty:
                        mergedTransactions = currTransactions
                    else:
                        mergedTransactions = pd.concat(
                            [mergedTransactions, currTransactions])
                disjointList.append([month, year, currTransactions])
        month += 1
        if month == 12:
            month = 0
            year += 1
    if token and not mergedTransactions.empty:
        mergedTransactions.to_csv("transactions.csv")
        with open("transactions.csv") as f:
            response = requests.post(settings.BANKING_MICROSERVICE + "add_transactions/",
                                     data={"account_number": accountNumber},
                                     headers={'Authorization': token},
                                     files={"transactions": f})
            print(response.json(), response.status_code)
        os.remove("transactions.csv")
    return disjointList


def createSearchBase():
    sectorWiseCompanies = []
    txt = ""
    with open('sectors.txt') as f:
        txt = json.loads(f.readlines()[0])
    sectorsList = list(txt.keys())
    for val in sectorsList:
        sectorWiseCompanies.append(txt[val])
    return [sectorsList, sectorWiseCompanies]


def getMonth(date):
    date = str(date).split('-')
    return int(date[1]) - 1


def getYear(date):
    date = str(date).split('-')
    return int(date[0])

# resolve error while updating the column for particulars


def preProcessingMonthWise(monthWiseTransactions, searchBase):

    def updateParticular(particular):
        particular = (re.split(r"[-/;,.\s]", particular))
        particular = "".join(particular)
        return particular.lower()

    # function to search sector from a function
    def searchingSector(particular):
        sectorsList = searchBase[0]
        sectorWiseCompanies = searchBase[1]
        # preprocessing of data will be on top
        particular = ("".join(re.split(r"[-/;,.\s]", particular))).lower()
        for ind, sector in enumerate(sectorsList):
            for company in sectorWiseCompanies[ind]:
                if (company in particular):
                    return sector
        return sectorsList[-1]

    monthWiseTransactions.Particulars = monthWiseTransactions['Particulars'].apply(
        updateParticular)
    monthWiseTransactions['Sector'] = monthWiseTransactions['Particulars'].apply(
        searchingSector)
    return monthWiseTransactions


def processingMonthWiseTransactions(monthWiseTransactions, month, year):

    searchBase = createSearchBase()

    def getTransactionTypes(monthWiseTransactions):
        dlen = len(monthWiseTransactions)
        transactionDict = dict()
        keywords = ['upi', 'cheque', 'neft', 'rtgs']
        for val in keywords:
            queriedTransactions = (
                monthWiseTransactions['Particulars']).str.contains(val)
            dlen -= len(monthWiseTransactions[queriedTransactions])
            transactionDict[val] = len(
                monthWiseTransactions[queriedTransactions])
        transactionDict["others"] = dlen
        return transactionDict

    def getLoanDetails(monthWiseTransactions):
        queriedDataframe = monthWiseTransactions['Particulars'].str.contains(
            'loan')
        monthWiseTransactions = monthWiseTransactions[queriedDataframe]
        creditMonthWiseLoanTransactions = monthWiseTransactions[monthWiseTransactions['Credit'] > 0]
        debitMonthWiseLoanTransactions = monthWiseTransactions[monthWiseTransactions['Credit'] <= 0]
        monthWiseCreditDebit = monthWiseTransactions[[
            'Credit', 'Debit']].sum(axis=0)
        credit = monthWiseCreditDebit['Credit']
        debit = monthWiseCreditDebit['Debit']
        return {
            "credit": {
                "amount": credit,
            },
            "debit": {
                "amount": debit,
            }
        }
    # average expense in a day

    def getAverageDayWiseExpense(monthWiseTransactions):
        debit = (monthWiseTransactions['Debit'].sum(axis=0))
        return debit/30

    # average income in a day
    def getAverageDayWiseIncome(monthWiseTransactions):
        credit = (monthWiseTransactions['Credit'].sum(axis=0))
        return credit/30

    def getCreditDebitFrequency(monthWiseTransactions):
        creditFreq = len(
            monthWiseTransactions[monthWiseTransactions['Credit'] > 0])
        debitFreq = len(monthWiseTransactions) - creditFreq
        return {
            "creditFreq": creditFreq,
            "debitFreq": debitFreq
        }

    # income in a month
    def getTotalMonthIncome(monthWiseTransactions):
        credit = (monthWiseTransactions['Credit'].sum(axis=0))
        return credit

    # spending in a month
    def getTotalMonthExpense(monthWiseTransactions):
        debit = (monthWiseTransactions['Debit'].sum(axis=0))
        return debit

#   # monthwise spending/Income ratio
    def getSpendingExpenseRatio(monthWiseTransactions):
        spending = getTotalMonthIncome(monthWiseTransactions)
        expense = getTotalMonthExpense(monthWiseTransactions)
        if (expense != 0):
            return spending/expense
        else:
            return "No expense in the month"

    def getCategorizedData(monthWiseTransactions):
        sectorsList = searchBase[0]
        sectorsData = dict()
        for sector in sectorsList:
            queriedSectorWiseTransactions = monthWiseTransactions['Sector'] == sector
            sectorWiseMonthTransactions = monthWiseTransactions[queriedSectorWiseTransactions]
            transactionTypes = getTransactionTypes(sectorWiseMonthTransactions)
            totalSectorMonthIncome = getTotalMonthIncome(
                sectorWiseMonthTransactions)
            totalSectorMonthExpense = getTotalMonthExpense(
                sectorWiseMonthTransactions)
            sectorData = {
                "transactionTypes": transactionTypes,
                "totalSectorMonthIncome": totalSectorMonthIncome,
                "totalSectorMonthExpense": totalSectorMonthExpense,
                "count": len(sectorWiseMonthTransactions)
            }
            sectorsData[sector] = sectorData
        return sectorsData
    # get taxed data
    keyWords = ['gst', 'tax', 'tds']

    # to get taxed data
    def getTaxedData(monthWiseTransactions):
        taxedTransactions = []
        for row in monthWiseTransactions.iterrows():
            tax = False
            for key in keyWords:
                tax = tax or (key in row[1].Particulars)
            if (tax):
                taxedTransactions.append(row[1].to_dict())
        return taxedTransactions

    # to rtgs data
    def getRTGSData(monthWiseTransactions):
        rtgsTransactions = []
        for row in monthWiseTransactions.iterrows():
            if ('rtgs' in row[1].Particulars):
                rtgsTransactions.append(row[1].to_dict())
        return rtgsTransactions

    # to get atm data
    def getATMData(monthWiseTransactions):
        atmData = []
        for row in monthWiseTransactions.iterrows():
            if ('atm' in row[1].Particulars and 'cash' in row[1].Particulars):
                atmData.append(row[1].to_dict())
        return atmData

    # getting the cash data
    def getCashData(monthWiseTransactions):
        cashData = []
        for row in monthWiseTransactions.iterrows():
            if ('cash' in row[1].Particulars):
                cashData.append(row[1].to_dict())
        return cashData

    def getDateTimeFormat(dateString):
        dateList = dateString.split('-')
        return datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))

    # to get holiday data

    def getHolidayData(monthWiseTransactions):
        holidayTransactionData = []
        for val in monthWiseTransactions.iterrows():
            holidayIndia = holidays.India(val[1].year)
            holidayList = list(holidayIndia.keys())
            if getDateTimeFormat(val[1].Date) in holidayList:
                holidayName = (holidayIndia[val[1].Date])
                holidayTransactionData.append((holidayName, val[1].to_dict()))
        return holidayTransactionData

    # caution data for negative balance
    def getNegativeBalanceTransactions(monthWiseTransactions):
        negativeBalData = []
        for val in monthWiseTransactions.iterrows():
            if (val[1].Balance < 0):
                negativeBalData.append(val[1].to_dict())
        return negativeBalData

    monthWiseTransactions = preProcessingMonthWise(
        monthWiseTransactions, searchBase)
    loanDetails = getLoanDetails(monthWiseTransactions)
    transactionTypes = getTransactionTypes(monthWiseTransactions)
    averageDayWiseExpense = getAverageDayWiseExpense(monthWiseTransactions)
    averageDayWiseIncome = getAverageDayWiseIncome(monthWiseTransactions)
    creditDebitFrequency = getCreditDebitFrequency(monthWiseTransactions)
    totalMonthIncome = getTotalMonthIncome(monthWiseTransactions)
    totalMonthExpense = getTotalMonthExpense(monthWiseTransactions)
    spendingExpenseRatio = getSpendingExpenseRatio(monthWiseTransactions)
    categorizedData = getCategorizedData(monthWiseTransactions)
    taxedData = getTaxedData(monthWiseTransactions)
    rtgsData = getRTGSData(monthWiseTransactions)
    atmData = getATMData(monthWiseTransactions)
    holidayTransactionData = getHolidayData(monthWiseTransactions)
    cashData = getCashData(monthWiseTransactions)
    negativeBalanceData = getNegativeBalanceTransactions(monthWiseTransactions)
    # print(taxedData)
    # print(rtgsData)
    storedCautionData = {
        "taxedData": taxedData,
        "rtgsData": rtgsData,
        "atmData": atmData,
        "cashData": cashData,
        "holidayTransactionData": holidayTransactionData,
        "negativeBalanceData": (len(negativeBalanceData), negativeBalanceData),
    }
    return {
        "month": month,
        "year": year,
        "loanDetails": loanDetails,
        "transactionTypes": transactionTypes,
        "averageDayWiseExpense": averageDayWiseExpense,
        "averageDayWiseIncome": averageDayWiseIncome,
        "creditDebitFrequency": creditDebitFrequency,
        "totalMonthIncome": totalMonthIncome,
        "totalMonthExpense": totalMonthExpense,
        "spendingExpenseRatio": spendingExpenseRatio,
        "categorizedData": categorizedData,
        "storedCautionData": storedCautionData
    }


def getTaxCaution(curr):
    taxFault = []
    cautionList = curr.get('storedCautionData')
    taxList = cautionList['taxedData']
    for taxData in taxList:
        if taxData['Debit'] % 10 == 0:
            taxFault.append(taxData)
    return taxFault


def getRTGSCaution(curr):
    rtgsFault = []
    cautionList = curr.get('storedCautionData')
    rtgsList = cautionList['rtgsData']
    for rtgsData in rtgsList:
        if rtgsData['Debit'] <= 200000 or rtgsData['Credit'] <= 200000:
            rtgsFault.append(rtgsData)
    return rtgsFault


def getATMFCaution(curr):
    atmFault = []
    cautionList = curr.get('storedCautionData')
    atmList = cautionList['atmData']
    for atmData in atmList:
        if atmData['Debit'] >= 20000:
            atmFault.append(atmData)
    return atmFault


def getEqualDebitCredit(curr):

    creditDebitFreq = curr.get('creditDebitFrequency')
    boolVal = (creditDebitFreq['creditFreq'] == creditDebitFreq['debitFreq']) or (
        curr.get('totalMonthIncome') == curr.get('totalMonthExpense'))
    month = curr.get('month')
    year = curr.get('year')
    return (boolVal, month, year)


def getNegativeBalanceCaution(curr):
    negBalList = []
    cautionList = curr.get('storedCautionData')
    negativeBalanceData = cautionList['negativeBalanceData']
    for data in negativeBalanceData[1]:
        negBalList.append(data)
    return negBalList


keyWord = ['cheque', 'clg']


def getHolidayChequeList(curr):
    chequeInHoliday = []
    cautionList = curr.get('storedCautionData')
    holidayTransactionData = cautionList['holidayTransactionData']
    for data in holidayTransactionData:
        boolVal = False
        for key in keyWord:
            boolVal = boolVal or key in data[1]['Particulars']
        if boolVal:
            print(data)
            chequeInHoliday.append(data)
    return chequeInHoliday
