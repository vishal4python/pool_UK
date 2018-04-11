
import requests
from  tabulate import tabulate
import pandas as pd
import time
import datetime
import re
from maks_lib import output_path
today = datetime.datetime.now()
print('Execution Started Please wait....')
start_time = time.time()
path = output_path+'Consolidate_Barclays_Data_Mortgage_'+today.strftime('%m_%d_%Y')+'.csv'
# path = 'Consolidate_Barclays_Data_Mortgage.csv'
Excel_Table = []
jsonHeaders = {"Host":"www.barclays.co.uk","User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0","Accept":"application/json, text/javascript, */*; q=0.01","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate, br","Referer":"https://www.barclays.co.uk/mortgages/mortgage-calculator/","Content-Type":"application/json","currentState":"default_current_state","action":"default","X-Requested-With":"XMLHttpRequest","Content-Length":"201","Connection":"keep-alive"}
table_headers = ['Bank_Product_Name', 'Min_Loan_Amount', 'Term (Y)', 'Interest_Type', 'Interest', 'APRC', 'Mortgage_Loan_Amt']


cases = [[90000, 18000], [270000, 54000], [450000, 90000]]
terms = [10, 15, 25, 30]
for case in cases:
    print('-'.center(100,'-'))
    print(case)
    for term in terms:
        print(term)
        d = {"header": {"flowId": "0"},
             "body": {"wantTo": "FTBP",
                      "estimatedPropertyValue": case[0],
                      "borrowAmount": case[0]-case[1],
                      "interestOnlyAmount": 0,
                      "repaymentAmount": case[0]-case[1],
                      "ltv": 80,
                      "totalTerm": term*12,
                      "purchaseType": "Repayment"
                      }
             }
        r = requests.post('https://www.barclays.co.uk/dss/service/co.uk/mortgages/costcalculator/productservice',json=d, headers=jsonHeaders)
        for data in r.json()['body']['mortgages']:
            # print(data)
            Bank_Product_Name = data['mortgageName']
            APRC = data['aprValue']
            Interest = data['initialRate']
            Balance = data['monthlyRepaymentHolder']['monthlyRepaymentForFixedTerm']
            Term_In_Months = data['monthlyRepaymentHolder']['fixedTermPeriod']
            LTV = data['maxLtv']
            Min_Loan_Amount = data['minLoanAmount']
            Interest_Type = data['mortgageType'].title()
            Interest_Type = Interest_Type if 'fixed' in Interest_Type.lower() else 'Variable'
            a = [Bank_Product_Name, Min_Loan_Amount, term, Interest_Type, Interest, APRC, case[0]-case[1]]
            Excel_Table.append(a)
            # print('-'.center(100,'-'))

print(tabulate(Excel_Table))
df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'Barclays Bank'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = 'Offline'
df['Mortgage_Down_Payment'] = '20%'
df['Mortgage_Category'] = 'New Purchase'
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Bank_Product_Code'] = None
df['Fixed_Rate_Term'] = df['Bank_Product_Name'].apply(lambda x: re.sub('[^0-9]','',re.findall('\d.*year',x,re.IGNORECASE)[0]) if len(re.findall('\d.*year',x,re.IGNORECASE))!=0 else None)
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Bank_Product_Code"]
df = df[order]
df.to_csv(path, index=False)

print('Execution Completed.')
print('Total Execution time is ',time.time()-start_time, 'seconds')