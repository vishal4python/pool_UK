import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
Excel_table = []
import pandas as pd
import datetime
import re
import numpy as np
from maks_lib import output_path
today = datetime.datetime.now()
path = output_path+"Consolidate_TSB_Data_Deposits_"+str(today.strftime('%Y_%m_%d'))+'.csv'
table_headers = ['Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term in Months', 'Interest_Type', 'Interest', 'AER']
Excel_table.append(table_headers)

resp =requests.get("https://www.tsb.co.uk/savings/compare-savings/").content
print(resp)
jsoup = BeautifulSoup(resp).find_all("div", attrs={"class":"col-sm-12 text_banner"})

tables = filter(lambda x:x.find('table', attrs={"class":"table_info tablesaw"}) is not None,jsoup)
# print(list(tables))
for table in list(tables):
    try:
        main_heading = table.find('h2').text
        data = [[td.text.strip() for td in tr.find_all('td')] for tr in table.find('tbody').find_all('tr')]
        for a in data:
            print(len(a))
            if len(a)>7:
                del a[1]
            Bank_Offer_Feature = 'Online' if 'online' in a[5].lower() else 'Offline'
            found = False
            for check in ["junior", "monthly saver", "young"]:
                if check in a[0].strip().lower():
                    found = True
                    break
            if not found:
                test = main_heading.replace('Compare', '').strip() + '_' + a[0].strip()
                if 'current' in test.lower():
                    Bank_Product_Type = 'Current'
                elif 'savings' in test.lower():
                    Bank_Product_Type = 'Savings'
                elif 'fixed' in test.lower():
                    Bank_Product_Type = 'Term Deposits'
                else:
                    Bank_Product_Type = 'Savings'
                Excel_table.append([Bank_Product_Type, main_heading.replace('Compare', '').strip()+'_'+a[0].strip(), a[2].strip(), Bank_Offer_Feature, 'Term in Months', 'Interest_Type',a[1].strip(), a[1].strip()])
        print(main_heading)

    except Exception as e:
        print(e)
    # break
try:
    resp = requests.get("https://www.tsb.co.uk/current-accounts/").content
    # print(resp)
    jsoup = BeautifulSoup(resp)
    div = jsoup.find("div", attrs={"class": "list_mode"}).find('div', attrs={"class": "accounts_module"})
    main_heading = div.find('h2').text.strip()
    aer = div.find('h4', attrs={"class": "noClassSet"}).text
    aer = re.findall('\d.*%', aer)[0] if len(re.findall('\d.*%', aer)) >= 1 else None
    print(aer)
    li = div.find('ul', attrs={"class": "tick-list-sml"}).find_all('li')[0].text
    interest = re.findall('\d.*%', li)[0] if len(re.findall('\d.*%', li)) >= 1 else None
    balance = re.findall('£\d?.*\d', li)[0] if len(re.findall('£\d?.*\d', li)) >= 1 else None
    print(interest)
    print(main_heading)
    b = ['Current', main_heading, balance, 'Online', np.nan, np.nan, interest+'gross', aer+'aer']
    print(b)
    Excel_table.append(b)
except Exception as e:
    print(e)

df = pd.DataFrame(Excel_table[1:], columns=table_headers)
df['Balance'] = df['Balance'].apply(lambda  x: re.sub('[^0-9.]','',re.findall('(£\d?.*\d |£\d?.*\d)',x)[0]) if len(re.findall('£\d?.*\d',x))>=1 else None)
df['Interest'] = df['Interest'].apply(lambda x: re.sub('[^0-9.%]','', re.findall('(\d.*gross|\d.*tax free)',x,re.IGNORECASE)[0]) if len(re.findall('(\d.*gross|\d.*tax free)',x,re.IGNORECASE))>=1 else np.nan)
df['AER'] = df['AER'].apply(lambda x: re.sub('[^0-9.%]','', re.findall('(\d.*/aer|\d.*aer)',x,re.IGNORECASE)[0]) if len(re.findall('(\d.*/aer|\d.*aer)',x,re.IGNORECASE))>=1 else np.nan)
df['Date'] = today.strftime('%m-%d-%Y')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'TSB'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Bank_Product_Code'] = np.nan
df['Interest_Type'] = 'Fixed'
df['Term in Months'] = df['Bank_Product_Name'].apply(lambda  x: int(re.sub('[^0-9]','', re.findall('\d.*Y',x)[0]))*12 if len(re.findall('\d.*Y',x))>=1 else None)
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER", "Bank_Product_Code"]
df = df[order]
df.to_csv(path, index=False)
print(tabulate(Excel_table))
