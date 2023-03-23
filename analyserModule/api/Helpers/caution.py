def giveRTGSErrors(transaction):
    count = 0
    transactions = []
    for i in range(transaction.shape[0]):
        if (transaction['Particulars'][i] == transaction['Particulars'][i] and 'RTGS' in df['Particulars'][i]):
            credit = transaction['Credit'][i]
            debit = transaction['Debit'][i]
            if (credit == credit):
                count += (credit <= 200000)
                infoDict = transaction.iloc[[i]].to_dict('records')[0]
                infoDict['type'] = 'credit'
                transactions.append(infoDict)
            else:
                count += (debit <= 200000)
                infoDict = transaction.iloc[[i]].to_dict('records')[0]
                infoDict['type'] = 'debit'
                transactions.append(infoDict)
# count = 0
# transactions=[]
# for i in range(df.shape[0]):
#     if (df['Particulars'][i] == df['Particulars'][i] and 'RTGS' in df['Particulars'][i]):
#         credit = df['Credit'][i]
#         debit = df['Debit'][i]
#         if (credit == credit):
#             count += (credit <= 200000)
#             infoDict=df.iloc[[i]].to_dict('records')[0]
#             infoDict['type']='credit'
#             transactions.append(infoDict)
#         else:
#             count += (debit <= 200000)
#             infoDict=df.iloc[[i]].to_dict('records')[0]
#             infoDict['type']='debit'
#             transactions.append(infoDict)
