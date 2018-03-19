import time
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import re
from maks_lib import output_path
now = datetime.datetime.now()
table = []
table_headers = ["Bank_Product_Name", "Min_Loan_Amount", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt"]
# table.append(table_headers)
browser = webdriver.Firefox()
def lloydBank(properties, deposit,year , elNumber):
    browser.get("https://www.lloydsbank.com/mortgages/mortgage-calculator.asp")
    browser.find_element_by_css_selector("#existing-customer > label:nth-child(4) > span:nth-child(1)").click()
    browser.find_element_by_css_selector("#existing-current-account-customer > label:nth-child(4) > span:nth-child(1)").click()
    
    
    browser.find_element_by_css_selector("#goal").click()
    browser.find_element_by_css_selector("#goal > option:nth-child(2)").click()
    
    browser.find_element_by_tag_name("body").click()
    
    browser.find_element_by_css_selector("#costaccordionAccordionButton").click()
    
    browser.find_element_by_css_selector("#valueOfprop").clear()
    browser.find_element_by_css_selector("#valueOfprop").send_keys(properties)
    
    browser.find_element_by_css_selector("#depositAmount").clear()
    browser.find_element_by_css_selector("#depositAmount").send_keys(deposit)
    
    browser.find_element_by_css_selector(".mortgage-term-available").click()
    
    browser.find_element_by_css_selector(".mortgage-term-available > option:nth-child("+str(elNumber)+")").click()
    
    browser.find_element_by_css_selector("a.button:nth-child(7)").click()
    
    time.sleep(5)
#     print(browser.page_source)
    
    jsoup = BeautifulSoup(browser.page_source)
    
    
    result = jsoup.find("div", attrs={"class":"result"})
    products = result.find_all("div", attrs={"class":"product"})
    for product in products:
        try:
            Bank_Product_Name =product.find("div", attrs={"class":"heading"}).text
            Interest = product.find("div", attrs={"class":"rate"}).text
            APRC = product.find("div", attrs={"class":"cost-comparison"}).text
            
            
            Interest = re.findall('\d.\d?\d?\d?%',Interest)
            if len(Interest)>=1:
                Interest = Interest[0]
            else:
                Interest = None
            
            APRC= re.findall('\d.*APRC',APRC)

            if len(APRC)>=1:
                APRC = APRC[0]
                APRC = re.sub('[^0-9.%]', '', APRC)
            else:
                APRC= None
            
            a = [Bank_Product_Name[:Bank_Product_Name.index('%')+1], None, year, "Fixed", Interest, APRC, str(int(properties-deposit))]
            table.append(a)
        except Exception as e:
            print(e)
    
terms = [[10,11],[15,16],[20,21],[25,26],[30,31]]
cases = [[90000,18000], [270000, 54000], [450000, 90000]]
for term in terms:
    for case in cases:
        lloydBank(case[0], case[1], term[0], term[1])

browser.close()
print(tabulate(table))

order= ["Date","Bank_Native_Country","State","Bank_Name","Bank_Local_Currency","Bank_Type","Bank_Product","Bank_Product_Type","Bank_Product_Name","Min_Loan_Amount","Bank_Offer_Feature","Term (Y)","Interest_Type","Interest","APRC","Mortgage_Loan_Amt","Mortgage_Down_Payment","Mortgage_Category","Mortgage_Reason","Mortgage_Pymt_Mode","Fixed_Rate_Term","Bank_Product_Code"]
column = ["Bank_Product_Name","Min_Loan_Amount","Term (Y)","Interest_Type","Interest","APRC","Mortgage_Loan_Amt"]

df = pd.DataFrame(table ,columns=column)

df["Date"] = now.strftime('%Y-%m-%d')

df["Bank_Native_Country"] = "UK"
df["State"] = "London"
df["Bank_Name"] = "Lloyds Bank"
df["Bank_Local_Currency"] = "GBP"
df["Bank_Type"]= "Bank"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Bank_Offer_Feature"] = "Offline"
df["Mortgage_Down_Payment"] = "20%"
df["Mortgage_Category"] = "New Purchase"
df["Mortgage_Reason"] = "Primary Residence"
df["Mortgage_Pymt_Mode"] = "Principal + Interest"
df["Bank_Product_Code"] = None
df["Fixed_Rate_Term"] = df["Bank_Product_Name"].apply(lambda x : re.match('\d\d?', str(x)).group(0))

print(df)

df = df[order]
df.to_csv(output_path + "Consolidate_Lloyds_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
