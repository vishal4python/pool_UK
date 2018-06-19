import requests
from bs4 import BeautifulSoup
import json
import datetime
today = datetime.datetime.now()
from tabulate import tabulate
import pandas as pd
import math
import re
import time
starttime = time.time()
from runAllScriptsOnce.maks_lib import output_path
Excel_Table = []
headers = {'content-type':	'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
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
                 'halifax intermediaries':'Halifax',
                 'santander Bank':'Santander Bank',
                 'santander':'Santander Bank',
                 'clydesdale bank':'Clydesdale Bank',
                 'virgin money plc.':'Virgin Money Plc.',
                 'virgin money':'Virgin Money Plc.'}

table_headers = ['Bank_Name', 'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature', 'Term (Y)', 'Interest_Type', 'Interest', 'APRC', 'Mortgage_Loan_Amt','Fixed_Rate_Term']
# Excel_Table.append(table_headers)
path = output_path+"Aggregator_CompareTheMarket_Mortgage_"+str(today.strftime('%Y_%m_%d'))+'.csv'
cases = [[90000, 72000],[270000, 216000], [450000, 360000]]
terms = [10,15,25,30]
for term in terms:
    print('-'.center(100,'-'))
    print('Term:',term)
    for case in cases:
        print('propertyValue = ',case[0])
        print('Deposits = ',case[0]-case[1])
        print('borrowingAmount = ', case[1])
        resp = requests.post('https://mortgage-table-presenter.comparethemarket.com/mortgage/calculations/?'\
        'borrowingAmount='+str(case[1])+'&customerType=FIRST_TIME&mortgageTerm='+str(term)+'&propertyValue='+str(case[0])+'&remainingBalance=0&'\
        'repaymentOption=REPAYMENT',headers=headers)
        print('No .of Reaults = ',resp.json()['totalProducts'])
        totalProducts = int(resp.json()['totalProducts']) / 10
        i = 0
        for r in range(math.ceil(totalProducts)):
            url = 'https://mortgage-table-presenter.comparethemarket.com/mortgage/calculations/?borrowingAmount='+str(case[1])+'&' \
                  'customerType=FIRST_TIME&limit=10&mortgageTerm='+str(term)+'&offset=' + str(i) + '&orderBy=initialMonthlyPayment&propertyValue='+str(case[0])
            loopresp = requests.post(url, headers=headers)
            i = i + 10

            for product in loopresp.json()['mortgageProducts']:
                # print(product)
                Bank_Name = product['providerName']
                Bank_Product_Name = product['displayName']
                Interest = product['initialRate']
                APRC = product['aprc']
                fixed_rate_term = product.get('initialTermYears', None)
                # print(fixed_rate_term)
                if Bank_Name.lower().strip() in neededUkBanks:
                    a = [neededUkBanks[Bank_Name.lower().strip()], Bank_Product_Name, None, 'Offline', term, 'Fixed', str(Interest)+'%', str(APRC)+'%', case[1],fixed_rate_term]
                    if a not in Excel_Table:
                        Excel_Table.append(a)

df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
# df['Ticker'] = 'Ticker file'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Product_Code'] = None
df['Mortgage_Down_Payment'] = '20%'
df['Mortgage_Category'] = 'New Purchase'
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Source'] = 'comparethemarket.com'
# df['Fixed_Rate_Term'] = df['Fixed_Rate_Term'].apply(lambda x: re.sub('[^0-9]','',re.findall('\d.* ',x)[0]) if len(re.findall('\d.* ',x))!=0 else None)
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode","Fixed_Rate_Term", "Source"]
df = df[order]
print(tabulate(Excel_Table))
if len(df.values)!=0:
    df.to_csv(path, index=False)
else:
    print('Data Not Found...')

print('time=',(time.time()-starttime))
