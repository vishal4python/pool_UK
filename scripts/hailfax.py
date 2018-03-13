import pandas as pd
#from tabula import read_pdf
import urllib3
import requests
# from bs4 import BeautifulSoup as bs
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
# res = requests.get("https://www.halifax.co.uk/savings/accounts/",headers=headers)
# if 'OK' in res.reason:
#     soup = bs(res.content,"html.parser")
# tabs = []
# s = soup.find('div',attrs={'class':"section tabs"})
# [tabs.append(tab.text) for tab in s.find_all('a')]
#
#
# column=['Bank_Product_Name', 'Interest Rate & AER', 'Balance',
#        'Interest_Type', 'Withdrawals', 'Interest paid', 'Unnamed: 6']
# dataset = pd.read_html(str(soup),flavor="bs4")
# df1 = dataset[0]
# df2 = dataset[1]
# df3 = dataset[2]
#
# df1.columns = column
# df2.columns = column
# df3.columns = column
#
# df = pd.concat([df1,df2,df3])
# df.drop(columns=['Withdrawals', 'Interest paid','Unnamed: 6'],inplace=True)
# print(df.head())

s="0.35%
tax free/AER variable for 12 months

After 12 months, your account automatically changes to an Instant ISA Saver. See Instant ISA Saver interest rates (PDF).."
import re
f = re.findall(r'([0]\.[0-9]%)\s(\d[months|years])',s)
print(f)




