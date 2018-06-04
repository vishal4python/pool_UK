
import datetime
from tabulate import tabulate
import pandas as pd
import re
import time
import requests
from bs4 import BeautifulSoup
starttime = time.time()
from maks_lib import output_path

now = datetime.datetime.now()
table = []
table_headers = ["Bank_Product_Name", "Min_Loan_Amount", "Term (Y)", "Interest_Type", "Interest", "APRC",
                 "Mortgage_Loan_Amt"]
# table.append(table_headers)



def lloydBank(case_0,case_1, term):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"}
    resp = requests.get('https://www.lloydsbank.com', headers=headers)
    data = {"aprTextValue": "APRC",
            "radioMortgFor": "fstHom",
            "mortgReq": case_0-case_1,
            "valueOfprop": case_0,
            "mortgTermYrs": term,
            "AddlAmt": '0',
            "isCurrentAccountCustomer": "No",
            "additionalBorrowingAmt": '0'}
    resp = requests.post(
        'https://www.lloydsbank.com/asp_includes/mortgages/mortgage-calculator-responsive/calculatorFunctions.asp',
        cookies=resp.cookies,
        data=data,
        )
    result = BeautifulSoup(resp.content, 'html.parser')
    products = result.find_all("div", attrs={"class": "product"})
    print(products)
    for product in products:
        try:
            Bank_Product_Name = product.find("div", attrs={"class": "heading"}).text
            Interest = product.find("div", attrs={"class": "rate"}).text
            APRC = product.find("div", attrs={"class": "cost-comparison"}).text

            Interest = re.findall('\d.\d?\d?\d?%', Interest)
            if len(Interest) >= 1:
                Interest = Interest[0]
            else:
                Interest = None

            APRC = re.findall('\d.*APRC', APRC)

            if len(APRC) >= 1:
                APRC = APRC[0]
                APRC = re.sub('[^0-9.%]', '', APRC)
            else:
                APRC = None

            a = [Bank_Product_Name[:Bank_Product_Name.index('%') + 1], None, term, "Fixed", Interest, APRC,
                 str(int(int(case_0) - int(case_1)))]
            print(a)
            table.append(a)
        except Exception as e:
            print(e)

terms = [10, 15, 20, 25, 30]
cases = [[90000, 18000], [270000, 54000], [450000, 90000]]
for term in terms:
    for case in cases:
        lloydBank(case[0], case[1], term)
        time.sleep(5)

print(tabulate(table))

order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product",
         "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type",
         "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason",
         "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Bank_Product_Code"]
column = ["Bank_Product_Name", "Min_Loan_Amount", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt"]

df = pd.DataFrame(table, columns=column)

df["Date"] = now.strftime('%Y-%m-%d')

df["Bank_Native_Country"] = "UK"
df["State"] = "London"
df["Bank_Name"] = "Lloyds Bank"
df["Bank_Local_Currency"] = "GBP"
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Bank_Offer_Feature"] = "Offline"
df["Mortgage_Down_Payment"] = "20%"
df["Mortgage_Category"] = "New Purchase"
df["Mortgage_Reason"] = "Primary Residence"
df["Mortgage_Pymt_Mode"] = "Principal + Interest"
df["Bank_Product_Code"] = None
df["Fixed_Rate_Term"] = df["Bank_Product_Name"].apply(lambda x: re.match('\d\d?', str(x)).group(0))

print(df)

df = df[order]
df.to_csv(output_path + "Consolidate_Lloyds_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
print('time=', (time.time() - starttime))