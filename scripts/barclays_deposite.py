import  pandas as pd
import requests
import re
from bs4 import BeautifulSoup as bs
from tabulate import tabulate
data = []
links = ['https://www.barclays.co.uk/savings/instant-access/',
         'https://www.barclays.co.uk/savings/isas/',
         'https://www.barclays.co.uk/savings/bonds/',
         'https://www.barclays.co.uk/current-accounts/'
         ]
table_headers = ['Bank_Product_Name','AER','Interest','Balance','Min_opening_Bal','Bank_Product_Type']

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
                AER1 = re.search(r'\d+%',p[1].text).group()
                interest1 = AER1
                Balance1 = re.search(r'\(.*\)',p[1].text).group().rstrip(")").lstrip("(")
                AER2 = re.search(r'\d+%',p[2].text).group()
                interest2 = AER2
                Balance2 = re.search(r'\(.*\)',p[2].text).group().rstrip(")").lstrip("(")
                MIN = p[3].text
                data.append([product_name, AER1,interest1,Balance1, MIN, bank_type])
                data.append([product_name, AER2, interest2,Balance2, MIN, bank_type])
                c += 1
            elif c == 2:
                product_name2 = p[2].text.replace("\n","")
                AER = re.search(r'\d+\.\d+% AER',p[3].text).group().rstrip("AER")
                interest = re.search(r'\d\.\d+%$', p[3].text).group()
                if "£" in p[4].text:
                    MIN = p[4].text.replace("\n","")
                    data.append(([product_name, AER, interest, None, MIN, bank_type]))
                    data.append(([product_name2, AER, interest, None, MIN, bank_type]))
                else:
                    MIN = re.search(r'£\d+',p[8].text).group()
                    AER2 = re.search(r'\d+\.\d+% AER',p[6].text).group().rstrip("AER")
                    interest2 =  re.search(r'\d\.\d+%$', p[6].text).group()
                    data.append(([product_name,AER,interest, None, MIN, bank_type]))
                    data.append(([product_name2,AER2,interest2, None, MIN, bank_type]))

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
                data.append([product_name, AER1, interest1, Balance1, MIN,'Savings'])
                data.append([product_name, AER2, interest2, Balance2, MIN,'Savings'])
                data.append([product_name, AER3, interest3, Balance3, MIN,'Savings'])
                c += 1
            elif c == 2:
                interest = AER = re.search(r'\d\.\d+%',p[1].text).group()
                Balance = p[2].text.strip("(").strip(")2")
                MIN = p[3].text.strip("2")
                data.append([product_name, AER, interest, Balance, MIN,'Savings'])
                c += 1
            elif c == 3:
                product_name1 = product_name + " "+p[2].text
                interest = AER = re.search(r'\d.\d+%',p[3].text).group()
                Balance = p[4].text.lstrip("(").rstrip(")2")
                MIN = p[5].text.strip("2")
                data.append([product_name1, AER, interest, Balance, MIN,'Savings'])
                c += 1
            elif c == 4:
                product_name1 = product_name +' '+ p[2].text
                AER = re.search(r'\d+\.\d+% AER', p[3].text).group().rstrip("AER")
                interest = re.search(r'\d\.\d+% variable', p[3].text).group().strip("variable")
                data.append([product_name1, AER, interest, None, None,'Savings'])
                c += 1
