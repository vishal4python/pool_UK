'''
Created on 14-Mar-2018

@author: sairam
'''
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from maks_lib import output_path
today = datetime.datetime.now()
path = output_path+"Consolidate_RBS_Data_Mortgage_"+str(today.strftime('%Y_%m_%d'))+'.csv'
# path = "Consolidate_RBS_Data_Mortgage_"+str(today.strftime('%Y_%m_%d'))+'.csv'
driver = webdriver.Firefox()
from tabulate import tabulate
table = []
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Bank_Product_Code"]
table_headers = ["Bank_Product_Name", "Min_Loan_Amount", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Fixed_Rate_Term", "Mortgage_Down_Payment"]
driver.get("https://personal.rbs.co.uk/personal/mortgages/mortgage-calculators/mortgagefinder.html")
time.sleep(2)
driver.find_element_by_xpath('/html/body/div[5]/div/a').click()
# driver.find_element_by_css_selector("#mortgageFinder_mortgage-term").send_keys("20")
cases = [[90000,18000],[270000,54000], [450000,90000]]
for case in cases:
    terms = [10,15,20,30]
    for term in terms:
        driver.find_element_by_xpath('//*[@id="mortgageFinder_mortgage-term"]').clear()
        driver.find_element_by_xpath('//*[@id="mortgageFinder_mortgage-term"]').send_keys(term)
        driver.find_element_by_name("PropertyValue").clear()
        driver.find_element_by_name("PropertyValue").send_keys(case[0])
        # time.sleep(2)
        driver.find_element_by_name("depositWorth").clear()
        driver.find_element_by_name("depositWorth").send_keys(case[1])
        time.sleep(2)
        driver.find_element_by_tag_name("body").click()
        # driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[3]/div/div/form/div/fieldset/div[1]/div[3]/div/div[11]/div/span/a').click()
        driver.find_element_by_css_selector(".js-cta-button > a:nth-child(1)").click()
        time.sleep(5)
        # print(driver.page_source)
        jsoup = BeautifulSoup(driver.page_source,"lxml")

        # driver.close()

        result_table = jsoup.find("div", attrs={"class":"js-mortgage-result mortgage-result "})
        # print(table)
        trs = result_table.find_all("div", attrs={"class":re.compile('row')})
        for tr in trs:
            try:
                # print(tr)
                Bank_Product_Name = tr.find("td", attrs={"class":"desk--one-fifth"}).text
                # print(Bank_Product_Name)

                Interest = tr.find("td", attrs={"class":"desk--one-tenth"}).text
                # print(Interest)

                ltv = tr.find("td", attrs={"class":"desk--one-twelfth highlight"}).text
                # print(ltv)
                Min_Loan_Amount = tr.find_all("div", attrs={"class":"desk--one-whole mortgage-detail--row"})[6].find("div", attrs={"class":"desk--three-fifths mortgage-detail--value"}).text
                # Min_Loan_Amount = tr.find("div", attrs={"class":"desk--three-fifths mortgage-detail--value"}).text
                # print(Min_Loan_Amount)
                frt = re.findall("\d.*year", Bank_Product_Name.lower())
                if len(frt)>=1:
                    frt = re.sub('[^0-9]','',frt[0])
                else:
                    frt = None
                if "fixed" in Bank_Product_Name.lower():
                    Interest_Type = "Fixed"
                else:
                    Interest_Type = "Variable"
                a = [Bank_Product_Name, Min_Loan_Amount, term, Interest_Type, Interest, None, case[0]-case[1], frt, 100-int(re.sub('[^0-9.]','',ltv))]
                table.append(a)
            except:
                pass
    # break

# print(tabulate(table))
df = pd.DataFrame(table, columns=table_headers)
df['Min_Loan_Amount'] = df['Min_Loan_Amount'].apply(lambda x : re.sub('[^0-9.]','',str(x))if len(re.sub('[^0-9.]','',str(x)))!=0 else None) 
df["Date"] = today.strftime('%m-%d-%Y')
df["Bank_Native_Country"] = "UK"
df["State"] = "London"
df["Bank_Name"] = "Royal Bank Of Scotland"
df["Bank_Local_Currency"] = "GBP"
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Bank_Offer_Feature"] = "Offline"
df["Mortgage_Category"] = "New Purchase"
df["Mortgage_Reason"] = "Primary Residence"
df["Mortgage_Pymt_Mode"] = "Principal + Interest"
df["Bank_Product_Code"] = None

df = df[order]
df.to_csv(path, index=False)
driver.close()
print("execution Completed.")
