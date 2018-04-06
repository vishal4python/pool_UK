import requests
from bs4 import BeautifulSoup
import json
import re
from tabulate import tabulate
import pandas as pd
import datetime
from maks_lib import output_path

today = datetime.datetime.now()
path = output_path + "Consolidate_Comparethemarket_Data_Deposit_"+today.strftime("%m_%d_%Y")+".csv"
# path = 'Comparethemarket_Data_Deposits_'+today.strftime('%m-%d-%Y')+'.csv'
Excel_Table = []
table_headers = ['Bank_Name', 'Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term_in_Months', 'Interest', 'AER']
# Excel_Table.append(table_headers)
remove_data = ['man', 'online saver', 'preferential rate', 'help']
neededUkBanks = {'royal bank of scotland':'Royal Bank Of Scotland',
                 'natwest':'NatWest',
                 'lloyds bank':'Lloyds Bank',
                 'hsbc':'HSBC',
                 'tsb':'TSB',
                 'barclays':'Barclays',
                 'bank of ireland':'Bank of Ireland',
                 'bank of ireland uk':'Bank of Ireland',
                 'metro bank':'Metro Bank',
                 'bank of scotland':'Bank of Scotland',
                 'the co-operative bank':'The Co-operative Bank',
                 'halifax':'Halifax',
                 'santander Bank':'Santander Bank',
                 'santander':'Santander Bank',
                 'clydesdale bank':'Clydesdale Bank',
                 'virgin money plc.':'Virgin Money Plc.',
                 'virgin money':'Virgin Money Plc.'}

urlList = [['Savings', 'https://money.comparethemarket.com/savings-accounts/'],
           ['Savings', 'https://money.comparethemarket.com/savings-accounts/cash-isas/'],
           ['Term Deposits', 'https://money.comparethemarket.com/savings-accounts/fixed-rate-bonds/']
           ]

for url in urlList:
    resp = requests.get(url[1]).content
    jsoup = BeautifulSoup(resp,'html.parser').find('div', attrs={'id':'savings-json'})
    # print(jsoup.text)
    for js in json.loads(jsoup.text):
        Bank_Product_Name = js['Name']
        check_year = re.search('\d.*Year', Bank_Product_Name,re.IGNORECASE)
        check_month = re.search('\d.*Month', Bank_Product_Name, re.IGNORECASE)
        splitChar = ['-', '|']
        if check_year:
            year = re.sub('[^0-9-|]', '', check_year.group(0))
            for splitC in splitChar:
                if splitC in year:
                    year =year.split(splitC)[0]
                    break
            Term_in_Months = int(year)*12
        elif check_month:
            check_month = re.sub('[^0-9-|]', '', check_month.group(0))
            for splitC in splitChar:
                if splitC in check_month:
                    check_month = check_month.split(splitC)[0]
                    break
            Term_in_Months = int(check_month)
        else:
            Term_in_Months = None
        Bank_Name = js['ProviderBrandName']
        Interest = AER = js['GrossAerString']
        Balance = js['MinimumInvestmentString'] +'-'+ js['MaximumInvestmentString']
        Bank_Offer_Feature = 'Online' if js['HasInternetAccess'] else 'Offline'
        if Bank_Name.lower().strip() in neededUkBanks:
            found = False
            for check in remove_data:
                if check in Bank_Product_Name.lower().strip():
                    found = True
                    break
            if not found:
                a = [neededUkBanks[Bank_Name.lower().strip()], url[0], Bank_Product_Name, Balance, Bank_Offer_Feature, Term_in_Months,Interest, AER]
                Excel_Table.append(a)
#     # print('-'.center(100,'-'))
# # print(js)
# # print(resp)


resp = requests.get('https://money.comparethemarket.com/current-accounts/?AFFCLIE=CM01').content
jsoup = BeautifulSoup(resp,'html.parser').find('div', attrs={'id':'current-accounts-json'})
    # print(jsoup.text)
for js in json.loads(jsoup.text):
    Bank_Product_Name = js['Name']
    check_year = re.search('\d.* Year', Bank_Product_Name.replace('to','-'),re.IGNORECASE)
    check_month = re.search('\d.* Month', Bank_Product_Name.replace('to','-'), re.IGNORECASE)
    splitChar = ['-', '|']
    if check_year:
        print(check_year.group(0))
        year = re.sub('[^0-9-]', '', check_year.group(0))
        for splitC in splitChar:
            if splitC in year:
                year =year.split(splitC)[0]
                break
        Term_in_Months = int(year)*12
    elif check_month:
        print(check_month.group(0))
        check_month = re.sub('[^0-9-]', '', check_month.group(0))

        for splitC in splitChar:
            if splitC in check_month:
                check_month = check_month.split(splitC)[0]
                break
        Term_in_Months = int(check_month)
    else:
        Term_in_Months = None
    Bank_Name = js['ProviderBrandName']
    Interest = AER = js['GrossAerString']
    # Balance = js['MinimumInvestmentString'] +'-'+ js['MaximumInvestmentString']
    # Bank_Offer_Feature = 'Online' if js['HasInternetAccess'] else 'Offline'
    Balance = None
    Bank_Offer_Feature = None
    Term_in_Months = None
    if Bank_Name.strip() in neededUkBanks:
        found = False
        for check in remove_data:
            if check in Bank_Product_Name.lower().strip():
                found = True
                break
        if not found:
            a = [neededUkBanks[Bank_Name.lower().strip()], 'Checkings', Bank_Product_Name, Balance, Bank_Offer_Feature, Term_in_Months,Interest, AER]
            Excel_Table.append(a)

df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Interest_Type'] = 'Fixed'
df['Source'] = 'comparethemarket.com'
df['Bank_Product_Code'] = None
df['Balance'] = df['Balance'].apply(lambda x:re.sub('[^0-9-]','',str(x)).strip('-'))
order = ["Date", "Bank_Native_Country", "State", "Bank_Name","Ticker", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term_in_Months", "Interest_Type", "Interest", "AER", "Source"]
df['AER'] = df['AER'].apply(lambda x:re.sub('[^0-9%.]','',x))
df['Interest'] = df['Interest'].apply(lambda x:re.sub('[^0-9%.]','',x))
df = df[order]
df.to_csv(path, index=False)
print(tabulate(Excel_Table))
