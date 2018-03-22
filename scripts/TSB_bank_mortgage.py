from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
table = []
import datetime
import re
from maks_lib import output_path
today = datetime.datetime.now()
path = output_path+"Consolidate_TSB_Data_Mortgage_"+str(today.strftime('%Y_%m_%d'))+'.csv'

table_headers = ['Bank_Product_Name', 'Mortgage_Down_Payment', 'Interest', 'APRC', 'Fixed_Rate_Term', 'Interest_Type','Term (Y)','Mortgage_Loan_Amt']
from tabulate import tabulate
browser = webdriver.Firefox()#replace with .Chrome(), or with the browser of your choice
browser.maximize_window()

url = "https://www2.tsb.co.uk/mortgages/calculator/"
browser.get(url) #navigate to the page
browser.get(url) #navigate to the page
cases = [[90000,18000],[270000,54000], [450000,90000]]
terms = [10,15,20,30]
for case in cases:
    terms = [10,15,25,30]
    for term in terms:
        try:
            browser.get(url)  # navigate to the page
            # term = 9
            browser.find_element_by_css_selector("a.calculator-button:nth-child(3)").click()
            browser.find_element_by_css_selector(".stacked-buttons > label:nth-child(1)").click()
            # browser.find_element_by_css_selector(".mortgage-details > div:nth-child(1) > span:nth-child(2) > input:nth-child(1)").clear()
            browser.find_element_by_css_selector(".mortgage-details > div:nth-child(1) > span:nth-child(2) > input:nth-child(1)").send_keys(case[0])
            browser.find_element_by_tag_name('body').click()
            # browser.find_element_by_css_selector(".mortgage-details > div:nth-child(2) > span:nth-child(2) > input:nth-child(1)").clear()
            browser.find_element_by_xpath('/html/body/form/section/div/div/div[1]/ul/li[2]/div/div/div/div/div/section/div[7]/div[1]/div[2]/span/input').send_keys(case[1])

            browser.find_element_by_css_selector(".mortgage-details > div:nth-child(3) > div:nth-child(2) > div:nth-child(2)").click()


            # browser.find_element_by_css_selector(".hover").click()
            # element_to_hover_over = browser.find_element_by_css_selector("#content > section > div.card.mortgage-figures.current-card > div.mortgage-details > div:nth-child(3) > div.fancy-select > ul > li:nth-child(19)")
            browser.find_element_by_xpath('//*[@id="content"]/section/div[7]/div[1]/div[3]/div[2]/ul/li['+str(term-1)+']').click()
            # element_to_hover_over = firefox.find_element_by_id("baz")
            # hover = ActionChains(browser).move_to_element(element_to_hover_over)
            # hover.click()
            #
            browser.find_element_by_tag_name('body').click()

            browser.find_element_by_xpath('//*[@id="content"]/section/div[7]/div[2]/button').click()
            time.sleep(5)
            page = browser.page_source
            # print(page)
            page = BeautifulSoup(page)
            trs = page.find('div', attrs={"class":"calculator-results"}).find('tbody').find_all('tr')
            for tr in trs:
                # print('-'.center(100,'-'))
                tds = tr.find_all('td')
                data = [td.text  for td in tds]
                name = data[0]
                try:
                    testAmount = int(re.sub('[^0-9]','',data[1]))
                    print('testAmount==',testAmount)
                    if testAmount!=0:
                        name = name+' With Fee'
                except Exception as e:
                    print(e)
                table.append([name, np.nan, re.findall('\d.*%',data[3].strip())[0], re.findall('\d.*%',data[6].strip())[0], 'Fixed_Rate_Term', 'Interest_Type',term,case[0]-case[1]])
        except Exception as e:
            print(e)


print(tabulate(table))
df = pd.DataFrame(table, columns=table_headers)
df["Date"] = today.strftime('%m-%d-%Y')
df["Bank_Native_Country"] = "UK"
df["State"] = "London"
df["Bank_Name"] = "TSB"
df["Bank_Local_Currency"] = "GBP"
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Bank_Offer_Feature"] = "Offline"
df["Mortgage_Category"] = "New Purchase"
df["Mortgage_Reason"] = "Primary Residence"
df["Mortgage_Pymt_Mode"] = "Principal + Interest"
df["Bank_Product_Code"] = np.nan
df['Min_Loan_Amount'] = np.nan
df['Mortgage_Down_Payment'] = '20%'
df['Fixed_Rate_Term'] = df['Bank_Product_Name'].apply(lambda x: re.sub('[^0-9]','',re.findall('\d.*Yea',x, re.IGNORECASE)[0]) if len(re.findall('\d.*Yea',x,re.IGNORECASE))>=1 else None)
df['Interest_Type'] = df['Bank_Product_Name'].apply(lambda x: "Fixed" if 'fixed' in x.lower() else 'Variable')
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Bank_Product_Code"]
df = df[order]
df.to_csv(path, index=False)
browser.close()