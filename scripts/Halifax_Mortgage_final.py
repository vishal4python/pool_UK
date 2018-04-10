import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import re
import datetime
from maks_lib import output_path
today = datetime.datetime.now()
path = output_path+'Consolidate_Halifax_Data_Mortgage_'+today.strftime('%m_%d_%Y')+'.csv'
Excel_Table = []
session = requests.session()

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}


table_headers = ['Bank_Product_Name','Interest', 'APRC', 'Mortgage_Loan_Amt','Min_Loan_Amount', 'Term (Y)', 'Interest_Type']
p = session.get('https://www.halifax.co.uk/mortgages/mortgage-calculator/calculator/',headers=headers)
print(session.cookies)

cases = [[90000,18000],[270000, 54000],[450000,90000]]
terms = [10,15,25,30]
for case in cases:
    for term in terms:
        formData = {"aprTextValue":"APRC",
                    "radioMortgFor":"fstHom",
                    "mortgReq":case[0]-case[1],
                    "valueOfprop":case[0],
                    "mortgTermYrs":term,
                    "AddlAmt":0,
                    "additionalBorrowingAmt":0
                    }

        p = session.post('https://www.halifax.co.uk/asp_includes/mortgages/mortgage-calculator-responsive/calculatorFunctions.asp',data = formData, headers=headers).content
        divs = BeautifulSoup(p,'html.parser').find_all('div', attrs={'class':'product'})
        for div in divs:
            try:
                print(div)
                Bank_product_name = div.find('div', attrs={'class':'heading'})
                Interest = div.find('div', attrs={'class': 'rate'})
                aprc = div.find('div', attrs={'class': 'cost-comparison'})
                a = [Bank_product_name.text if Bank_product_name is not None else None, Interest.text if Interest is not None else None, aprc.text if aprc is not None else None,case[0]-case[1],None, term, 'Fixed']
                Excel_Table.append(a)
            except Exception as e:
                print(e)

print(tabulate(Excel_Table))
df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Bank_Product_Name'] = df['Bank_Product_Name'].apply(lambda x: x.split('%')[0] if '%' in x else x)
df['Interest'] = df['Interest'].apply(lambda x: re.findall('\d.*% ',x)[0] if len(re.findall('\d.*%',x))!=0 else None)
df['APRC'] = df['APRC'].apply(lambda x: re.findall('\d.*%',x)[0] if len(re.findall('\d.*%',x))!=0 else None)


df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'Halifax'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = 'Offline'
df['Mortgage_Down_Payment'] = '20%'
df['Mortgage_Category'] = 'New Purchase'
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Fixed_Rate_Term'] = df['Bank_Product_Name'].apply(lambda x: re.sub('[^0-9]','',re.findall('\d.*year',x,re.IGNORECASE)[0]) if len(re.findall('\d.*year',x,re.IGNORECASE))!=0 else None)
df['Bank_Product_Code'] = None
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Bank_Product_Code"]
df = df[order]
df.to_csv(path, index=False)