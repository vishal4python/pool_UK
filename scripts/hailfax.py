import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import datetime
from maks_lib import output_path

now = datetime.datetime.now()
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
res = requests.get("https://www.halifax.co.uk/savings/accounts/",headers=headers)
if 'OK' in res.reason:
    soup = bs(res.content,"html.parser")
tabs = []
s = soup.find('div',attrs={'class':"section tabs"})
[tabs.append(tab.text) for tab in s.find_all('a')]


column=['Bank_Product_Name', 'Interest Rate & AER', 'Balance',
       'Interest_Type', 'Withdrawals', 'Interest paid', 'Unnamed: 6']
dataset = pd.read_html(str(soup),flavor="bs4")
df1 = dataset[0]
df2 = dataset[1]
df3 = dataset[2]

#Assign columns name
df1.columns = column
df2.columns = column
df3.columns = column

#concate all dataframes
df = pd.concat([df1,df2,df3])

df.drop(df.columns[[4,5,6]], axis=1, inplace=True)
#df.drop(columns=['Withdrawals', 'Interest paid','Unnamed: 6'], inplace=True)

#Regx
s = df['Interest Rate & AER']
df['Interest'] = s.str.extract('(\d[.][0-9]{2,}%)',expand=True)
df['AER'] = df['Interest']
df['Term in Months'] = s.str.extract('(\d\d? year|\d\d? )',expand=True).replace("1 year","12").replace("2 year","24").replace("5 year","60")
df.drop(df.columns[[1]], axis=1, inplace=True)
df['Balance'] = df['Balance'].str.extract('(£[0-9]+,[0-9]+|£[0-9]+\sto\s£[0-9]+|£[0-9]+)',expand=True)

df['Date'] = now.strftime("%m-%d-%Y")
df['Bank_Native_Country'] = 'UK'
df['State'] = "London"
df['Bank_Name'] = "Halifax"
df['Bank_Local_Currency'] = "GBP"
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Deposits"
df["Bank_Product_Type"] = np.NAN
df["Bank_Offer_Feature"] = "Offline"
df["Bank_Product_Code"] = np.NAN

columns = ['Date','Bank_Native_Country','State','Bank_Name','Bank_Local_Currency','Bank_Type','Bank_Product',
           'Bank_Product_Type','Bank_Product_Name','Balance','Bank_Offer_Feature','Term in Months','Interest_Type',
           'Interest','AER','Bank_Product_Code'
           ]


dff = df.reindex(columns=columns) #Re-Indexing
dff.iloc[0:2,7] = "Savings"
dff.iloc[2:5,7] = "Fixed Term"
dff.iloc[5:9,7] = "Savings"
dff["Bank_Product_Type"] = dff.iloc[:,7].str.replace("Fixed Term","Term Deposits")
dff["Balance"] = dff.iloc[:,9].str.replace("£","")
dff=dff[:7]
# Writing to CSV
#dff.to_csv(output_path + "Halifax_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
dff.to_csv(output_path + "Consolidate_Halifax_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
