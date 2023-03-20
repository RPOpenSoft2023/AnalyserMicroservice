import pandas as pd
import numpy as np

#
def total_credit_deposits(start_date, end_date, bank_statement):
  bank_statement['Credit']= bank_statement['Credit'].replace(np.nan,0)
  data_frame_final = bank_statement[(bank_statement['Date']>=start_date) & (bank_statement['Date']<=end_date)]
  total_Sum_credit = data_frame_final['Credit'].sum()
  return total_Sum_credit