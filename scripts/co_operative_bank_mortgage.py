'''
Created on 14-Mar-2018

@author: sairam
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from tabulate import  tabulate
from datetime import datetime
today = datetime.now()
from maks_lib import output_path

path = output_path+"Consolidate_ CoOp_Data_Mortgage"+today.strftime('%Y_%m_%d')+".csv"
# path = "Consolidate_coOp_Data_Mortgage"+today.strftime('%m_%d_%Y')+".csv"
table = []
table_headers = ["Bank_Product_Name", "Min_Loan_Amount", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Fixed_Rate_Term","Mortgage_Down_Payment"]
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product",
         "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type",
         "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term",
         "Bank_Product_Code"]

table.append(table_headers)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
resp = requests.get("https://www.co-operativebank.co.uk/mortgages/existing-customers-moving-rates", headers=headers)

jsoup = BeautifulSoup(resp.content, "html.parser")
divs = jsoup.find_all("div", attrs={"class": re.compile("c-rate-card js-rate-card js-rate-card-ret"), "identifier":re.compile("\d?yrfixopt")})
# print(len(divs))
for div in divs:
#     print("-".center(100, '-'))
    try:
        #         print(div)
        Bank_Product_Name = div.find("mark", attrs={"method-type":"MortgagesText"}).text
        # print(Bank_Product_Name)
        Interest = div.find("mark", attrs={"data-crc-property": "Initial Rate Ret"}).text
        # print(Interest)

        Interest_Type = div.find("a", attrs={"href": "#popup-initial-rate"}).text
        # print(Interest_Type)

        APRC = div.find("mark", attrs={"data-crc-property": "Initial APR Ret"}).text
        # print(APRC)

        Mortgage_Down_Payment = div.find("mark", attrs={"data-crc-property": "Max Loan to Value"}).text
        # print(Mortgage_Down_Payment)

        Min_Loan_Amount = div.find("mark", attrs={"data-crc-property": "Minimum Loan Amount Ret"}).text
        # print(Min_Loan_Amount)
        term = re.findall("\d.*Year", Bank_Product_Name)
        if len(term)>=1:
            term = re.sub('[^0-9]','',term[0])
        else:
            term = None
        a = [Bank_Product_Name, Min_Loan_Amount, None, Interest_Type, Interest, APRC, None,term, 100-float(re.sub('[^0-9.]','',Mortgage_Down_Payment))]
        table.append(a)
    except Exception as e:
        print(e)
        #     break
lifes = jsoup.find_all("div", attrs={"class": re.compile("c-rate-card js-rate-card js-rate-card-ret"), "identifier":re.compile("lifetrkopt")})
for life in lifes:
    try:
        Bank_Product_Name = life.find("mark", attrs={"method-type":"MortgagesText"}).text
#         print(Bank_Product_Name)

        Interest = life.find("mark", attrs={"data-crc-property":"Initial Rate Ret"}).text
#         print(Interest)

        if "variable" in Interest:
            Interest_Type = "Variable"
        else:
            Interest_Type = "Fixed"

            APRC = life.find("mark", attrs={"data-crc-property":"Initial APR Ret"}).text

        Mortgage_Down_Payment = life.find("mark", attrs={"data-crc-property":"Max Loan to Value"}).text

        Min_Loan_Amount = life.find("mark", attrs={"data-crc-property":"Minimum Loan Amount Ret"}).text

        term = re.findall("\d.*Year", Bank_Product_Name)
        if len(term) >= 1:
            term = re.sub('[^0-9]', '', term[0])
        else:
            term = None
        a = [Bank_Product_Name, Min_Loan_Amount, None, Interest_Type, Interest, APRC, None,
             term, Mortgage_Down_Payment]
        table.append(a)
    except:
        pass
print(tabulate(table))
df = pd.DataFrame(table[1:], columns=table_headers)
df['Date'] = today.strftime('%m-%d-%Y')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'The Co-operative Bank'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = "Offline"
df['Mortgage_Category'] = 'Existing Customers '
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Bank_Product_Code'] = None
df = df[order]
df.to_csv(path,index=False)
