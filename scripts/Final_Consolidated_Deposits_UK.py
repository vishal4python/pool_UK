# coding: utf-8

# In[33]:


import glob
import os
import pandas as pd
import numpy as np
import datetime
import re
import warnings
from maks_lib import output_path
from maks_lib import input_path

warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

extension = 'csv'

all_files = glob.glob(output_path + '*.{}'.format(extension))
all_mortage_files = [file for file in all_files if
                     file.split("\\")[-1].startswith("Cons") and "Mortgage" in file.split("\\")[-1]]
all_deposite_files = [file for file in all_files if
                      file.split("\\")[-1].startswith("Cons") and file not in all_mortage_files]

deposite_cols = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name',
                 'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type',
                 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature',
                 'Term_in_Months', 'Interest_Type', 'Interest', 'AER', 'Bank_Product_Code']
df_deposit = pd.DataFrame(columns=deposite_cols)

for idx, file in enumerate(all_deposite_files):
    print(file)
    print(pd.read_csv(all_deposite_files[idx]).shape[1])

# In[34]:


for file in all_deposite_files:
    df_temp = pd.read_csv(file)
    df_temp.columns = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name',
                       'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type',
                       'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature',
                       'Term_in_Months', 'Interest_Type', 'Interest', 'AER', 'Bank_Product_Code']
    df_deposit = pd.concat([df_deposit, df_temp])

# In[35]:


df_deposit['Date'] = " {}".format(now.strftime("%Y-%m-%d"))
df_deposit['Minm_Balance'] = np.NAN
df_deposit['Maxm_Balance'] = np.NAN

# In[37]:


for idx in range(len(df_deposit.index)):
    if "Below" in str(df_deposit['Balance'].iloc[idx]) or "or less" in str(
            df_deposit['Balance'].iloc[idx]) or "Less than" in str(
            df_deposit['Balance'].iloc[idx]) or "less than" in str(df_deposit['Balance'].iloc[idx]) or "Up to" in str(
            df_deposit['Balance'].iloc[idx]):
        df_deposit['Maxm_Balance'].iloc[idx] = df_deposit['Balance'].iloc[idx]
    elif "-" in str(df_deposit['Balance'].iloc[idx]):
        df_deposit['Minm_Balance'].iloc[idx], df_deposit['Maxm_Balance'].iloc[idx] = str(
            df_deposit['Balance'].iloc[idx]).split("-")
    elif " to " in str(df_deposit['Balance'].iloc[idx]):
        df_deposit['Minm_Balance'].iloc[idx], df_deposit['Maxm_Balance'].iloc[idx] = str(
            df_deposit['Balance'].iloc[idx]).split("to")
    else:
        df_deposit['Minm_Balance'].iloc[idx] = df_deposit['Balance'].iloc[idx]

df_deposit.drop(columns=['Balance'], inplace=True)

for idx in range(len(df_deposit.index)):
    text1 = str(df_deposit['Maxm_Balance'].iloc[idx])
    result = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", text1)
    try:
        df_deposit['Maxm_Balance'].iloc[idx] = result[0]
    except IndexError:
        df_deposit['Maxm_Balance'].iloc[idx] = np.NAN

    text2 = str(df_deposit['Minm_Balance'].iloc[idx])
    result = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", text2)
    try:
        df_deposit['Minm_Balance'].iloc[idx] = result[0]
    except IndexError:
        df_deposit['Minm_Balance'].iloc[idx] = np.NAN

# In[39]:


df_ticker = pd.read_csv(input_path + "Bank_Ticker_UK.csv")

# In[40]:


result = pd.merge(df_deposit, df_ticker, how='left', on='Bank_Name')

# In[41]:


arranged_cols = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name', 'Ticker',
                 'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type', 'Bank_Product_Code',
                 'Bank_Product_Name', 'Minm_Balance', 'Maxm_Balance', 'Bank_Offer_Feature', 'Term_in_Months',
                 'Interest_Type', 'Interest', 'AER']
df_deposit = result.reindex(columns=arranged_cols)
df_deposit["Interest_Type"] = "Fixed"

# In[42]:


for idx in range(len(df_deposit.index)):
    if "Savings" in str(df_deposit['Bank_Product_Type'].iloc[idx]):
        s = "SB"
    elif "Current" in str(df_deposit['Bank_Product_Type'].iloc[idx]):
        s = "CC"
    else:
        s = "CD"
    try:
        t = int(df_deposit['Term_in_Months'].iloc[idx])
    except ValueError:
        t = "_"
    df_deposit['Bank_Product_Code'].iloc[idx] = "{0}{1}{2}{3}".format(t, "M", s,
                                                                      df_deposit['Interest_Type'].iloc[idx][0])

# In[44]:

for idx in range(len(df_deposit.index)):
    df_deposit["Minm_Balance"].iloc[idx] = str(df_deposit["Minm_Balance"].iloc[idx]).replace(",", "")
    df_deposit["Maxm_Balance"].iloc[idx] = str(df_deposit["Maxm_Balance"].iloc[idx]).replace(",", "")
    df_deposit["Maxm_Balance"] = df_deposit["Maxm_Balance"].str.replace("nan", "")


# In[46]:
df_deposit = df_deposit[((df_deposit.Bank_Product_Type == "Term Deposits") & (df_deposit.Term_in_Months.isin([6.0,12.0,24.0,36.0,0.0]))) |(df_deposit.Bank_Product_Type != "Term Deposits") ]

df_deposit.to_csv(output_path + "UK\\" + "UK_Deposits_Data_{}.csv".format(now.strftime("%Y_%m_%d")), index=False)

