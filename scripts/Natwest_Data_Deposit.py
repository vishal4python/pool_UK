#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tabulate import tabulate
import numpy as np
import datetime
from maks_lib import output_path

today = datetime.datetime.now()
path = output_path+"Consolidate_Natwest_Data_Deposits_"+str(today.strftime('%Y_%m_%d'))+'.csv'
# path = "Consolidate_Natwest_Data_Deposits_"+str(today.strftime('%Y_%m_%d'))+'.csv'

table = []
table_columns = ["Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER"]
# table.append(table_columns)
#Pass the site url here.
resp = requests.get("https://personal.natwest.com/personal/savings/compare-savings-accounts-new.html#ISAdesktop")
jsoup = BeautifulSoup(resp.content,"lxml")

#Find All Tabs Data.
tabs = [["instantaccessdesktop",True],["ISAdesktop", False], ["FTSA desktop", False]]
for tabLi in tabs:

    tab = jsoup.find("section", attrs={"id":tabLi[0]})
    table_head_Bank_Offer_Feature = [table_head.text for table_head in tab.find_all("div", attrs={"role": "columnheader"})]
    print(len(table_head_Bank_Offer_Feature))

    table_headers = [table_head.find("h4").text.strip() for table_head in tab.find_all("div", attrs={"role":"columnheader"})]
    tds = [ row.find_all("div", attrs={"role":"cell"}) for row in [rows  for rows in tab.find_all("div", attrs={"class":re.compile("comparison-content-table comparison-is-accordian")})  ]]
    minimumBalance = [re.sub('[^0-9.]', '', t.text) for t in tds[3]]
    
    for i in range(3):
        dummy = dict()
        index_value = 0
        for year in [col for col in tds[2][i].text.strip().split('\n') if len(col)>1]:
            if len(re.findall('\d\syear', year))>=1:
                index_value = re.sub('[^0-9]', '', re.findall('\d\syear', year)[0])
                dummy[index_value] = year
                 
            else:
                if len(dummy) == 0:
                    dummy[0] = ''
                dummy[index_value] = dummy[index_value]+'\n'+year
         
        for keys in dummy.keys():
             
            for col_1 in dummy[keys].split('\n'):
                interest_type = "Fixed" if "fixed" in col_1.lower() else "Variable"
                interest_type = "Fixed" if "fixed" in table_headers[i].lower() else interest_type
                col_1 = re.sub('\(.*\)', '',col_1)
                AER = re.findall('\d.*%', col_1)
                AER = re.findall('(\d.*% AER|\d.*%)', col_1)[0] if len(re.findall('(\d.*% AER|\d.*%)', col_1))>=1 else None
                interest = re.findall('(\d\d?\.?\d?\d?\d?.? gross)', col_1)[0] if len(re.findall('(\d.*% gross)', col_1))>=1 else None
                
                Amount = re.findall('(above £.*\d|£.*\d|\d\d?m)', col_1)
                Amount = Amount[0] if len(Amount)>=1 else None

                #a = ["Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER"]
                Terms_in_month = int(keys)*12 if keys!=0 else None
                if Terms_in_month == None:
                    Terms_in_month = re.findall('\d.*Y',table_headers[i])
                    Terms_in_month = int(re.sub('[^0-9]', '', Terms_in_month[0]))*12  if len(Terms_in_month)!=0 else None
                try:
                    mil_Amount = re.findall('\dm',Amount)
                    if len(mil_Amount)>=1:
                        Amount = str(int(re.sub('[^0-9]','',mil_Amount[0]))*10000000)
                except:
                    pass
                if AER is not None:
                    if tabLi[1]:
                        interest = interest if interest is not None else AER
                    print(table_head_Bank_Offer_Feature[i])
                    Bank_Offer_Feature = table_head_Bank_Offer_Feature[i] if len(table_head_Bank_Offer_Feature)>=3 else 'Offline'
                    Bank_Offer_Feature = 'Online' if 'online' in Bank_Offer_Feature.lower() else "Offline"



                    print(Bank_Offer_Feature)
                    a = ["Bank_Product_Type", table_headers[i], re.sub('[^0-9a-zA-Z, ]','',Amount).replace('and','-'), Bank_Offer_Feature, Terms_in_month,
                         interest_type, re.sub('[^0-9.%]', '',interest) if interest is not None else None, 
                         re.sub('[^0-9.%]', '',AER) if AER is not None else None ]
                    if 'help' not in table_headers[i].lower():
                        table.append(a)
                

def checkBankProductType(x):
    if "fixed" in str(x).lower():
        return 'Term Deposits'
    else:
        return 'Savings'

# print(tabulate(table))
# print(table_headers)
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER", "Bank_Product_Code"]
df = pd.DataFrame(table, columns=table_columns)
df['Date'] = today.strftime('%m-%d-%Y')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'NatWest'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Bank_Product_Type'] = df['Interest_Type'].apply(checkBankProductType)
df['Bank_Product_Code'] =   np.nan
order = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name', 'Bank_Local_Currency', 'Bank_Type', 'Bank_Product', 'Bank_Product_Type', 'Bank_Product_Name',
         'Balance', 'Bank_Offer_Feature', 'Term in Months', 'Interest_Type', 'Interest', 'AER', 'Bank_Product_Code']
df = df[order]
df.to_csv(path,index=False)
print(df)
