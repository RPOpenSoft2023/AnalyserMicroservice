import pandas as pd
import numpy as np


def total_credit_deposits(start_date, end_date, bank_statement_var):
    bank_statement = bank_statement_var.copy()
    bank_statement['Credit'] = bank_statement['Credit'].replace(np.nan, 0)
    data_frame_final = bank_statement[(bank_statement['Date'] >= start_date) & (
        bank_statement['Date'] <= end_date)]
    total_Sum_credit = data_frame_final['Credit'].sum()
    return total_Sum_credit


def LargeCredSources(start_date, end_date, bank_statement_var):
    bank_statement = bank_statement_var.copy()
    bank_statement['Debit'] = bank_statement['Debit'].replace(np.nan, 0)
    bank_statement['Credit'] = bank_statement['Credit'].replace(np.nan, 0)
    bankstatement1 = bank_statement[(bank_statement.Date >= start_date) & (
        bank_statement.Date <= end_date)]
    bankstatement1 = bankstatement1.sort_values('Date')
    bankstatement1.drop('Date', axis=1, inplace=True)
    bankstatement1 = bankstatement1.groupby('Particulars', as_index=False).agg(
        {'Debit': 'sum', 'Credit': 'sum', 'Balance': 'sum'})
    bankstatement1.sort_values('Credit', inplace=True, ascending=False)
    Result = list(bankstatement1.head()['Particulars'])
    return Result


def LargeDebitSources(start_date, end_date, bank_statement_var):
    bank_statement = bank_statement_var.copy()
    bank_statement['Debit'] = bank_statement['Debit'].replace(np.nan, 0)
    bank_statement['Credit'] = bank_statement['Credit'].replace(np.nan, 0)
    bankstatement2 = bank_statement[(bank_statement.Date >= start_date) & (
        bank_statement.Date <= end_date)]
    bankstatement2 = bankstatement2.sort_values('Date')
    bankstatement2.drop('Date', axis=1, inplace=True)
    bankstatement2 = bankstatement2.groupby('Particulars', as_index=False).agg(
        {'Debit': 'sum', 'Credit': 'sum', 'Balance': 'sum'})
    bankstatement2.sort_values('Debit', inplace=True, ascending=False)
    Result = list(bankstatement2.head()['Particulars'])
    return Result
