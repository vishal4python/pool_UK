# -*- coding:utf-8 -*-
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import time
import pandas as pd
import datetime
from maks_lib import output_path
today  = datetime.datetime.now()
startTime = time.time()
path = output_path+"Consolidate_MoneyMarket_Data_Deposits_"+str(today.strftime('%Y_%m_%d'))+'.csv'
Excel_table = []
table_headers = ['Bank_Name', 'Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature',
                 'Term_in_Months', 'Interest', 'AER']
Excel_table.append(table_headers)
browser = webdriver.Firefox()
browser.maximize_window()
neededUkBanks = {'royal bank of scotland':'Royal Bank Of Scotland',
                 'natwest':'NatWest',
                 'lloyds bank':'Lloyds Bank',
                 'lloyds':'Lloyds Bank',
                 'hsbc':'HSBC',
                 'tsb':'TSB',
                 'barclays':'Barclays',
                 'bank of ireland':'Bank of Ireland',
                 'bank of ireland uk':'Bank of Ireland',
                 'metro bank':'Metro Bank',
                 'bank of scotland':'Bank of Scotland',
                 'the co-operative bank':'The Co-operative Bank',
                 'cooperative bank':'The Co-operative Bank',
                 'halifax':'Halifax',
                 'santander Bank':'Santander Bank',
                 'santander':'Santander Bank',
                 'clydesdale bank':'Clydesdale Bank',
                 'clydesdale':'Clydesdale Bank',
                 'virgin money plc.':'Virgin Money Plc.',
                 'virgin money':'Virgin Money Plc.'
                 }

types = ['https://www.moneysupermarket.com/savings/results/?goal=SAV_EASYACCESS',
         'https://www.moneysupermarket.com/savings/results/?goal=SAV_CASHISA']
# https://www.moneysupermarket.com/current-accounts/results/?goal=cur_all##    ,'https://www.moneysupermarket.com/savings/results/?goal=SAV_FIXEDRATEBONDS'
urlList = []

for i in types:
    urlDict = {}
    browser.get(i)
    page = browser.page_source
    page = BeautifulSoup(page).find('span', attrs={'class': 'msm-pagination__current'})
    if page is not None:
        print(page.text.split()[-1])
        urlDict['pageNumber'] = int(page.text.split()[-1])
        urlDict['url'] = i
        urlList.append(urlDict)
# print(browser.page_source)
print(urlList)

for url in urlList:
    print('-'.center(100, '-'))
    for i in range(1, 3):
        #     for i in range(1,url['pageNumber']+1):
        print(url['url'] + '&page=' + str(i))
        browser.get(url['url'] + '&page=' + str(i))
        jsoup = BeautifulSoup(browser.page_source)
        divs = jsoup.find_all('div', attrs={'class': 'msm-best-buy-table__wrapper'})
        for div in divs:
            Bank_Name = div.find('span', attrs={'class': 'msm-best-buy-table__header-description--title'})
            Bank_Product_Name = div.find('div', attrs={'class': 'msm-best-buy-table__header-description'}).find('div')
            Bank_Name = Bank_Name.text if Bank_Name is not None else None
            Bank_Product_Name = Bank_Product_Name.text if Bank_Product_Name is not None else None
            aer_interest = div.find('span', attrs={'class': 'msm-best-buy-table__cell-description'})
            AER = aer_interest.text if aer_interest is not None else None
            balance = div.find('div', attrs={'class': 'msm-best-buy-table__cell msm-best-buy-table__cell--default'})
            Balance = balance.text if balance is not None else None
            # bank_offer_feature = div.find('div', attrs = {'class':'msm-best-buy-table__list-container msm-best-buy-table__list-container--horizontal'})
            # Bank_Offer_Feature = if bank_offer_feature is not None:
            #     print(bank_offer_feature.text)
            for k in neededUkBanks:
                if Bank_Name is not None:
                    if k in Bank_Name.lower().strip():
                        a = [neededUkBanks[k], 'Savings', Bank_Product_Name, Balance, 'Offline', None, AER, AER]
                        Excel_table.append(a)
                        break

try:
    type1_fixed = ['https://www.moneysupermarket.com/savings/results/?goal=SAV_FIXEDRATEBONDS']
    urlList1 = []
    for j in type1_fixed:
        urlDict1 = {}
        browser.get(j)
        page1 = browser.page_source
        page1 = BeautifulSoup(page1).find('span', attrs={'class': 'msm-pagination__current'})
        if page1 is not None:
            print(page1.text.split()[-1])
            urlDict1['pageNumber1'] = int(page1.text.split()[-1])
            urlDict1['url1'] = j
            urlList1.append(urlDict1)
    # print(browser.page_source)
    print(urlList1)
    #
    for url1 in urlList1:
        # print('-'.center(100, '-'))
        for j in range(1, url1['pageNumber1'] + 1):
            print(url1['url1'] + '&page=' + str(j))
            browser.get(url1['url1'] + '&page=' + str(j))
            jsoup = BeautifulSoup(browser.page_source)
            divs1 = jsoup.find_all('div', attrs={'class': 'msm-best-buy-table__wrapper'})
            for div1 in divs1:
                Bank_Name1 = div1.find('span', attrs={'class': 'msm-best-buy-table__header-description--title'})
                Bank_Name = Bank_Name1.text if Bank_Name1 is not None else None
                aer_interest1 = div1.find('span', attrs={'class': 'msm-best-buy-table__cell-description'})
                AER = aer_interest1.text if aer_interest1 is not None else None
                balance1 = div1.find('div',
                                     attrs={'class': 'msm-best-buy-table__cell msm-best-buy-table__cell--default'})
                Balance = balance1.text if balance1 is not None else None
                Bank_Product_Name = div.find('div', attrs={'class': 'msm-best-buy-table__header-description'}).find(
                    'div')
                Bank_Product_Name = Bank_Product_Name.text if Bank_Product_Name is not None else None
                # bank_offer_feature1 = div1.find('div', attrs={
                #     'class': 'msm-best-buy-table__list-container msm-best-buy-table__list-container--horizontal'})
                # bank_offer_feature1 = if bank_offer_feature1 is not None:
                #     print(bank_offer_feature1.text)

                term1 = \
                div1.find_all('div', attrs={'class': 'msm-best-buy-table__cell msm-best-buy-table__cell--default'})[
                    1].find('span')
                term1 = term1.text if term1 is not None else None

                for k in neededUkBanks:
                    if Bank_Name is not None:
                        if k in Bank_Name.lower().strip():
                            a = [neededUkBanks[k], 'Term Deposits', Bank_Product_Name, Balance, 'Offline', term1, AER, AER]
                            Excel_table.append(a)
                            break

except Exception as e:
    print(e)

try:
    type2_current = ['https://www.moneysupermarket.com/current-accounts/results/?goal=cur_all##']
    urlList2 = []
    for k in type2_current:
        urlDict2 = {}
        browser.get(k)
        page2 = browser.page_source
        page2 = BeautifulSoup(page2).find('span', attrs={'class': 'msm-pagination__current'})
        if page2 is not None:
            # print(page2.text.split()[-1])
            urlDict['pageNumber2'] = int(page2.text.split()[-1])
            urlDict['url2'] = k
            urlList2.append(urlDict)
    # print(browser.page_source)
    print(urlList2)

    for url2 in urlList2:
        print('-'.center(100, '-'))
        for k in range(1, url2['pageNumber'] + 1):
            print(url2['url2'] + '&page=' + str(k))
            browser.get(url2['url2'] + '&page=' + str(k))
            jsoup = BeautifulSoup(browser.page_source)
            divs2 = jsoup.find_all('div', attrs={'class': 'msm-best-buy-table__wrapper'})
            for div2 in divs2:
                Bank_Name2 = div2.find('div', attrs={'class': 'msm-best-buy-table__header-description'}).find('a')
                Bank_Name = Bank_Name2.text if Bank_Name2 is not None else None
                aer_interest2 = div2.find('span', attrs={'class': 'msm-best-buy-table__percentage'})
                AER = aer_interest2.text if aer_interest2 is not None else None
                try:
                    balance = \
                    div2.find_all('div', attrs={'class': 'msm-best-buy-table__cell msm-best-buy-table__cell--default'})[
                        1].find_all('p')[1]
                    balance = balance.text if balance is not None else None
                except:
                    balance = None
                Bank_Product_Name = div.find('div', attrs={'class': 'msm-best-buy-table__header-description'}).find(
                    'div')
                Bank_Product_Name = Bank_Product_Name.text if Bank_Product_Name is not None else None
                for k in neededUkBanks:
                    if Bank_Name is not None:
                        if k in Bank_Name.lower().strip():
                            a = [neededUkBanks[k], 'Current', Bank_Product_Name, balance, 'Offline', None, AER, AER]
                            Excel_table.append(a)
                            break


except Exception as x:
    print(x)

def getTermInMonths(x):
    if x is None:
        return None
    check_year = re.search('\d.* Year', x.replace('to', '-'), re.IGNORECASE)
    check_month = re.search('\d.* Month', x.replace('to', '-'), re.IGNORECASE)
    splitChar = ['-', '|']
    if check_year:
        year = re.sub('[^0-9-]', '', check_year.group(0))
        for splitC in splitChar:
            if splitC in year:
                year = year.split(splitC)[0]
                break
        return int(year) * 12
    elif check_month:
        check_month = re.sub('[^0-9-]', '', check_month.group(0))

        for splitC in splitChar:
            if splitC in check_month:
                check_month = check_month.split(splitC)[0]
                break
        return int(check_month)
    else:
        return None

browser.close()
print(tabulate(Excel_table))
df = pd.DataFrame(Excel_table, columns=table_headers)
df['Bank_Name'] = df['Bank_Name'].apply(lambda x: str(x).strip() if x is not None else x)
df['Bank_Product_Name'] = df['Bank_Product_Name'].apply(lambda x: str(x).strip() if x is not None else x)
df['Balance'] = df['Balance'].apply(lambda x: re.sub('[^0-9-,]', '', re.findall('£\d.*\d',x.replace('to', '-').replace('and','-') if x is not None else '')[0]) if len(re.findall('£\d.*\d', x if x is not None else '')) != 0 else None)
df['Term_in_Months'] = df['Term_in_Months'].apply(getTermInMonths)
df['Interest'] = df['Interest'].apply(lambda x: str(x).strip() if x is not None else x)
df['AER'] = df['AER'].apply(lambda x: str(x).strip() if x is not None else x)
df['Date'] = ''
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Bank_Product_Code'] = None
df['Interest_Type'] = 'Fixed'
df['Source'] = 'moneysupermarket.com'

order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product",
         "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Balance", "Bank_Offer_Feature",
         "Term_in_Months", "Interest_Type", "Interest", "AER", "Source"]
df = df[order]
df.to_csv(path, index=False)