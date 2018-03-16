from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import  BeautifulSoup as bs
import numpy as np
import pandas as pd
import time
import warnings
import datetime
import os
import glob
from maks_lib import output_path
import re

now = datetime.datetime.now()

warnings.simplefilter(action='ignore')


class Hailfax:
    def __init__(self, url, pvalue, dvalue, term):
        self.url = url
        self.pvalue = pvalue
        self.dvalue = dvalue
        self.term = term

    def start_driver(self):
        self.driver = webdriver.Firefox(executable_path=r'C:\ProgramData\Anaconda3\Scripts\geckodriver.exe')
        self.driver.maximize_window()

    def close_driver(self):
        return self.driver.close()

    def get_url(self):
        self.driver.get(self.url)

    def fillform(self):
        time.sleep(6)
        no_button_xpath = "/html/body/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/form/div/div[1]/div/div[1]/div[1]/fieldset/div[2]/div[1]/label[2]/span"
        no_button = self.driver.find_element_by_xpath(no_button_xpath)
        no_button.click()
        select = Select(self.driver.find_element_by_id('goal'))
        select.select_by_value('1')
        unhind_xpath = "/html/body/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/form/div/div[1]/div/div[2]/div[2]/div[1]/span"
        unhind = self.driver.find_element_by_xpath(unhind_xpath)
        unhind.click()
        self.driver.find_element_by_name("valueOfprop").send_keys(self.pvalue[1])
        self.driver.find_element_by_name("depositAmount").send_keys(self.dvalue[1])
        Select(self.driver.find_element_by_class_name("mortgage-term-available")).select_by_visible_text(self.term)
        time.sleep(5)
        button = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/form/div/div[3]/div/div[3]/div[2]/a")
        button.click()
        time.sleep(10)
        # Select(self.driver.find_element_by_xpath('//*[@id="sort-results"]')).select_by_visible_text("Rate")


    def get_current_url(self):
        return self.driver.current_url

    def save_page(self):
        page = self.driver.page_source
        with open("hailfax_mortgage_"+self.dvalue[1]+"_"+self.term+".html", 'w')as file:
            file.write(page)

class ExtractInfo:

    def __init__(self, page,tab, term, pvalue, dvalue):
        self.page = page
        self.tab = tab
        self.term = term
        self.pvalue = pvalue
        self.dvalue = dvalue

    def findtables_tab1(self):
        soup = bs(self.page, "html.parser")
        file = open("test.txt",'a')
        for j in soup.find_all('div', {'class':["heading","rate"]}):
            text = re.findall(r'^[0-9].*%',j.text)
            if text:
                text = text[0]
                f_term = re.search(r'\d{1,}', text).group()
                interest_type = re.search(r'[A-Z]\w{3,}', text).group()
                t_in = text+","+f_term +","+interest_type
                file.write(t_in)
            rate = re.findall(r'[0-9].[0-9]{2,3}%',j.text)
            if rate:
                mortgage_loan = str(int(self.pvalue[1]) - int(self.dvalue[1]))
                rate = ","+rate[0]+","+rate[1] +","+self.term +","+mortgage_loan+'\n'
                file.write(rate)

        file.close()
        time.sleep(3)


def removeexistingfile():
    tfile = "test.txt"
    if os.path.exists(tfile):
        os.remove(tfile)
    time.sleep(1)
def removehtml():
    htmls = glob.glob("hailfax_*.html")
    for html in htmls:
        os.remove(html)



def pandaper():
    dataset = pd.read_table('test.txt',sep=',',delimiter=None, header=None)
    dataset.columns = ['Bank_Product_Name', 'Fixed_Rate_Term', 'Interest_Type', "Interest", "APRC", "Term (Y)",
                       'Mortgage_Loan_Amt']
    print(dataset)
    dataset['Date'] = now.strftime("%Y-%m-%d")
    dataset['Bank_Native_Country'] = "UK"
    dataset['State'] = "London"
    dataset['Bank_Name'] = "Halifax Bank"
    dataset['Bank_Local_Currency'] = "GBP"
    dataset['Bank_Type'] = "Bank"
    dataset['Bank_Product'] ='Mortgages'
    dataset['Bank_Product_Type'] = "Mortgages"
    dataset['Min_Loan_Amount'] = np.nan
    dataset['Bank_Offer_Feature'] = "Offline"
    dataset['Mortgage_Down_Payment'] = "20%"
    dataset['Mortgage_Category'] = "New Purchase"
    dataset['Mortgage_Reason'] = "Primary Residence"
    dataset['Mortgage_Pymt_Mode'] = "Principal + Interest"
    dataset['Bank_Product_Code'] = np.nan
    columns = ['Date','Bank_Native_Country','State','Bank_Name','Bank_Local_Currency','Bank_Type','Bank_Product',
               'Bank_Product_Type','Bank_Product_Name','Min_Loan_Amount','Bank_Offer_Feature','Term (Y)','Interest_Type',
               'Interest','APRC','Mortgage_Loan_Amt','Mortgage_Down_Payment','Mortgage_Category','Mortgage_Reason',
               'Mortgage_Pymt_Mode','Fixed_Rate_Term','Bank_Product_Code'
               ]
    df = dataset.reindex(columns=columns)
    df.to_csv(output_path + "Consolidate_Halifax_Data_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)

if __name__ == "__main__":
    print("Scraping inprogress ...")
    property_values = [('case1','90000'),('case2','270000'),('case3','450000')]
    deposite_values = [('case1','18000'),('case2','54000'),('case3','90000')]
    url = "https://www.halifax.co.uk/mortgages/mortgage-calculator/calculator/"
    for i in range(len(property_values)):
        for term in ["10","15","25","30"]:
            obj = Hailfax(url, property_values[i], deposite_values[i], term)
            obj.start_driver()
            obj.get_url()
            obj.fillform()
            obj.save_page()
            obj.close_driver()

    removeexistingfile()
    tab1 = ['heading','rate']
    for i in range(len(property_values)):
        for term in ["10","15","25","30"]:
            #wpage = open("hailfax_mortgage_"+deposite_values[i][1]+"_"+term+".html",'r')
            with open("hailfax_mortgage_"+deposite_values[i][1]+"_"+term+".html",'r') as wpage:
                extract = ExtractInfo(wpage, tab1, term, property_values[i], deposite_values[i])
                extract.findtables_tab1()
    pandaper()
    removehtml()
    print("\n Finished !! ")
