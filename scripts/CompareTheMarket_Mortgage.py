import requests
from bs4 import BeautifulSoup
import json
import datetime
today = datetime.datetime.now()
from tabulate import tabulate
import pandas as pd
from maks_lib import output_path
Excel_Table = []
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

table_headers = ['Bank_Name', 'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature', 'Term (Y)', 'Interest_Type', 'Interest', 'APRC', 'Mortgage_Loan_Amt']
# Excel_Table.append(table_headers)
path = output_path+"Consolidate_CompareTheMarket_mortgage_"+str(today.strftime('%Y_%m_%d'))+'.csv'
cases = [[90000, 72000],[270000, 216000], [450000, 360000]]
terms = [10,15,25,30]
for term in terms:
    print('Term:',term)
    for case in cases:
        resp = requests.get('https://money.comparethemarket.com/mortgages/first-time-buyer/?AFFCLIE=CM01&PropertyValue='+str(case[0])+'&BorrowAmount='+str(case[1])+'&Term='+str(term)+'&IsInterestOnly=false&IsRequestFromTool=true').content
        for js in json.loads(BeautifulSoup(resp, 'html.parser').find('div', attrs={'id':'mortgages-json'}).text):
            Bank_Name = js['LenderName']
            Bank_Product_Name = js['ProductName']
            Interest = js['InitialRate']
            APRC = js['Aprc']
            if Bank_Name.lower().strip() in neededUkBanks:
                a = [neededUkBanks[Bank_Name.lower().strip()], Bank_Product_Name, None, 'Offline', term, 'Fixed', str(Interest)+'%', str(APRC)+'%', case[1]]
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
order = ["Date", "Bank_Native_Country", "State", "Bank_Name","Ticker", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Source"]
df = df[order]
df.to_csv(path, index=False)
print(tabulate(Excel_Table))
