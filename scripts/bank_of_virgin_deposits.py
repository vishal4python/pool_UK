#-*- coding:utf-8 -*-
'''
Created on 13-Mar-2018

@author: sairam
'''
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import pandas as pd
import datetime
today = datetime.datetime.now()
from maks_lib import output_path
path = output_path+"Consolidate_Virgin_Data_Deposit_"+today.strftime('%Y_%m_%d')+".csv"
# path = "Consolidate_Virgin_Data_Deposit_"+str(today.strftime('%Y_%m_%d'))+".csv"
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER", "Bank_Product_Code"]
table = []
removedData = ["Help to Buy", "Saving to Buy","Man", "Charity", "Double", "Young"]
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
table_headers = ["Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months",
                 "Interest_Type", "Interest", "AER"]
# table.append(table_headers)
resp = requests.get("https://uk.virginmoney.com/savings/find/results/", headers=headers)
jsoup = BeautifulSoup(resp.content, "html.parser")
fas_result = jsoup.find("div", attrs={"id": "FAS_results"})
divs = fas_result.find_all("div", attrs={"class": re.compile('toggle-content toggle-content--hidden')})
for div in divs:
    sections = div.find_all("section", attrs={"class": re.compile('section__primary ')})
    for scetion in sections:
        try:
            product_name = scetion.find("h3", attrs={"class": re.compile("beta center")}).text.strip()
            if product_name is not None:
                left_div = scetion.find("div", attrs={"class": "savings-features center cf "})
                right_div = scetion.find("div", attrs={"class": "margin-bottom-30 center center__left savings-rate"})
                if left_div is not None and right_div is not None:

                    interest_rate_type = scetion.find("p", attrs={"class": re.compile('delta')}).text
                    div_table = left_div.find("table")
                    trs = div_table.find_all("tr")
                    Bank_Offer_Feature = trs[1].find("td", attrs={"class": "right-text"}).text.strip()
                    minimum_balance = trs[3].find("td", attrs={"class": "right-text"}).text.strip()
                    interest = None
                    IARE = None

                    are = right_div.text
                    iare = re.findall('\d.*%', are)
                    if iare is not None:
                        interest = iare[-1]
                        IARE = iare[0]
                    term_in_months = re.findall('\d.*Year', product_name)
                    if len(term_in_months) != 0:
                        term_in_months = re.findall('\d', term_in_months[0])[0]
                    else:
                        term_in_months = None

                    if "\n" in product_name:
                        product_name = product_name[:product_name.index('\n')]
                    if "fixed" in re.sub('[\n,\r]','',interest_rate_type).lower():
                        interest_type = "Fixed"
                    else:
                        interest_type = "Variable"

                    product_name = re.sub('[\n,\r]', '', product_name)
                    checkData = True if len([rd for rd in removedData if rd.lower() in product_name.lower()]) != 0 else False
                    if checkData:
                        continue
                    a = ["Savings", re.sub('[\n,\r]', '', product_name), minimum_balance, Bank_Offer_Feature, term_in_months,
                         interest_type, interest, IARE]
                    table.append(a)

        except Exception as e:
            print(e)
try:
    interserCharges = requests.get("https://uk.virginmoney.com/virgin/current-account/questions-and-answers/#charges", headers=headers)
    interserCharges = BeautifulSoup(interserCharges.content,"lxml")
    charges = interserCharges.find("article", attrs={"id":"charges"})
    charges_account = charges.find("h3").text
    charges_account = charges_account.split('\n')[0]
    charges_amount = charges.find("p").text
    charges_amount = re.findall('£\d.*\d',charges_amount)
    if len(charges_amount)>=1:
        charges_amount = charges_amount[0]
    charges_rates = charges.find("table").find("tbody").find_all("tr")[0].find_all("td")
    charge_interest = charges_rates[0].text
    charge_interest = charge_interest[:charge_interest.index('%')+1]
    charge_aer = charges_rates[1].text
    charge_aer = charge_aer[:charge_aer.index('%')+1]

    charge_type = charges.find("table").text
    if "variable" in charge_type:
        charge_type = "Variable"
    else:
        charge_type = "Fixed"
    b = ["Current", charges_account, charges_amount, "Variable", None,charge_type, charge_interest, charge_aer]
    table.append(b)
except Exception as e:
    print(e)

def Change_bank_product_name(x):
    if "fixed" in str(x).lower():
        return "Term Deposits"
    elif "current" in str(x).lower():
        return "Current"
    else:
        return 'Savings'

# print(tabulate(table))
df = pd.DataFrame(table, columns=table_headers)
df["Balance"] = df["Balance"].apply(lambda x : re.sub('[^0-9-,]','',x.replace('–','-')).strip('-')+' ')
df['Bank_Offer_Feature'] = df["Bank_Offer_Feature"].apply(lambda x : x if "online" in x.lower() else "Offline")
df["Term in Months"] = df["Term in Months"].apply(lambda x: int(x)*12 if len(re.sub('[^0-9-]','',str(x))) !=0  else None)
df['Bank_Product_Type'] = df['Bank_Product_Name'].apply(Change_bank_product_name)
df.loc[:, 'Date'] = today.strftime('%m-%d-%Y')
df.loc[:, 'Bank_Native_Country'] = 'UK'
df.loc[:, 'State'] = 'London'
df.loc[:, 'Bank_Name'] = 'Virgin Money Plc'
df.loc[:, 'Bank_Local_Currency'] = 'GBP'
df.loc[:, 'Bank_Type'] = 'Bank'
df.loc[:, 'Bank_Product'] = 'Deposits'
df.loc[:, 'Bank_Product_Code'] = None
df = df[order]
df.to_csv(path,index=False)
print(df)
