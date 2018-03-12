import pandas as pd
from tabula import read_pdf
import urllib3
import requests
from bs4 import BeautifulSoup as bs
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
res = requests.get("https://www.halifax.co.uk/savings/accounts/",headers=headers)
if 'OK' in res.reason:
    soup = bs(res.content,"lxml")
tabs = []
s = soup.find('div',attrs={'class':"section tabs"})
[tabs.append(tab.text) for tab in s.find_all('a')]

table1 = soup.find('table',attrs={"class":"table sortableTable no-header-bg-image"})
a = table1.find_all('th')
print(a.text)
