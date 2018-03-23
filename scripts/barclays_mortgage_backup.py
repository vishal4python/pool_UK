import time
import datetime
from selenium import webdriver
import os
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import re
import numpy as np
from maks_lib import output_path
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException

now = datetime.datetime.now()
table = []
table_headers = ["Bank_Product_Name", "Fixed_Rate_Term","APRC", "Interest","Min_Loan_Amount","Mortgage_Loan_Amt","Term (Y)"]
# table.append(table_headers)
print("Scrapping is in-progress..")
browser = webdriver.Firefox()

file = open("test.txt",'w',encoding="UTF-8")

def filform(properties, deposit, year):
    xpath = '//*[@id="mortgage-calculator-component"]/div/div[5]/form/div[2]/div/fieldset/div/div/div/div/select'
    Select(browser.find_element_by_xpath(xpath)).select_by_value("FTBP")

    time.sleep(1)
    pxpath = "//*[@id='mortgage-calculator-component']/div/div[5]/form/div[3]/div/fieldset/div/div/div/input"
    browser.find_element_by_xpath(pxpath).clear()
    browser.find_element_by_xpath(pxpath).send_keys(properties)
    #browser.find_element_by_xpath(pxpath).send_keys("90000")

    repay = "//*[@id='mortgage-calculator-component']/div/div[5]/form/div[4]/div/fieldset/div/div/div/div/select"
    Select(browser.find_element_by_xpath(repay)).select_by_value("repayment")

    dxpath = "//*[@id='mortgage-calculator-component']/div/div[5]/form/div[8]/div/fieldset/div/div/div/input"
    browser.find_element_by_xpath(dxpath).clear()
    browser.find_element_by_xpath(dxpath).send_keys(deposit)
    #browser.find_element_by_xpath(dxpath).send_keys("72000")

    yxpath = "//*[@id='mortgage-calculator-component']/div/div[5]/form/div[11]/div/fieldset/div/div/div/div[1]/div/div/select"
    Select(browser.find_element_by_xpath(yxpath)).select_by_value(str(year))
    #Select(browser.find_element_by_xpath(yxpath)).select_by_value("10")
    time.sleep(2)
    browser.find_element_by_css_selector("#mortgage-calculator-component > div > div.mCalc-module.mCalc-Cost > form > div:nth-child(12) > div > ul > li > button").click()

def barclays(properties, deposit, year):
    browser.get("https://www.barclays.co.uk/mortgages/mortgage-calculator/#/cost")
    browser.refresh()

    time.sleep(10)

    try:
        filform(properties, deposit, year)

    except ElementClickInterceptedException:
        #print("Error",e)
        try:
            #alert = browser.switch_to_alert()
            browser.find_element_by_xpath("/html/body/div[14]/div/div[1]/div/a[1]").click()
            time.sleep(1)
            filform(properties, deposit, year)
        except Exception as e:
            filform(properties, deposit, year)
            print("Error",e)
    time.sleep(15)
    # print(browser.page_source)

    jsoup = BeautifulSoup(browser.page_source,"html.parser")

    result = jsoup.find("table", attrs={"class": "table table-mortgage display responsive nowrap dataTable dtr-column collapsed"})
    #print(result)
    # print("---------------------------")
    if result is not None:
        trs = result.find_all('tr')
        for tr in trs:
            if tr is not None:
                tds = tr.find_all("td")
                for td in tds:
                    product_name = re.search(r'(\d .*Fixed|\d .*Tracker)', td.text)
                    if product_name is not None:
                        Bank_product_name = product_name.group()
                        fixed_rate = re.search(r'\d ', Bank_product_name).group()
                        Interest_type =  re.search(r'(Fixed|Tracker)', Bank_product_name).group()
                        if "Fixed" in Interest_type:
                            Interest_Type = "Fixed"
                        if "Tracker" in Interest_type:
                            Interest_Type = "Variable"
                        file.write((Bank_product_name+","+fixed_rate+","))
                    APRC = re.search(r'\d\.\d+%.*', td.text)
                    if APRC is not None:
                        APRC = APRC.group()
                        if len(APRC) < 6:
                            APRC = APRC
                            file.write(APRC+",")
                        if "until" in APRC or 'BBBR' in APRC:
                            interest = re.search(r'\d\.\d{1,}%', APRC).group()
                            file.write(interest+",")
                    if "Min loan" in td.text:

                        ltv = re.search(r"\d+%",td.text).group()
                        print(ltv)
                        max_loan = re.search(r'(Max loan) (.*\d)', td.text).groups()[1]
                        min_loan = re.search(r'\d,\d+', td.text).group()
                        min_loan = min_loan.replace(",","")
                        #print(min_loan,"--------------------------------------")
                        file.write(min_loan+","+str(deposit)+","+str(year)+","+ltv+"\n")
def panda():
    dataset = pd.read_table('test.txt', sep=',', delimiter=None, header=None)
    #dataset.columns = ['Bank_Product_Name', 'Fixed_Rate_Term', 'Interest_Type', "Interest", "APRC", "Term (Y)", 'Mortgage_Loan_Amt']
    dataset.columns = ["Bank_Product_Name", "Fixed_Rate_Term","APRC", "Interest","Min_Loan_Amount","Mortgage_Loan_Amt","Term (Y)","ltv"]
    dataset['Date'] = now.strftime("%Y-%m-%d")
    dataset['Bank_Native_Country'] = "UK"
    dataset['State'] = "London"
    dataset['Bank_Name'] = "Barclays"
    dataset['Bank_Local_Currency'] = "GBP"
    dataset['Bank_Type'] = "Bank"
    dataset['Bank_Product'] = 'Mortgages'
    dataset['Bank_Product_Type'] = "Mortgages"
    dataset['Bank_Offer_Feature'] = "Offline"
    dataset['Mortgage_Down_Payment'] = "20%"
    dataset['Mortgage_Category'] = "New Purchase"
    dataset['Mortgage_Reason'] = "Primary Residence"
    dataset['Mortgage_Pymt_Mode'] = "Principal + Interest"
    dataset['Bank_Product_Code'] = np.nan
    dataset["Interest_Type"] = "Variable"
    dataset['APRC'] = dataset["APRC"].str.split("%")[0]
    columns = ['Date', 'Bank_Native_Country', 'State', 'Bank_Name', 'Bank_Local_Currency', 'Bank_Type', 'Bank_Product',
               'Bank_Product_Type', 'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature', 'Term (Y)',
               'Interest_Type', 'Interest', 'APRC', 'Mortgage_Loan_Amt', 'Mortgage_Down_Payment', 'Mortgage_Category', 'Mortgage_Reason',
               'Mortgage_Pymt_Mode', 'Fixed_Rate_Term', 'Bank_Product_Code',"ltv"
               ]
    df = dataset.reindex(columns=columns)
    df.to_csv(output_path + "Consolidate_Barclays_Data_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)

terms = [10, 15, 20, 30]
cases = [[90000, 72000], [270000, 216000], [450000, 360000]]
barclays(90000, 72000, 10)
# for term in terms:
#     for case in cases:
#         #print(case[0], case[1], term)
#         barclays(case[0], case[1], term)

file.close()
browser.close()
panda()
#os.remove("test.txt")
print("Scrapping Finished !!!")
