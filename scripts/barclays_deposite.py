import  pandas as pd
import requests
import re
from bs4 import BeautifulSoup as bs
from tabulate import tabulate
import numpy as np
import datetime
now = datetime.datetime.now()
from maks_lib import output_path
import warnings
warnings.simplefilter(action='ignore')
data = []
path = output_path + "Consolidate_Barclays_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y"))

links = ['https://www.barclays.co.uk/savings/instant-access/',
         'https://www.barclays.co.uk/savings/isas/',
         'https://www.barclays.co.uk/savings/bonds/',
         'https://www.barclays.co.uk/current-accounts/'
         ]
table_headers = ['Bank_Product_Name','AER','Interest','Balance','Min_opening_Bal','Bank_Product_Type','Term in Months']

def instant_access():
    res = requests.get("https://www.barclays.co.uk/savings/instant-access/")
    soup = bs(res.content,'html.parser')
    head = soup.find('div',attrs={"class":"col-sm-6 col-sm-offset-3 wrapper-heading"})
    bank_type = head.find('h2').text.split(" ")[1].capitalize()
    result = soup.find("table", attrs={"id":"table"})
    trs = result.find_all('tr')
    c = 0
    for tr in trs:
        p = tr.find_all('p')
        if c == 0:
            c += 1
            continue
        else:
            product_name = p[0].text.replace("\n","")
            if c == 1:
                AER1 = re.search(r'\d\.\d+%',p[1].text).group()
                interest1 = AER1
                Balance1 = re.search(r'\(.*\)',p[1].text).group().rstrip(")").lstrip("(")
                AER2 = re.search(r'\d\.\d+%',p[2].text).group()
                interest2 = AER2
                Balance2 = re.search(r'\(.*\)',p[2].text).group().rstrip(")").lstrip("(")
                MIN = p[3].text
                data.append([product_name, AER1,interest1,Balance1, MIN, bank_type,None])
                data.append([product_name, AER2, interest2,Balance2, MIN, bank_type,None])
                c += 1

def iaas():
    res = requests.get('https://www.barclays.co.uk/savings/isas/')
    soup = bs(res.content, "html.parser")
    result = soup.find("table", attrs={"id": "table"})
    trs = result.find_all('tr')
    c = 0
    for tr in trs:
        p = tr.find_all('p')
        #print(p)
        if c == 0:
            c += 1
            continue
        else:
            product_name = p[0].text.replace("\n", "")
            if c == 1:
                interest1 = AER1 =  p[1].text
                Balance1 = p[2].text.strip("(").strip(")2")
                interest2 = AER2 = p[5].text
                Balance2 = p[6].text.lstrip("(").rstrip(")2")
                interest3 = AER3 = p[8].text
                Balance3 = p[9].text.lstrip("(").rstrip(")2")
                MIN = p[10].text.strip("2")
                data.append([product_name, AER1, interest1, Balance1, MIN,'Savings',None])
                data.append([product_name, AER2, interest2, Balance2, MIN,'Savings',None])
                data.append([product_name, AER3, interest3, Balance3, MIN,'Savings',None])
                c += 1
            elif c == 2:
                interest = AER = re.search(r'\d\.\d+%',p[1].text).group()
                Balance = p[2].text.strip("(").strip(")2")
                MIN = p[3].text.strip("2")
                Term_in_Months = int(product_name.split("-")[0]) * 12
                data.append([product_name, AER, interest, Balance, MIN,'Savings',Term_in_Months])
                c += 1

def bonds():
    res = requests.get('https://www.barclays.co.uk/savings/bonds/')
    soup = bs(res.content, "html.parser")
    result = soup.find("table", attrs={"id": "table"})
    trs = result.find_all('tr')
    c = 0
    for tr in trs:
        p = tr.find_all('p')
        if c == 0:
            c += 1
            continue
        else:
            product_name = p[0].text.replace("\n", "")
            Term_in_Months = int(product_name.split("-")[0]) * 12
            if c == 1:
                interest = AER = p[1].text
                Balance = p[2].text.strip("(").strip(")\n")
                MIN = p[3].text
                data.append([product_name, AER, interest, Balance, MIN, 'Term Deposits',Term_in_Months])
                c += 1
            elif c == 2:
                interest = AER = p[1].text
                Balance = p[2].text.strip("(").strip(")\n")
                MIN = p[3].text.rstrip("\n")
                data.append([product_name, AER, interest, Balance, MIN, 'Term Deposits',Term_in_Months])
                c += 1

def current():
    res = requests.get('https://www.barclays.co.uk/current-accounts/')
    soup = bs(res.content, "html.parser")
    results = soup.find_all("h3", attrs={"class": "promo-title"})
    product_name1 = results[0].text
    product_name2 = results[1].text
    data.append([product_name1, None, None, None, None, "Current",None])
    data.append([product_name2, None, None, None, None, "Current",None])

def main():
    instant_access()
    iaas()
    bonds()
    current()
    #print(tabulate(data))

if __name__ == '__main__':
    print("Scraping Started..")
    main()
    data = pd.DataFrame(data, columns=table_headers)
    data['Date'] = now.strftime("%Y-%m-%d")
    data['Bank_Native_Country'] = 'UK'
    data['State'] = 'London'
    data['Bank_Name'] = 'Barclays'
    data['Bank_Local_Currency'] = 'GBP'
    data['Bank_Type'] = 'Bank'
    data['Bank_Product'] = 'Deposits'
    data['Bank_Offer_Feature'] = "Offline"
    #data["Term in Months"] = np.nan
    data["Bank_Product_Code"] = np.nan
    data["Interest_Type"] = "Fixed"
    data["Min_opening_Bal"] = data["Min_opening_Bal"].apply(lambda x: re.sub('[^0-9.-]','',str(x)))
    data["Balance"] = " "+data["Balance"].apply(lambda x: re.sub('[^0-9.,-]','',str(x).replace('to','-').replace("million", "000000")))
    order = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name', 'Bank_Local_Currency', 'Bank_Type', 'Bank_Product',
             'Bank_Product_Type', 'Bank_Product_Name','Balance', 'Bank_Offer_Feature', 'Term in Months', 'Interest_Type',
             'Interest', 'AER', 'Bank_Product_Code']
    df = data[order]
    df.to_csv(path, index=False)
    print("Scraping Finished !!!")
