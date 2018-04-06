
# coding: utf-8

# In[52]:



# coding: utf-8

# In[121]:


import glob
import os
import pandas as pd
import numpy as np
import datetime
import re
import warnings

output_path = "C:\\Users\\vishal\\PycharmProjects\\pool_UK-master\\data\\output\\"
input_path =  "C:\\Users\\vishal\\PycharmProjects\\pool_UK-master\\data\\input\\"
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

extension = 'csv'


# In[122]:


agg_files = glob.glob(output_path+'*.{}'.format(extension))
agg_mortage_files  = [file for file in agg_files if file.split("\\")[-1].startswith("Aggregator") and "Mortgage" in file.split("\\")[-1]]
agg_deposite_files = [file for file in agg_files if file.split("\\")[-1].startswith("Aggregator") and file not in agg_mortage_files]



# In[53]:


agg_mortage_files


# In[54]:



for val in agg_mortage_files:
    df = pd.read_csv(val)
    print(df.shape[1],df.columns)


# In[55]:


COLUMN_NAMES = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name',
       'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type',
       'Bank_Product_Code', 'Bank_Product_Name', 'Min_Loan_Amount',
       'Bank_Offer_Feature', 'Term (Y)', 'Interest_Type', 'Interest', 'APRC',
       'Mortgage_Loan_Amt', 'Mortgage_Down_Payment', 'Mortgage_Category',
       'Mortgage_Reason', 'Mortgage_Pymt_Mode', 'Source']
df_mortgage = pd.DataFrame(columns=COLUMN_NAMES)
df_mortgage['Fixed_Rate_Term'] = np.NAN


# In[56]:


for file in agg_mortage_files:
    df_temp =pd.read_csv(file)
    df_mortgage = pd.concat([df_mortgage, df_temp])


# In[58]:



df_mortgage['Date'] = " {}".format(now.strftime("%Y-%m-%d"))
df_ticker = pd.read_csv(input_path+"Bank_Ticker_UK.csv")
result = pd.merge(df_mortgage, df_ticker, how='left', on='Bank_Name')


# In[8]:


arranged_cols = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name','Ticker',
       'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type','Bank_Product_Code',
       'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature',
       'Term (Y)', 'Interest_Type', 'Interest', 'APRC', 'Mortgage_Loan_Amt',
       'Mortgage_Down_Payment', 'Mortgage_Category', 'Mortgage_Reason',
       'Mortgage_Pymt_Mode', 'Fixed_Rate_Term','Source']
df_mortgage = result.reindex(columns= arranged_cols)


# In[9]:


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


# In[10]:


# df_mortgage["Min_Loan_Amount"] = df_mortgage["Min_Loan_Amount"].str.replace(",","").str.replace("-","")
for idx in range(len(df_mortgage.index)):
    df_mortgage["Mortgage_Loan_Amt"].iloc[idx] = str(df_mortgage["Mortgage_Loan_Amt"].iloc[idx]).replace(",","")
df_mortgage["Mortgage_Loan_Amt"] = df_mortgage["Mortgage_Loan_Amt"].str.replace("nan", "")
# In[14]:


for idx in range(len(df_mortgage.index)):
    if df_mortgage['Term (Y)'].iloc[idx] ==  df_mortgage['Fixed_Rate_Term'].iloc[idx]:
         df_mortgage['Interest_Type'].iloc[idx] = "Fixed"
    else:
         df_mortgage['Interest_Type'].iloc[idx] = "Variable"
records_tobe_removed = []
for idx in range(len(df_mortgage.index)):
    if "Buy To Let" in str(df_mortgage['Bank_Product_Name'].iloc[idx]) or "Discount" in str(df_mortgage['Bank_Product_Name'].iloc[idx]) or "Cashback" in str(df_mortgage['Bank_Product_Name'].iloc[idx]):
        records_tobe_removed.append(idx)
df_mortgage.drop(records_tobe_removed, inplace=True)
# In[13]:


df_mortgage.to_csv(output_path+"UK\\" + "Aggregate_UK_Mortgage_Data_{}.csv".format(now.strftime("%Y_%m_%d")), index=False )

