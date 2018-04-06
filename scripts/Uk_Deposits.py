import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import datetime
from maks_lib import output_path
today = datetime.datetime.now()
path = output_path + "Consolidate_Agg_UK_Deposit_Data_Deposit_"+today.strftime("%m_%d_%Y")+".csv"
# path = 'mybanktracker_Data_UK_Deposits_'+today.strftime('%m-%d-%Y')+'.csv'
import re
Excel_Table = []
table_headers = ['Bank_Name', 'Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term_in_Months', 'Interest', 'APY']
# Excel_Table.append(table_headers)

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


# resp = requests.get('https://uk.deposits.org/savings-accounts/').content
urlList = [['Savings','https://uk.deposits.org/savings-accounts/'], ['Term Deposits','https://uk.deposits.org/deposits/']]
for url in urlList:
    resp = requests.get(url[1]).content
    # print(resp)
    trs = BeautifulSoup(resp).find('div', attrs={'class':'boxed'}).find('table').find('tbody').find_all('tr')

    for tr in trs:
        # print(tr)
        td = tr.find_all('td')
        Bank_Name = td[0].find('a', attrs={'class':'title'}).text
        Bank_Product_Name = td[1].find('a', attrs={'class':'title'}).text
        Balance = td[1].find('span')
        if Balance is not  None:
            Balance = Balance.text
            if re.search('minimum.*\d', Balance, re.IGNORECASE) is not  None:
                ab = re.search('minimum.*\d', Balance, re.IGNORECASE)
                # print(re.split('\s',ab.group(0)))
                for k in re.split('\s',ab.group(0)):
                    if re.search('\$\d.*\d',k) is not None:
                        Balance = k
                        break
                    else:
                        Balance = None
            else:
                Balance = None
        else:
            Balance = None
        Interest = td[2].find('span', attrs={'class':'details'}).text

        check_year = re.search('\d.* Year', Bank_Product_Name.replace('to', '-'), re.IGNORECASE)
        check_month = re.search('\d.* Month', Bank_Product_Name.replace('to', '-'), re.IGNORECASE)
        splitChar = ['-', '|']
        if check_year:
            year = re.sub('[^0-9-]', '', check_year.group(0))
            for splitC in splitChar:
                if splitC in year:
                    year = year.split(splitC)[0]
                    break
            Term_in_Months = int(year) * 12
        elif check_month:
            check_month = re.sub('[^0-9-]', '', check_month.group(0))

            for splitC in splitChar:
                if splitC in check_month:
                    check_month = check_month.split(splitC)[0]
                    break
            Term_in_Months = int(check_month)
        else:
            Term_in_Months = None
        Bank_Name = Bank_Name.replace(url[0], '').strip()
        # if Bank_Name.lower().strip() in neededUkBanks:
        for k in neededUkBanks.keys():
            if k in Bank_Name.lower():
                Interest = Interest.replace('or', '-')
                if '-' in Interest:

                    Interest = Interest.split('-')[0]
                a = [neededUkBanks[k], url[0], Bank_Product_Name, Balance,'Offline', Term_in_Months,Interest, None]
                Excel_Table.append(a)
                break

df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Bank_Product_Code'] = None
df['Interest_Type'] = 'Fixed'
df['Source'] = 'uk.deposits.org'
df['Balance'] = df['Balance'].apply(lambda x:re.sub('[^0-9,]','',str(x)) if len(re.sub('[^0-9,]','',str(x)))!=0 else None)
order = ["Date", "Bank_Native_Country", "State", "Bank_Name","Ticker", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term_in_Months", "Interest_Type", "Interest", "APY", "Source"]
df = df[order]
df.to_csv(path, index=False)
print(tabulate(Excel_Table))
