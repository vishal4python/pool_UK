import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import pandas as pd
Excel_Table =[]
import datetime
from maks_lib import output_path

today = datetime.datetime.now()
path = output_path + "Consolidate_Agg_UK_Deposit_Data_Mortgage_"+today.strftime("%m_%d_%Y")+".csv"

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
                 'virgin money':'Virgin Money Plc.'}

table_headers = ['Bank_Name', 'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature', 'Fixed_Rate_Term', 'Interest_Type', 'Interest', 'APRC', 'Mortgage_Loan_Amt']
# Excel_Table.append(table_headers)
headers = {"Accept": "text/html, */*; q=0.01",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9",
"Connection": "keep-alive",
"Host": "uk.deposits.org",
"Referer": "https://uk.deposits.org/loans/",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
"X-Requested-With": "XMLHttpRequest"}
urlList =["https://uk.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=fixed",
          "https://uk.deposits.org/index.html?is_ajax=true&ajax=loans&param=all&param_specific=p2p"]
for url in urlList:
    resp = requests.get(url, headers=headers).content
    # print(resp)
    trs = BeautifulSoup(resp).find('div', attrs={'class':'reload_tabs'}).find('table').find('tbody').find_all('tr')
    for tr in trs:
        td = tr.find_all('td')
        Bank_Name = td[0].find('a', attrs={'class':'title'}).text
        Bank_Product_Name = td[1].find('a', attrs={'class': 'title'}).text
        Interest = td[2].find('span', attrs={'class':'details'}).text
        td[2].find('span').extract()
        APRC = td[2].text
        Term = Bank_Product_Name
        check = Term
        # print(check)
        Interest_Type = 'Fixed' if 'fixed' in Term.lower() else 'Variable'


        check_year = re.search('\d.* year', Term.replace('to', '-'), re.IGNORECASE)

        if check_year:
            # print(check_year.group(0))
            splitChar = ['-', '|']
            year = re.sub('[^0-9-]', '', check_year.group(0))
            for splitC in splitChar:
                if splitC in year:
                    Term = year.split(splitC)[0]
                    break
                else:
                    Term = year

        else:
            Term = None

        # print(td[2])
        for bank in neededUkBanks.keys():
            if bank.lower() in Bank_Name.lower() or bank.lower() in Bank_Product_Name.lower():
                a = [neededUkBanks[bank], Bank_Product_Name, None, 'Offline', Term, Interest_Type, Interest, APRC, None]
                Excel_Table.append(a)
                break


print(tabulate(Excel_Table))
df = pd.DataFrame(Excel_Table, columns=table_headers)
df["Date"] = ' '+today.strftime('%Y-%m-%d')
df["Bank_Native_Country"] = "UK"
df["State"] = "London"
df["Bank_Local_Currency"] = "GBP"
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Bank_Offer_Feature"] = "Offline"
df["Mortgage_Category"] = "New Purchase"
df["Mortgage_Reason"] = "Primary Residence"
df["Mortgage_Pymt_Mode"] = "Principal + Interest"
df["Bank_Product_Code"] = None
df['Source'] = 'uk.deposits.org'
df['Mortgage_Down_Payment'] = '20%'
df['Term (Y)'] = None
df['APRC'] = df['APRC'].apply(lambda x:re.sub('[^0-9%-.]','',str(x)))
order = ["Date", "Bank_Native_Country", "State", "Bank_Name","Ticker", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Source"]
df = df[order]
df.to_csv(path, index=False)
