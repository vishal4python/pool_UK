
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from tabulate import tabulate
import numpy as np
import time
import re
from datetime import datetime
today = datetime.now()
from maks_lib import output_path
path = output_path+"Consolidate_HSBC_Data_Mortgage"+today.strftime('%m_%d_%Y')+".csv"
table = []
table_headers = ['Bank_Product_Name', 'Mortgage_Down_Payment', 'Interest', 'APRC', 'Fixed_Rate_Term(Y)', 'Interest_Type']
table.append(table_headers)
browser = webdriver.Firefox()#replace with .Chrome(), or with the browser of your choice
url = "https://www.hsbc.co.uk/1/2/mortgages/mortgage-rates/first-time-buyer"
browser.get(url) #navigate to the page
time.sleep(3)
jsoup = BeautifulSoup(browser.page_source)
jsoup = jsoup.find("ul", attrs={"id":"ourMortgagesList"})

divs = jsoup.find_all("div", attrs={"class":"contentStyle17a"})
results = []
for div in divs:
    heading = div.find("h3").text
    urls = [[heading, li.text, li.a["href"]] for li in div.find('ul').find_all('li') if "hsbc" not in li.text.lower()] if '80%' in heading else False
    print(urls)
    if urls:
        results.append(urls)

final_tds = []
for url in results:
    for u in url:
        browser.get(u[2])
        time.sleep(2)
        jsoup = BeautifulSoup(browser.page_source)
        trs = jsoup.find("table", attrs={"id":"mortgageProductInDetail"}).find('tbody').find_all('tr')
        tds = [td.text  for tr in trs[:1] for td in tr.find_all('td')]
        tds.append(u[0]) #7 Bank_Product_Name
        tds.append(u[1]) #8
        final_tds.append(tds)

for t in final_tds:
    table.append([t[8], t[0], t[1], t[4], t[3], ''])
browser.close()

print(tabulate(table))

df = pd.DataFrame(table[1:], columns=table_headers)
df['Date'] = today.strftime('%m-%d-%Y')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'HSBC'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = 'Offline'
df['Mortgage_Category'] = 'New Purchase'
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Min_Loan_Amount'] = np.nan
df['Term (Y)'] = np.nan
df['Mortgage_Loan_Amt'] = np.nan
df['Bank_Product_Code'] = np.nan
df['APRC'] = df['APRC'].apply(lambda x : re.sub('[^0-9.%]','',x)+'%')
df['Fixed_Rate_Term(Y)'] = df['Fixed_Rate_Term(Y)'].apply(lambda x: re.sub('[^0-9]','',re.findall('\d.*Yea',x)[0]) if len(re.findall('\d.*Yea',x))>=1 else None)
# df['Interest_Type'] = df['Bank_Product_Name'].apply(lambda x: "Fixed" if 'fixed' in x.lower() else 'Variable')
df['Interest_Type'] = 'Variable'
df['Mortgage_Down_Payment'] = '20%'
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term(Y)", "Bank_Product_Code"]
df = df[order]
df.to_csv(path,index=False)
print(tabulate(table))
print('Execution Completed...')