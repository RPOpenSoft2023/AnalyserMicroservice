# deposits made into the account over a specific period
# %%
import numpy as np
import pandas as pd  # To read bank_statement

bank_statement = pd.read_csv('analyserModule/axis_bank_statement1.csv')

def IncomeCalculator(start_date,end_date,bank_statement):
    bank_statement['Date'] = pd.to_datetime(bank_statement['Date'])
    bank_statement.set_index('Date', inplace=True)    
    selected_rows = bank_statement.loc[start_date:end_date]
    Income = selected_rows['Credit'].sum()
    return Income

def TotalIncomeCalculator(bank_statement):
    total_income = bank_statement['Credit'].sum()
    return total_income

def MonthlyIncomeCalculator(start_date,end_date,bank_statement):
    start_date = pd.to_datetime(start_date).date
    end_date = pd.to_datetime(end_date).date
    bank_statement['Date'] = pd.to_datetime(bank_statement['Date'])
    bank_statement.set_index('Date', inplace=True)
    selected_rows = bank_statement.loc[start_date:end_date]
    Income = selected_rows['Credit'].sum()
    monthdiff = (end_date - start_date)/np.timedelta64(1,'M')
    print(monthdiff)
    MonthlyIncome = Income/monthdiff
    return MonthlyIncome

start_date = '2020-01-02'
end_date = '2020-01-14'
print(TotalIncomeCalculator(bank_statement))
print(IncomeCalculator(start_date,end_date,bank_statement))
print(MonthlyIncomeCalculator(start_date,end_date,bank_statement))
