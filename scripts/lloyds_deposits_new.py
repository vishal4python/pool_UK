import requests
import re
import datetime
import time
from maks_lib import output_path
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate

print('Program Exection Started...')
starttime = time.time()

now = datetime.datetime.now()

lloydsData = []
tableHeaders = ['Bank_Product_Name','Bank_Product_Type' ,'Interest','AER', 'Balance','Term in Months']
# lloydsData.append(tableHeaders)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
resp = requests.get('https://www.lloydsbank.com/savings.asp?WT.ac=NavBarTop/Navigation/Public/navigation/top_nav/savings/All_savings_accounts#all-savings-accounts', headers=headers).content
table = BeautifulSoup(resp, 'html.parser').find('table', attrs={'class':'table sortableTable'})
if table is not None:
    for tr in table.find('tbody').find_all('tr'):
        BankName = tr.find('th').text.strip().replace('\n',' ')
        tds = tr.find_all('td')
        interest = tds[0].text.strip().replace('\n',' ')
        balance = tds[1].text.strip().replace('\n',' ')
        AER = re.findall('[0-9\.]*%', interest)
        print(len(AER))
        term_in_years = re.search('[0-9]* ?Year ', BankName)
        print('term_in_years ',term_in_years)
        term_in_years = int(re.sub('[^0-9]','', term_in_years.group(0) if term_in_years is not None else '0'))*12
        print(term_in_years)
        check = map(lambda x: x in BankName.lower(),['monthly', 'junior', 'help'])
        if any(check):
            continue
        Bank_Product_Type = 'Savings' if 'isa' in BankName.lower() else ('Term Deposits' if 'fixed bond' in BankName.lower() else 'Savings')
        if len(AER)==1:
            AER = re.sub('[^0-9\.%]', '', AER[0])
            Balance = re.search('£[0-9,]*', interest)
            lloydsData.append([BankName,Bank_Product_Type,AER, AER, re.sub('[^0-9,+-]','',balance),None if term_in_years ==0 else term_in_years])
        elif len(AER)==2:
            AER = AER
            Balance = re.findall('[a-zA-Z ]*£[0-9,]*[.\D]*', interest)
            if len(Balance) == 2:
                a = [( re.search('£[0-9,]*',b).group(0)+'+' if 'more' in b else ('1 - '+re.search('£[0-9,]*',b).group(0)if 'below' in b else re.search('£[0-9,]*',b).group(0)) )for b in Balance]
                for k in zip(AER, a):
                    print(k)
                    lloydsData.append([BankName,Bank_Product_Type, k[0], k[0], re.sub('[^0-9,+-]','',k[1]),None if term_in_years ==0 else term_in_years])

        print('-'.center(100,'-'))

print(tabulate(lloydsData))

#------------------------------------Moving Data to CSV File using Pandas----------------------------------------------

# Arrange the Order of all fields.
columns= ["Date","Bank_Native_Country","State","Bank_Name","Bank_Local_Currency","Bank_Type","Bank_Product","Bank_Product_Type","Bank_Product_Name","Balance","Bank_Offer_Feature","Term in Months","Interest_Type","Interest","AER","Bank_Product_Code"]
df = pd.DataFrame(lloydsData,columns=tableHeaders)
df["Date"] = now.strftime("%m-%d-%Y")
df["Bank_Native_Country"] = "UK"
df["State"] = "London"
df["Bank_Name"] = "Lloyds Bank"
df["Bank_Local_Currency"] = "GBP"
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Deposits"
df["Bank_Offer_Feature"] = "Offline"
df["Bank_Product_Code"] = None
df["Interest_Type"] = 'Variable'
df = df[columns]
df.to_csv(output_path + "Consolidate_Lloyds_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)  #Location of a file to store the data

print('time=',(time.time()-starttime)) #Displaying total execution time.
