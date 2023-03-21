import pandas as pd
import numpy as np
import re
from . import basicUtility as bu


def storeLoanInfo(bank_statement_var):
    bank_statement = bank_statement_var.copy()
    start_date = bank_statement['Date'][0]
    end_date = bank_statement['Date'][bank_statement.shape[0]-1]
    print(start_date, end_date)
    startDateTuple = bu.getMonthYearFromDate(start_date)
    endDateTuple = bu.getMonthYearFromDate(end_date)
    currMnth = startDateTuple[0]
    endMnth = endDateTuple[0]
    currYr = startDateTuple[1]
    endYr = endDateTuple[1]
    # Initialize dict
    keywords = ['LOAN', 'Loan', 'loan', 'LN', 'ln']
    monthly_loan = {}     # dict: {key -> (debit, credit loan)}
#     print(currMnth,currYr,endMnth,endYr)

    if (endYr == currYr):
        for month in range(currMnth, endMnth+1):
            print(month)
            if (currMnth < 10):
                currMnthStr = f"0{month}"
            else:
                currMnthStr = f"{month}"
            currStr = f"{currYr}-{currMnthStr}"
            print(currStr)
            monthly_loan[currStr] = [0, 0]
    else:
        for month in range(currMnth, 13):
            if (currMnth < 10):
                currMnthStr = f"0{month}"
            else:
                currMnthStr = f"{month}"
            currStr = f"{currYr}-{currMnthStr}"
            monthly_loan[currStr] = [0, 0]
        for month in range(1, endMnth+1):
            if (currMnth < 10):
                currMnthStr = f"0{currMnth}"
            else:
                currMnthStr = f"{currMnth}"
            currStr = f"{endYr}-{currMnthStr}"
            monthly_loan[currStr] = [0, 0]
    # for key,values in monthly_loan.items():
#         print(key,values)
    # update dict
    for row in range(bank_statement.shape[0]):
        msg = bank_statement['Particulars'][row]

        isloan = False
        if (msg == msg):    # is str
            string = re.split(r"[-/;,.\s]", msg)

            for word in string:
                if (word in keywords):
                    isloan = True
                    break

        if (isloan):
            date = bank_statement['Date'][row]
            string = date.split('-')
            currYr = string[0]
            currMnth = string[1]
            currStr = currYr + "-" + (currMnth)

            if (bank_statement['Debit'][row] == bank_statement['Debit'][row]):
                monthly_loan[currStr][0] += float(bank_statement['Debit'][row])
            elif (bank_statement['Credit'][row] == bank_statement['Credit'][row]):
                monthly_loan[currStr][1] += float(
                    bank_statement['Credit'][row])
        # print(monthly_loan)

    return monthly_loan


def getLoanInfo(start_date, end_date, bank_statement_var):
    bank_statement = bank_statement_var.copy()
    # Initialize dict
    keywords = ['LOAN', 'Loan', 'loan', 'LN', 'ln']
    monthly_loan = {}     # dict: {key -> (debit, credit loan)}
    currStr = start_date.split('-')
    currYr = int(currStr[0])
    currMnth = int(currStr[1])
    endStr = end_date.split('-')
    endYr = int(endStr[0])
    endMnth = int(endStr[1])
    mnth = start_date[:]

    while not (currMnth == endMnth and currYr == endYr):
        if (currMnth < 10):
            currMnthStr = "0" + ("% s" % currMnth)
        else:
            currMnthStr = ("% s" % currMnth)
        currStr = ("% s" % currYr) + "-" + currMnthStr
        monthly_loan[currStr] = [0, 0]    # debit, credit

        if (currMnth != 12):
            currMnth += 1
        else:
            currMnth = 1
            currYr += 1

    # update dict
    for row in range(bank_statement.shape[0]):
        msg = bank_statement['Particulars'][row]

        isloan = False
        if (msg == msg):    # is str
            string = re.split(r"[-/;,.\s]", msg)

            for word in string:
                if (word in keywords):
                    isloan = True
                    break

        if (isloan):
            date = bank_statement['Date'][row]
            string = date.split('-')
            currYr = string[0]
            currMnth = string[1]
            currStr = currYr + "-" + (currMnth)

            if (bank_statement['Debit'][row] == bank_statement['Debit'][row]):
                monthly_loan[currStr][0] += float(bank_statement['Debit'][row])
            elif (bank_statement['Credit'][row] == bank_statement['Credit'][row]):
                monthly_loan[currStr][1] += float(
                    bank_statement['Credit'][row])
        # print(monthly_loan)

    return monthly_loan
