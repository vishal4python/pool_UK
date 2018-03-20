# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
import pandas as pd
import datetime
# import numpy as np
from maks_lib import output_path

to_day = datetime.datetime.now()
locationPath = output_path+'Consolidate_RBS_Data_Deposits_'+str(to_day.strftime("%Y_%m_%d"))+'.csv'
# locationPath = 'Consolidate_RBS_Data_Deposits_'+str(to_day.strftime("%Y_%m_%d"))+'.csv'
table = []
table_headers = ["Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER"]
# table.append(table_headers)

headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

resp = requests.get("https://personal.rbs.co.uk/personal/savings/compare-savings-accounts.html", headers=headers)
jsoup = BeautifulSoup(resp.content, "lxml")
table_data = jsoup.find("div", attrs={"class":"comparison-table-wrapper"})
headers = table_data.find("div", attrs={"class":"comparison-header-main-table"})
columnheaders = headers.find_all("div", attrs={"role":"columnheader"})
product_names_dict = dict()
product_names = [columnheader.find('h4').text for columnheader in columnheaders]
print(product_names)
main_table = table_data.find("div", attrs={"class":"comparison-content-main-table"})
content_tables = main_table.find_all("div", attrs={"class":re.compile('comparison-content-table comparison-is-accordian')})
royalBankData = []
for id , content_table in enumerate(content_tables):
    if id in [2,3]:
        content_block = content_table.find("div", attrs={"class":"comparison-is-accordian-block"})
        contentCells = content_block.find_all("div", attrs={"class":"comparison-content-cell"})
        royalBankData.append(contentCells)
dummyDict = dict()


#INSTANT SAVER
# print("INSTANT SAVER".center(100,'-'))
cells = royalBankData[0]
lis = cells[0].find("ul").find_all('li')
variable_type = cells[0].text
variable_type = re.findall('\(.*\)', variable_type)
variable = None
if len(variable_type)!=0:
    for va in variable_type:
        if 'variable' in va.lower():
            variable = 'Variable'
            break
        elif 'fixed' in va.lower():
            variable = 'Fixed'
            break

for li in lis:
    inter = text = re.findall(r'\d?\.?\d*%',li.text)
    text = re.findall(r'(above\s?\n?£.*\d|£.*\d)',li.text)
    is_aer = re.findall(r'\d.*AER', li.text)
    if len(text)!=0 and len(inter)!=0:
        if len(is_aer) >= 1:
            is_aer = re.sub('[^a-z0-9.%-,]', '', is_aer[-1])
        else:
            is_aer = None
        table.append(['Savings', product_names[0], text[0], 'Offline', None, variable, inter[-1], is_aer])

#INSTANT ACCESS ISA
# print("INSTANT ACCESS ISA".center(100,'-'))
lis = cells[1].find("ul").find_all('li')
lis_variable_type = cells[1].text
lis_variable_type = re.findall('\(.*\)', lis_variable_type)
lis_variable = None
if len(lis_variable_type)!=0:
    for va in lis_variable_type:
        if 'variable' in va.lower():
            lis_variable = 'Variable'
            break
        elif 'fixed' in va.lower():
            lis_variable = 'Fixed'
            break

for li in lis:
    inter = text = re.findall(r'\d?\.?\d*%',li.text)
    text = re.findall(r'(above\s?\n?£.*\d|£.*\d)',li.text)
    iaisa_aer = re.findall(r'\d.*AER', li.text)
    if len(text)!=0 and len(inter)!=0:
        if len(iaisa_aer) >= 1:
            iaisa_aer = re.sub('[^0-9.%]', '', iaisa_aer[-1])
        else:
            iaisa_aer = None
        table.append(['Savings', product_names[1], text[0], 'Offline', None, lis_variable, inter[-1], iaisa_aer])

# FIXED RATE ISA
# print("FIXED RATE ISA".center(100,'-'))
lis = cells[2]

frias_variable_type = cells[2].text
frias_variable_type = re.findall('\(.*\)', frias_variable_type)
frias_variable = None
if len(frias_variable_type)!=0:
    for va in frias_variable_type:
        if 'variable' in va.lower():
            frias_variable = 'Variable'
            break
        elif 'fixed' in va.lower():
            frias_variable = 'Fixed'
            break

lis = re.sub('[\n]',' ',str(lis))
years = re.findall(r'<p>.*?</ul>',str(lis))
for year in years:
    lsoup = BeautifulSoup(year,'lxml')
    frisa_heading = lsoup.find('strong').text
    sub_frisa_heading = frisa_heading
    frisa_heading = re.findall('\d', frisa_heading)
    if len(frisa_heading)!=0:
        frisa_heading = int(frisa_heading[0])*12
    lis = lsoup.find("ul").find_all('li')
    for li in lis:
        inter = text = re.findall(r'\d?\.?\d*%', li.text)
        text = re.findall(r'(above\s?\n?£.*\d|£.*\d)', li.text)
        frisa_aer = re.findall(r'\d.*AER', li.text)
        if len(text) != 0 and len(inter) != 0:
            if len(frisa_aer)>=1:
                _frisa_aer = re.sub('[^0-9.%-a-z]','',frisa_aer[-1].replace('and','-').lower())
            else:
                _frisa_aer = None
            table.append(['Savings', product_names[2]+' '+sub_frisa_heading, text[0], 'Offline', frisa_heading, frias_variable, inter[-1], _frisa_aer])

# FIXED TERM SAVINGS
# print("FIXED TERM SAVINGS".center(100,'-'))
fts = cells[3]
fts_variable_type = cells[2].text
fts_variable_type = re.findall('\(.*\)', fts_variable_type)
frias_variable = None
if len(fts_variable_type)!=0:
    for va in fts_variable_type:
        if 'variable' in va.lower():
            fts_variable = 'Variable'
            break
        elif 'fixed' in va.lower():
            fts_variable = 'Fixed'
            break

fts = re.sub('[\n]',' ',str(fts))
years = re.findall(r'<p>.*?</ul>',str(fts))
for year in years:
    lsoup = BeautifulSoup(year,'lxml')
    year_heading = lsoup.find('strong').text
    sub_year_heading = year_heading
    year_heading = re.findall('\d',year_heading)
    if len(year_heading)!=0:
        year_heading = int(year_heading[0])*12
    lis = lsoup.find("ul").find_all('li')
    for li in lis:
        inter = text = re.findall(r'\d?\.?\d*%', li.text)
        text = re.findall(r'(above\s?\n?£.*\d|£.*\d)', li.text)
        aer = re.findall(r'\d.*AER',li.text)
        if len(text) != 0 and len(inter) != 0:
            if len(aer)!=0:
                aer = re.sub('[^0-9.%]','',aer[-1])
            else:
                aer = None
            table.append(['Term Deposits', product_names[3]+' '+sub_year_heading, text[0], 'Offline', year_heading, fts_variable, re.sub('[^0-9.%]','',inter[-1]), aer])

headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
every_day = requests.get("https://www.beta.rbs.co.uk/personal/current_accounts_in_england_wales.html",headers=headers, verify=False)
# print(every_day.content)
every_day_jsoup = BeautifulSoup(every_day.content, 'lxml')
everyDay = every_day_jsoup.find("div", attrs={"id":"everyday"}).find('h2').text
table.append(['Current', everyDay, None, 'Offline', None, None, None, None])
# print(tabulate(table))
df = pd.DataFrame(table,columns=table_headers)
def Change_bank_product_name(x):
    if "fixed" in str(x).lower():
        return "Term Deposits"
    elif "current" in str(x).lower():
        return "Current"
    elif "everyday" in str(x).lower():
        return "Current"
    else:
        return 'Savings'
       
df['Bank_Product_Type'] = df['Bank_Product_Name'].apply(Change_bank_product_name)
df['Balance']= df['Balance'].apply(lambda x : re.sub('[^a-z ,0-9-]','', str(x).replace('and','-')) if len(str(x))!=0 else x)
df.loc[:, 'Date'] = to_day.strftime("%m-%d-%Y")
df.loc[:, 'Bank_Native_Country'] = 'UK'
df.loc[:, 'State'] = 'London'
df.loc[:, 'Bank_Name'] = 'Royal Bank Of Scotland'
df.loc[:, 'Bank_Local_Currency'] = 'GBP'
df.loc[:, 'Bank_Type'] = 'Bank'
df.loc[:, 'Bank_Product'] = 'Deposits'
df.loc[:, 'Bank_Product_Code'] = None


order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER", "Bank_Product_Code"]
df = df[order]
df.to_csv(locationPath, index=False)
print(df)
