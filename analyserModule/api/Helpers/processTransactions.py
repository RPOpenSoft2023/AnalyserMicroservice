import numpy as np
import pandas as pd
import re
import json
from ..models import monthWiseAnalytics
import requests
from django.conf import settings
import os
from rest_framework.exceptions import ValidationError

searchBase = list()

def preprocessing(transactions):
  transactions = transactions.dropna(axis = 0, subset=['Date', 'Particulars', 'Balance']) #removing rows with date as empty cell
  transactions = transactions.replace(np.nan, 0) #replacing NaN with 0.0
  requiredColumnslist = ['Date', 'Particulars', 'Debit', 'Credit', 'Balance'] #Columns list we need
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
  while(1) : 
    if (year > endYear) or ((year == endYear) and (month > endMonth)): 
      break
    else : 
      # check with backend if that exists, if it does't
      if(len(monthWiseAnalytics.objects.filter(month = month, year=year, accountNumber=accountNumber).values())== 0):		
        queriedTransactions = (transactions['month'] == month) & (transactions['year'] == year)

        currTransactions = transactions[queriedTransactions]
        
        # update this to banking microservice, and process this only when it's successfully updated
        if(token):  
          if  mergedTransactions.empty : 
              currTransactions = preProcessingMonthWise(currTransactions)
              mergedTransactions = currTransactions
          else : 
              currTransactions = preProcessingMonthWise(currTransactions)
              mergedTransactions = pd.concat([mergedTransactions, currTransactions])
        disjointList.append([month, year, currTransactions])
    month += 1
    if month == 12: 
      month = 0
      year += 1
  # if token and not mergedTransactions.empty: 
  mergedTransactions.to_csv("transactions.csv")
  with open("transactions.csv") as f:
    response = requests.post(settings.BANKING_MICROSERVICE + "add_transactions/", 
                            data={"account_number": accountNumber}, 
                            headers = { 'Authorization': token },
                            files={"transactions": f})
    assert(response.status_code != 200)
  os.remove("transactions.csv")
  return disjointList

def createSearchBase():
	sectorWiseCompanies=[]
	txt =""
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

## resolve error while updating the column for particulars
def preProcessingMonthWise(monthWiseTransactions):
  def updateParticular(particular):
    particular = (re.split(r"[-/;,.\s]", particular))
    particular = "".join(particular)
    return particular.lower()

	#function to search sector from a function
  def searchingSector(particular):
    sectorsList = searchBase[0]
    sectorWiseCompanies = searchBase[1]
    # preprocessing of data will be on top
    particular = ("".join(re.split(r"[-/;,.\s]", particular))).lower()
    for ind, sector in enumerate(sectorsList):
      for company in sectorWiseCompanies[ind] : 
        if(company in particular):
          return sector
    return sectorsList[-1]
  searchBase = createSearchBase()
  monthWiseTransactions.Particulars = monthWiseTransactions['Particulars'].apply(updateParticular)
  monthWiseTransactions['Category'] = monthWiseTransactions['Particulars'].apply(searchingSector)
  return monthWiseTransactions

def processingMonthWiseTransactions(monthWiseTransactions, month, year):
  def getTransactionTypes(monthWiseTransactions):
    dlen = len(monthWiseTransactions)
    transactionDict = dict()
    keywords = ['upi', 'cheque', 'neft', 'rdgs']
    for val in keywords : 
      queriedTransactions = (monthWiseTransactions['Particulars']).str.contains(val)
      dlen -= len(monthWiseTransactions[queriedTransactions])
      transactionDict[val] = len(monthWiseTransactions[queriedTransactions])
    transactionDict["others"] = dlen
    return transactionDict

  def getLoanDetails(monthWiseTransactions):
    queriedDataframe = monthWiseTransactions['Particulars'].str.contains('loan')
    monthWiseTransactions = monthWiseTransactions[queriedDataframe]
    creditMonthWiseLoanTransactions = monthWiseTransactions[monthWiseTransactions['Credit'] > 0]
    debitMonthWiseLoanTransactions = monthWiseTransactions[monthWiseTransactions['Credit'] <= 0]
    monthWiseCreditDebit = monthWiseTransactions[['Credit', 'Debit']].sum(axis = 0)
    credit = monthWiseCreditDebit['Credit']
    debit = monthWiseCreditDebit['Debit']
    return {
        "credit" : {
            "amount" : credit,
        },
        "debit" : {
            "amount" : debit,
        }
    }
  # average expense in a day
  def getAverageDayWiseExpense(monthWiseTransactions):
    debit = (monthWiseTransactions['Debit'].sum(axis = 0))
    return debit/30

  # average income in a day
  def getAverageDayWiseIncome(monthWiseTransactions):
    credit = (monthWiseTransactions['Credit'].sum(axis = 0))
    return credit/30

  def getCreditDebitFrequency(monthWiseTransactions):
    creditFreq =  len(monthWiseTransactions[monthWiseTransactions['Credit'] > 0])
    debitFreq = len(monthWiseTransactions) - creditFreq
    return {
        "creditFreq" : creditFreq,
        "debitFreq" : debitFreq
    }

  # income in a month
  def getTotalMonthIncome(monthWiseTransactions):
    credit = (monthWiseTransactions['Credit'].sum(axis = 0))
    return credit

  # spending in a month
  def getTotalMonthExpense(monthWiseTransactions):
    debit = (monthWiseTransactions['Debit'].sum(axis = 0))
    return debit

  # monthwise spending/Income ratio
  def getSpendingExpenseRatio(monthWiseTransactions):
    spending = getTotalMonthIncome(monthWiseTransactions)
    expense = getTotalMonthExpense(monthWiseTransactions)
    if(expense != 0):
      return spending/expense
    else:
      return "No expense in the month"
  
  def getCategorizedData(monthWiseTransactions) : 
    sectorsList = searchBase[0]
    sectorsData = dict()
    for sector in sectorsList : 
      queriedSectorWiseTransactions = monthWiseTransactions['Category'] == sector
      sectorWiseMonthTransactions = monthWiseTransactions[queriedSectorWiseTransactions]
      transactionTypes = getTransactionTypes(sectorWiseMonthTransactions)
      totalSectorMonthIncome = getTotalMonthIncome(sectorWiseMonthTransactions)
      totalSectorMonthExpense = getTotalMonthExpense(sectorWiseMonthTransactions)
      sectorData = {
          "transactionTypes" : transactionTypes,
          "totalSectorMonthIncome" : totalSectorMonthIncome,
          "totalSectorMonthExpense" : totalSectorMonthExpense,
          "count" : len(sectorWiseMonthTransactions)
      }
      sectorsData[sector] = sectorData
    return sectorsData
  
  # monthWiseTransactions = preProcessingMonthWise(monthWiseTransactions, searchBase)
  searchBase = createSearchBase()
  loanDetails = getLoanDetails(monthWiseTransactions)
  transactionTypes = getTransactionTypes(monthWiseTransactions) 
  averageDayWiseExpense = getAverageDayWiseExpense(monthWiseTransactions)
  averageDayWiseIncome = getAverageDayWiseIncome(monthWiseTransactions)
  creditDebitFrequency = getCreditDebitFrequency(monthWiseTransactions)
  totalMonthIncome = getTotalMonthIncome(monthWiseTransactions)
  totalMonthExpense = getTotalMonthExpense(monthWiseTransactions)
  spendingExpenseRatio = getSpendingExpenseRatio(monthWiseTransactions)
  categorizedData = getCategorizedData(monthWiseTransactions)
  return {
      "month" : month,
      "year" : year,
      "loanDetails" : loanDetails, 
      "transactionTypes" : transactionTypes,
      "averageDayWiseExpense" : averageDayWiseExpense,
      "averageDayWiseIncome" : averageDayWiseIncome,
      "creditDebitFrequency" : creditDebitFrequency,
      "totalMonthIncome" : totalMonthIncome,
      "totalMonthExpense" : totalMonthExpense,
      "spendingExpenseRatio" : spendingExpenseRatio,
      "categorizedData" : categorizedData
  }