
# coding: utf-8

# In[35]:



# coding: utf-8

# In[227]:


import glob
import os
import pandas as pd
import numpy as np
import datetime
import re
import warnings
#output_path = "C:\\Users\\vishal\\PycharmProjects\\pool-master\\data\\output\\US"
output_path = "C:\\Users\\vishal\\PycharmProjects\\pool_UK-master\\data\\output\\"
input_path =  "C:\\Users\\vishal\\PycharmProjects\\pool_UK-master\\data\\input\\"
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

extension = 'csv'


# In[228]:


agg_files = glob.glob(output_path+'*.{}'.format(extension))
agg_mortage_files  = [file for file in agg_files if file.split("\\")[-1].startswith("Aggregator") and "Mortgage" in file.split("\\")[-1]]
agg_deposite_files = [file for file in agg_files if file.split("\\")[-1].startswith("Aggregator") and file not in agg_mortage_files]



# In[36]:


agg_deposite_files


# In[37]:


for val in agg_deposite_files:
    df = pd.read_csv(val)
    print(df.shape[1],df.columns)


# In[38]:


# deep = pd.read_csv('C:\\Users\\vishal\\PycharmProjects\\pool_UK-master\\data\\output\\UK_Deposits_Data_2018_03_29.csv')#
# deep.shape[1]
# deep.columns


# In[39]:


COLUMN_NAMES = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name', 'Ticker',
       'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type',
       'Bank_Product_Code', 'Bank_Product_Name', 'Minm_Balance',
       'Maxm_Balance', 'Bank_Offer_Feature', 'Term in Months', 'Interest_Type',
       'Interest', 'AER', 'Source']
df_deposit = pd.DataFrame(columns=COLUMN_NAMES)
for file in agg_deposite_files:
    df_temp =pd.read_csv(file)
    df_deposit = pd.concat([df_deposit, df_temp])


# In[40]:


df_deposit.drop(columns=['Ticker'], inplace = True)
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



# In[41]:


# In[39]:


df_ticker = pd.read_csv(input_path + "Bank_Ticker_UK.csv")

# In[40]:




# In[43]:


result = pd.merge(df_deposit, df_ticker, how='left', on='Bank_Name')


# In[45]:




# In[41]:


arranged_cols = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name', 'Ticker',
                 'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type', 'Bank_Product_Code',
                 'Bank_Product_Name', 'Minm_Balance', 'Maxm_Balance', 'Bank_Offer_Feature', 'Term_in_Months',
                 'Interest_Type', 'Interest', 'AER','Source']
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

df_deposit.to_csv(output_path + "UK\\" + "Aggregate_UK_Deposits_Data_{}.csv".format(now.strftime("%Y_%m_%d")), index=False)

#hello world
