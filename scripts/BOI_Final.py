
import pandas as pd
import numpy as np
import datetime
import warnings

from maks_lib import input_path
from maks_lib import output_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

df1 = pd.read_excel(input_path+"365-online-customer-rate-sheet.xlsx")
df = pd.read_excel(input_path+"Deposits-Customer-Rate-Sheet.xlsx")

df00 = df1[11:13]
df00 = df00.rename(columns={'Unnamed: 2': 'Min_Opening_Bal', 'Unnamed: 3': 'Balance', 'Unnamed: 4': 'Interest', 'Unnamed: 5': 'AER'})
df00 = df00.rename(columns={'Bank of Ireland': 'Bank_Product_Name'})
df00.drop(df00.columns[[1]], axis=1, inplace=True)

df01 = df1[16:17]
df01 = df01.rename(columns={'Bank of Ireland': 'Bank_Product_Name'})
df01.drop(df01.columns[[1, 2, 3, 4, 5]], axis=1, inplace=True)

df02 = df1[17:18]
df02 = df02.rename(columns={'Unnamed: 1': 'Term in Months', 'Unnamed: 2': 'Min_Opening_Bal', 'Unnamed: 3': 'Balance',
                            'Unnamed: 4': 'Interest', 'Unnamed: 5': 'AER'})
df02['Bank of Ireland'] = df01['Bank_Product_Name'].values
df02 = df02.rename(columns={'Bank of Ireland': 'Bank_Product_Name'})

frames1 = [df00, df02]
result1 = pd.concat(frames1)
result1["Bank_Offer_Feature"] = "Online"
for index in range(len(result1.index)):
    result1['Interest'].iloc[index] = result1['Interest'].iloc[index].replace("variable", "").replace("Fixed", "")
    result1['AER'].iloc[index] = result1['AER'].iloc[index].replace("variable", "").replace("Fixed", "")

df1 = df[7:9]
df1.drop(df1.columns[[0, 1, 6, 7]], axis=1, inplace=True)
df1 = df1.rename(columns={'Unnamed: 2': 'Min_Opening_Bal', 'Unnamed: 3': 'Balance', 'Unnamed: 4': 'Interest', 'Unnamed: 5': 'AER'})
df1["Bank_Product_Name"] = "GoalSaver"

df2 = df[33:34]
df2.drop(df2.columns[[0, 6, 7]], axis=1, inplace=True)
df2 = df2.rename(columns={'Unnamed: 1': 'Term in Months', 'Unnamed: 2': 'Min_Opening_Bal', 'Unnamed: 3': 'Balance',
                          'Unnamed: 4': 'Interest', 'Unnamed: 5': 'AER'})
df2["AER"] = (df2["AER"] * 100).astype(str) + '%'
df2["Interest"] = (df2["Interest"] * 100).astype(str) + '%'
df2["Bank_Product_Name"] = "Term Deposits - Fixed Rates"

df3 = df[35:36]
df3.drop(df3.columns[[0, 6, 7]], axis=1, inplace=True)
df3 = df3.rename(columns={'Unnamed: 1': 'Term in Months', 'Unnamed: 2': 'Min_Opening_Bal', 'Unnamed: 3': 'Balance',
                          'Unnamed: 4': 'Interest', 'Unnamed: 5': 'AER'})
df3["AER"] = (df3["AER"] * 100).astype(str) + '%'
df3["Interest"] = (df3["Interest"] * 100).astype(str) + '%'
df3["Bank_Product_Name"] = "Term Deposits - Fixed Rates"

df4 = df[42:43]
df4.drop(df4.columns[[0, 6, 7]], axis=1, inplace=True)
df4 = df4.rename(columns={'Unnamed: 1': 'Term in Months', 'Unnamed: 2': 'Min_Opening_Bal', 'Unnamed: 3': 'Balance',
                          'Unnamed: 4': 'Interest', 'Unnamed: 5': 'AER'})
df4["Bank_Product_Name"] = "Term Deposits - Fixed Rates"

df5 = df[51:52]
df5.drop(df5.columns[[1, 6, 7]], axis=1, inplace=True)
df5 = df5.rename(columns={'Unnamed: 0': 'Bank_Product_Name', 'Unnamed: 2': 'Min_Opening_Bal', 'Unnamed: 3': 'Balance',
                          'Unnamed: 4': 'Interest', 'Unnamed: 5': 'AER'})

frames2 = [df1, df2, df3, df4, df5]
result2 = pd.concat(frames2)
result2["Bank_Offer_Feature"] = "Offline"

for index in range(len(result2.index)):
    result2['Interest'].iloc[index] = result2['Interest'].iloc[index].replace("Variable", "").replace("Fixed", "")
    result2['AER'].iloc[index] = result2['AER'].iloc[index].replace("Variable", "").replace("Fixed", "")
    result2['Min_Opening_Bal'].iloc[index] = result2['Min_Opening_Bal'].iloc[index].replace("¼", "").replace("¼", "")
    result2['Balance'].iloc[index] = str(result2['Balance'].iloc[index]).replace("¼", "").replace("¼", "")

frames = [result1, result2]
result = pd.concat(frames)
df_final = pd.DataFrame(
    columns=["Date", "Bank_Native_Country", 'State', "Bank_Name", 'Bank_Local_Currency', 'Bank_Type',
             'Bank_Product', 'Bank_Product_Type', 'Bank_Product_Name', 'Min_Opening_Bal', 'Balance',
             'Bank_Offer_Feature', 'Term in Months', 'Interest_Type', 'Interest', 'AER', 'Bank_Product_Code'])

df_final['AER'] = result['AER'].values
df_final['Balance'] = result['Balance'].values
df_final['Bank_Product_Name'] = result['Bank_Product_Name'].values
df_final['Min_Opening_Bal'] = result['Min_Opening_Bal'].values
df_final['Bank_Offer_Feature'] = result['Bank_Offer_Feature'].values
df_final['Interest'] = result['Interest'].values
df_final['Term in Months'] = result['Term in Months'].values
df_final['Date'] = now.strftime("%m-%d-%Y")
df_final["Bank_Native_Country"] = "UK"
df_final["State"] = "London"
df_final["Bank_Name"] = "Bank of Ireland"
df_final["Bank_Local_Currency"] = "GBP"
df_final["Bank_Type"] = "Bank"
df_final["Bank_Product"] = "Deposits"
df_final['Balance1']=df_final.apply(lambda x:'%s-%s' % (x['Min_Opening_Bal'],x['Balance']),axis=1)
df_final['Balance']=df_final['Balance1']
df_final.drop(df_final.columns[[9,17]], axis=1, inplace=True)

df_final["Interest_Type"] = "Variable"
for index in range(len(result.index)):
    df_final['Term in Months'].iloc[index] = str(df_final['Term in Months'].iloc[index]).replace("Months", "").replace("months", "").replace("Years",'')
    df_final['Term in Months'].iloc[index] = str(df_final['Term in Months'].iloc[index]).replace("nan", "")

    if "Saver" in result['Bank_Product_Name'].iloc[index]:
        df_final.ix[index, 'Bank_Product_Type'] = "Savings"

    elif "Fixed" in result['Bank_Product_Name'].iloc[index]:

        df_final.ix[index, 'Bank_Product_Type'] = "Term Deposits"

    elif "Personal" in result['Bank_Product_Name'].iloc[index]:
        df_final.ix[index, 'Bank_Product_Type'] = "Current"
    else:
        df_final.ix[index, 'Bank_Product_Type'] = "Savings"
    if "nan" in df_final['Balance'].iloc[index]:
       
        df_final['Balance'].iloc[index] = str(df_final['Balance'].iloc[index]).replace("-nan", "")
    if "3" in df_final['Term in Months'].iloc[index]:
        df_final["Term in Months"].iloc[index] = 3*12



df_final.to_csv(output_path+"Consolidate_BankofIreland_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
