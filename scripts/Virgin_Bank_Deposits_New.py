import requests
from bs4 import BeautifulSoup
from tabulate import  tabulate
import re
import pandas as pd
import numpy as np
Excel_Table = []
import datetime
today = datetime.datetime.now()
from maks_lib import output_path

path = output_path+"Consolidate_Virgin_Data_Deposits_"+str(today.strftime('%Y_%m_%d'))+'.csv'
table_headers = ['Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term in Months', 'Interest_Type', 'Interest', 'AER']
# Excel_Table.append(table_headers)
resp = requests.get("https://uk.virginmoney.com/savings/find/results/").content
jsoup = BeautifulSoup(resp)
lists = jsoup.find('div', attrs={'id':"FAS_results"}).find_all('section', attrs={'role':"tabpanel"})
tbodys = [li.find('table').find('tbody') for li in lists]
tr_list = [tbody.find_all('tr') for tbody in tbodys]
account_typ = ['Online','Offline']
for id, trs in enumerate(tr_list):
    for tr in trs:
        data = [re.sub(' +',' ',re.sub('\s',' ',td.text.replace('\n','').replace('\n\r',''))).strip() for td in tr.find_all('td')]
        data.append(account_typ[id])
        # ['Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term in Months', 'Interest_Type','Interest', 'AER']
        b = [data[0], data[0], data[2], data[-1], data[0], data[1], data[1], data[1]]
        checks = ["young", '5 year', 'man', 'charity', 'help', 'double', 'easy access cash isa', 'easy access saver']
        check_found = False
        for check in checks:
            if check in data[0].lower():
                check_found = True
                break
        if not check_found:
            Excel_Table.append(b)

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
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
        # ['Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term in Months', 'Interest_Type','Interest', 'AER']
    b = ["Current", charges_account, charges_amount, "Variable", '',charge_type, charge_interest+'gross', charge_aer+'aer']
    # print(b)
    Excel_Table.append(b)
except Exception as e:
    print(e)


def product_type(x):
    if 'fixed' in x.lower():
        return 'Term Deposits'
    elif 'current' in x.lower():
        return 'Current'
    else:
        return 'Savings'

df = pd.DataFrame(Excel_Table, columns=table_headers)
# print(df['Balance'])
df['Balance'] = df['Balance'].apply(lambda x: re.findall('(£\d?.*\d |£\d?.*\d)', x)[0] if len(re.findall('£\d?.*\d', x))>=1 else np.nan)
df['Balance'] = df['Balance'].apply(lambda x:re.sub(' +','-',re.sub('[^0-9,]', ' ',x)).replace('-,-','-').strip('-'))
df['Interest'] = df['Interest'].apply(lambda x: re.sub('[^0-9.%]','',re.findall('(\d.*%.*gross|\d.*%.*tax)',x,re.IGNORECASE)[0]) if len(re.findall('(\d.*%.*gross|\d.*%.*tax)',x,re.IGNORECASE))>=1 else np.nan)
df['AER'] = df['AER'].apply(lambda x: re.sub('[^0-9.%]','',re.findall('(\d.*%.*AER)',x,re.IGNORECASE)[0]) if len(re.findall('(\d.*%.*AER)',x,re.IGNORECASE))>=1 else np.nan)
df['Interest_Type'] = df['Interest_Type'].apply(lambda x: "Fixed" if 'fixed' in x.lower() else 'Variable')
df['Term in Months'] = df['Term in Months'].apply(lambda x: int(re.sub('[^0-9]','',re.findall('\d.*year',x,re.IGNORECASE)[0]))*12 if len(re.findall('\d.*year',x,re.IGNORECASE))>=1 else np.nan)
df['Interest'] = df['Interest'].apply(lambda x: re.sub('%\d.*','%',str(x)))
df['Bank_Product_Type'] = df['Bank_Product_Type'].apply(product_type)
df['Date'] = today.strftime('%m-%d-%Y')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'Virgin Money Plc.'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Bank_Product_Code'] = np.nan
df['Interest_Type'] = 'Fixed'

order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER", "Bank_Product_Code"]
df = df[order]

df.to_csv(path, index=False)
print('Execution Completed...')
