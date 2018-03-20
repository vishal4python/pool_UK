
# coding: utf-8

# In[150]:


import glob
import os
import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import output_path
from maks_lib import input_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

extension = 'csv'


# In[151]:


all_files = glob.glob(output_path+'*.{}'.format(extension))
all_mortage_files  = [file for file in all_files if file.split("\\")[-1].startswith("Cons") and "Mortgage" in file.split("\\")[-1]]
all_deposite_files = [file for file in all_files if file.split("\\")[-1].startswith("Cons") and file not in all_mortage_files]


# In[152]:


COLUMN_NAMES = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name',
       'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type',
       'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature',
       'Term (Y)', 'Interest_Type', 'Interest', 'APRC', 'Mortgage_Loan_Amt',
       'Mortgage_Down_Payment', 'Mortgage_Category', 'Mortgage_Reason',
       'Mortgage_Pymt_Mode', 'Fixed_Rate_Term', 'Bank_Product_Code']


# In[153]:


df_mortgage = pd.DataFrame(columns=COLUMN_NAMES) 


# In[154]:


for idx, file in enumerate(all_mortage_files):
    print(file)
    print(pd.read_csv(all_mortage_files[idx]).shape[1])


# In[155]:


for file in all_mortage_files:
    df_temp =pd.read_csv(file)
    df_temp.columns = COLUMN_NAMES
    df_mortgage = pd.concat([df_mortgage, df_temp])


# In[156]:


df_mortgage['Date'] = " {}".format(now.strftime("%Y-%m-%d"))
df_ticker = pd.read_csv(input_path+"Bank_Ticker_UK.csv")
result = pd.merge(df_mortgage, df_ticker, how='left', on='Bank_Name')


# In[157]:


arranged_cols = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name','Ticker',
       'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type',
       'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature',
       'Term (Y)', 'Interest_Type', 'Interest', 'APRC', 'Mortgage_Loan_Amt',
       'Mortgage_Down_Payment', 'Mortgage_Category', 'Mortgage_Reason',
       'Mortgage_Pymt_Mode', 'Fixed_Rate_Term', 'Bank_Product_Code']
df_mortgage = result.reindex(columns= arranged_cols)


# In[158]:


for idx in range(len(df_mortgage.index)):
    try:
        t = int(df_mortgage['Term (Y)'].iloc[idx])
    except ValueError:
        t = "_"
    try:
        int_type = df_mortgage['Interest_Type'].iloc[idx][0]
    except TypeError:
        int_type = "_"
    df_mortgage['Bank_Product_Code'].iloc[idx] = "{0}{1}{2}{3}".format(t,"Y", "M",int_type )


# In[159]:


df_mortgage.to_csv(output_path+"UK\\" + "UK_Mortgage_Data_{}.csv".format(now.strftime("%m_%d_%Y")), index=False )

