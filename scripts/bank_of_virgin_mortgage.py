import requests
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import  tabulate
from datetime import datetime
today = datetime.now()
import re
from maks_lib import output_path
path = output_path+"Consolidate_Virgin_Data_Mortgage_"+str(today.strftime('%m_%d_%Y'))+'.csv'
table = []
# term = "25"
# property_value = "90000"
# deposit = "18000"
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency",
         "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name",
         "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type",
         "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category",
         "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Bank_Product_Code"]
table_headers = ["Bank_Product_Name", "Min_Loan_Amount", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Fixed_Rate_Term"]
table.append(table_headers)


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
           }
def virgin_mortgage(property_value, deposit, term):
    data = {"filterstep": "true",
            "next": "Next",
            "FilterModel.Deposit": deposit,
            "FilterModel.PropertyValue": property_value,
            "FilterModel.RepaymentTerm": term,
            "FilterModel.RepaymentMethod": "Repayment",
            "FilterModel.ProductFees": "both",
            "FilterModel.CashbackProducts": "both",
            "FilterModel.BuyerType": "firsttimebuyer",
            "FilterModel.ShowHelp": "True",
            "FilterModel.SaveStep": "0",
            "products_found_count": "0",
            "next": "Update%20results"
            }
    resp = requests.post("https://uk.virginmoney.com/mortgages/find-a-mortgage/firsttimebuyer/", data=data, headers = headers)
    # print(resp.content)
    jsoup = BeautifulSoup(resp.content,"lxml")
    panel = famResultsPanel = jsoup.find("div", attrs={"id":"famResultsPanel"})
    form_table = panel.find("form", attrs={"id":"mortgageform"})
    tbodys = form_table.find_all("tbody", attrs={"class":"table--fam-results fam__product"})
    for tbody in tbodys:
        tds = tbody.find_all("td")
        Bank_Product_Name = (tds[0].text)
        Fixed_Rate_Term = (tds[2].text)
        interest_rate = (tds[3].text).split("%")[0]
        aprc = (tds[5].text)
        years = re.findall('\d.*year', Fixed_Rate_Term)
        if len(years)>=1:
            years = re.sub('[^0-9.]','',years[0])
        else:
            years = None
        if "fixed" in Bank_Product_Name.lower():
            Interest_Type = "Fixed"
        else:
            Interest_Type = "Variable"
        a = [Bank_Product_Name.strip('\n'), None, term, Interest_Type, interest_rate, aprc, int(deposit)-int(term),years]
        table.append(a)
    # break
terms = ["10","15","25","30"]
case = [["90000", "18000"], ["270000", "54000"],["450000","90000"]]
for term in terms:
    for ca in case:
        virgin_mortgage(ca[0],ca[1],term)
print(tabulate(table))

df = pd.DataFrame(table[1:], columns=table_headers)
df["Date"] = today.strftime('%m-%d-%Y')
df["Bank_Native_Country"] = "UK"
df["State"] = "London"
df["Bank_Name"] = "Virgin Money Plc."
df["Bank_Local_Currency"] = "GBP"
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Bank_Offer_Feature"] = "Offline"
df["Mortgage_Down_Payment"] = "20%"
df["Mortgage_Category"] = "New Purchase"
df["Mortgage_Reason"] = "Primary Residence"
df["Mortgage_Pymt_Mode"] = "Principle + Interest"
df["Bank_Product_Code"] = None
df = df[order]
df.to_csv(path, index=False)
print(df)