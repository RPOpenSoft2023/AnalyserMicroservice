# import numpy as np
# import pandas as pd
# from datetime import date
# # from . import basicUtility as bu


# def Total_Freq_of_Debit_Payment(start_date, end_date, bank_statement_var):
#     bank_statement = bank_statement_var.copy()
#     bank_statement['Debit'] = bank_statement['Debit'].replace(np.nan, 0)
#     data_refined = bank_statement[(bank_statement['Date'] >= start_date) & (
#         bank_statement['Date'] <= end_date)]
#     num_rows = data_refined.shape[0]  # to count number of rows
#     debit_col = data_refined['Debit']
#     debit_freq = debit_col.value_counts()  # to get counts of all values
#     return (num_rows-debit_freq[0])


# def Total_Freq_of_Credit_Payment(start_date, end_date, bank_statement_var):
#     bank_statement = bank_statement_var.copy()
#     bank_statement['Credit'] = bank_statement['Credit'].replace(np.nan, 0)
#     data_refined = bank_statement[(bank_statement['Date'] >= start_date) & (
#         bank_statement['Date'] <= end_date)]
#     num_rows = data_refined.shape[0]  # to count number of rows
#     debit_col = data_refined['Credit']
#     debit_freq = debit_col.value_counts()  # to get counts of all values
#     return (num_rows-debit_freq[0])


# def freqOfCreditPayment(start_month, start_year, end_month, end_year, bank_statement_var):
#     bank_statement = bank_statement_var.copy()
#     freqList = []
#     if end_year == start_year:
#         for month in range(start_month, end_month+1):
#             start_date = bu.getStartDateFromMonthYear(month, start_year)
#             end_date = bu.getEndDateFromMonthYear(month, start_year)
#             freqList.append({str(month): Total_Freq_of_Credit_Payment(
#                 start_date, end_date, bank_statement)})
#     else:
#         for month in range(start_month, 13):
#             start_date = bu.getStartDateFromMonthYear(month, start_year)
#             end_date = bu.getEndDateFromMonthYear(month, start_year)
#             freqList.append({str(month): Total_Freq_of_Credit_Payment(
#                 start_date, end_date, bank_statement)})
#         for month in range(1, end_month+1):
#             start_date = bu.getStartDateFromMonthYear(month, end_year)
#             end_date = bu.getEndDateFromMonthYear(month, end_year)
#             freqList.append({str(month): Total_Freq_of_Credit_Payment(
#                 start_date, end_date, bank_statement)})
#     return freqList


# def freqOfDebitPayment(start_month, start_year, end_month, end_year, bank_statement_var):
#     bank_statement = bank_statement_var.copy()
#     freqList = []
#     if end_year == start_year:
#         for month in range(start_month, end_month+1):
#             start_date = bu.getStartDateFromMonthYear(month, start_year)
#             end_date = bu.getEndDateFromMonthYear(month, start_year)
#             freqList.append({str(month): Total_Freq_of_Debit_Payment(
#                 start_date, end_date, bank_statement)})
#     else:
#         for month in range(start_month, 13):
#             start_date = bu.getStartDateFromMonthYear(month, start_year)
#             end_date = bu.getEndDateFromMonthYear(month, start_year)
#             freqList.append({str(month): Total_Freq_of_Debit_Payment(
#                 start_date, end_date, bank_statement)})
#         for month in range(1, end_month+1):
#             start_date = bu.getStartDateFromMonthYear(month, end_year)
#             end_date = bu.getEndDateFromMonthYear(month, end_year)
#             freqList.append({str(month): Total_Freq_of_Debit_Payment(
#                 start_date, end_date, bank_statement)})
#     return freqList


# def avg_monthly_expenditure(start_date, end_date, bank_statement):
#     df = bank_statement.copy()
#     df = bank_statement.copy()
#     df["Balance"] = df["Balance"].fillna(0)
#     df["Credit"] = df["Credit"].fillna(0)
#     df["Debit"] = df["Debit"].fillna(0)
#     sum_spending = df['Debit'].sum()
#     start_date_list = start_date.split("-")
#     end_date_list = end_date.split("-")
#     d0 = date(int(start_date_list[0]), int(
#         start_date_list[1]), int(start_date_list[2]))
#     d1 = date(int(end_date_list[0]), int(
#         end_date_list[1]), int(end_date_list[2]))
#     avg_spending = sum_spending/((d1-d0).days)*30
#     print((d1-d0).days)
#     return avg_spending


# def daywise_credit_debit(day, month, year, bank_statement):
#     df = bank_statement.copy()
#     df["Balance"] = df["Balance"].fillna(0)
#     df["Credit"] = df["Credit"].fillna(0)
#     df["Debit"] = df["Debit"].fillna(0)
#     new_df = df[['Date', 'Debit', 'Credit']].copy()

#     new_df["Date"] = pd.to_datetime(new_df["Date"])
#     daywise_expenditure = new_df.loc[(pd.DatetimeIndex(df['Date']).month == month) & (
#         pd.DatetimeIndex(df['Date']).year == year) & (pd.DatetimeIndex(df['Date']).day == day)]

#     return daywise_expenditure


# def monthwise_credit_debit(months, years, bank_statement):
#     df = bank_statement.copy()
#     df["Balance"] = df["Balance"].fillna(0)
#     df["Credit"] = df["Credit"].fillna(0)
#     df["Debit"] = df["Debit"].fillna(0)
#     df["Date"] = pd.to_datetime(df["Date"])

#     credit = 0
#     debit = 0
#     data_of_month = df.loc[(pd.DatetimeIndex(df['Date']).month == months) & (
#         pd.DatetimeIndex(df['Date']).year == years)]
#     credit = data_of_month["Credit"].sum()
#     debit = data_of_month["Debit"].sum()
#     data = [{'Month': months, 'Year': years, 'Credit': credit, 'Debit': debit}]
#     return data


# def given_month_data(startmonth, startyear, endmonth, endyear, bankstatementvar):
#     bankstatement = bankstatementvar.copy()
#     data = []
#     if (endyear == startyear):
#         for month in range(startmonth, endmonth+1):
#             data.append(monthwise_credit_debit(
#                 month, startyear, bankstatement))
#     else:
#         for month in range(startmonth, 12):
#             data.append(monthwise_credit_debit(
#                 month, startyear, bankstatement))
#         for month in range(1, endmonth):
#             data.append(monthwise_credit_debit(month, endyear, bankstatement))

#     return data
