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
today = datetime.datetime.now().strftime('%m-%d-%Y')
from maks_lib import output_path
path = output_path+"Consolidate_Virgin_Data_Deposit_"+today+".csv"
# path = "Consolidate_Virgin_Data_Deposit_"+today+".csv"
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER", "Bank_Product_Code"]
table = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
table_headers = ["Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months",
                 "Interest_Type", "Interest", "AER"]
# table.append(table_headers)
resp = requests.get("https://uk.virginmoney.com/savings/find/results/", headers=headers)
# print(resp.content)
jsoup = BeautifulSoup(resp.content, "html.parser")
fas_result = jsoup.find("div", attrs={"id": "FAS_results"})
divs = fas_result.find_all("div", attrs={"class": re.compile('toggle-content toggle-content--hidden')})
# print(len(divs))
for div in divs:
    #     print("-".center(100,'-'))
    sections = div.find_all("section", attrs={"class": re.compile('section__primary ')})
    for scetion in sections:
        #     print(div)
        try:
            #             print("-".center(100,'='))
            product_name = scetion.find("h3", attrs={"class": re.compile("beta center")}).text.strip()
            #             print(product_name)
            if product_name is not None:
                left_div = scetion.find("div", attrs={"class": "savings-features center cf "})
                right_div = scetion.find("div", attrs={"class": "margin-bottom-30 center center__left savings-rate"})
                if left_div is not None and right_div is not None:

                    interest_rate_type = scetion.find("p", attrs={"class": re.compile('delta')}).text
                    #                 print(interest_rate_type.text)
                    div_table = left_div.find("table")
                    trs = div_table.find_all("tr")
                    Bank_Offer_Feature = trs[1].find("td", attrs={"class": "right-text"}).text.strip()
                    minimum_balance = trs[3].find("td", attrs={"class": "right-text"}).text.strip()
                    #                     print(Bank_Offer_Feature)
                    #                     print(minimum_balance)
                    interest = None
                    IARE = None

                    #                     if right_div is not None:
                    are = right_div.text
                    print(are)
                    iare = re.findall('\d.*%', are)
                    if iare is not None:
                        interest = iare[-1]
                        IARE = iare[0]
                    # print(are)
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
                    a = ["Savings", re.sub('[\n,\r]', '', product_name), minimum_balance.replace("Â£1 â€“ Â",''), Bank_Offer_Feature, term_in_months,
                         interest_type, interest, IARE]
                    #                     print(a)
                    table.append(a)

        except Exception as e:
            print(e)

print(tabulate(table))
df = pd.DataFrame(table, columns=table_headers)
df.loc[:, 'Date'] = today
df.loc[:, 'Bank_Native_Country'] = 'UK'
df.loc[:, 'State'] = 'London'
df.loc[:, 'Bank_Name'] = 'Virgin Money Plc'
df.loc[:, 'Bank_Local_Currency'] = 'GBP'
df.loc[:, 'Bank_Type'] = 'Bank'
df.loc[:, 'Bank_Product'] = 'Deposits'
df.loc[:, 'Bank_Product_Code'] = None
print(df)
df = df[order]
df.to_csv(path,index=False)