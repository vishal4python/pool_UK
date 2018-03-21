import time
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import re
from maks_lib import output_path
from selenium.webdriver.support.ui import Select

now = datetime.datetime.now()
table = []
table_headers = ["Bank_Product_Name", "Min_Loan_Amount", "Term (Y)", "Interest_Type", "Interest", "APRC",
                 "Mortgage_Loan_Amt"]
# table.append(table_headers)
browser = webdriver.Chrome()


def barclays(properties, deposit, year):
    browser.get("https://www.barclays.co.uk/mortgages/mortgage-calculator/#/cost")

    time.sleep(5)
    a = Select(browser.find_element_by_xpath('//*[@id="mortgage-calculator-component"]/div/div[5]/form/div[2]/div/fieldset/div/div/div/div/select'))
    a.select_by_value("FTBP")
    time.sleep(1)
    browser.find_element_by_xpath("//*[@id='mortgage-calculator-component']/div/div[5]/form/div[3]/div/fieldset/div/div/div/input").send_keys(90000)

    b = Select(browser.find_element_by_xpath("//*[@id='mortgage-calculator-component']/div/div[5]/form/div[4]/div/fieldset/div/div/div/div/select"))
    b.select_by_value("repayment")

    browser.find_element_by_xpath("//*[@id='mortgage-calculator-component']/div/div[5]/form/div[8]/div/fieldset/div/div/div/input").send_keys(72000)

    c = Select(browser.find_element_by_xpath("//*[@id='mortgage-calculator-component']/div/div[5]/form/div[11]/div/fieldset/div/div/div/div[1]/div/div/select"))
    c.select_by_value("10")

    browser.find_element_by_css_selector("#mortgage-calculator-component > div > div.mCalc-module.mCalc-Cost > form > div:nth-child(12) > div > ul > li > button").click()

    time.sleep(15)
    # print(browser.page_source)

    jsoup = BeautifulSoup(browser.page_source,"html.parser")

    result = jsoup.find("table", attrs={"class": "table table-mortgage display responsive nowrap dataTable dtr-column collapsed"})
    trs = result.find_all('tr')
    for tr in trs:
        if tr is not None:
            tds = tr.find_all("td")
            for td in tds:
                product_name = re.search(r'(.*Fixed|.*Tracker)', td.text)
                if product_name is not None:
                    Bank_product_name = product_name.group()
                    fixed_rate = re.search(r'\d ', Bank_product_name).group()
                APRC = re.search(r'\d\.\d+%.*', td.text)
                if APRC is not None:
                    APRC = APRC.group()
                    if len(APRC) < 6:
                        APRC = APRC
                    if "until" in APRC or 'BBBR' in APRC:
                        interest = re.search(r'\d\.\d{1,}%', APRC).group()
                if "Min loan" in td.text:
                    max_loan = re.search(r'(Max loan) (.*\d)', td.text).groups()[1]
                    min_loan = re.search(r'\d,\d+', td.text).group()


    #         Interest = product.find("div", attrs={"class": "rate"}).text
    #         APRC = product.find("div", attrs={"class": "cost-comparison"}).text
    #
    #         Interest = re.findall('\d.\d?\d?\d?%', Interest)
    #         if len(Interest) >= 1:
    #             Interest = Interest[0]
    #         else:
    #             Interest = None
    #
    #         APRC = re.findall('\d.*APRC', APRC)
    #
    #         if len(APRC) >= 1:
    #             APRC = APRC[0]
    #             APRC = re.sub('[^0-9.%]', '', APRC)
    #         else:
    #             APRC = None
    #
    #         a = [Bank_Product_Name[:Bank_Product_Name.index('%') + 1], None, year, "Fixed", Interest, APRC,
    #              str(int(properties - deposit))]
    #         table.append(a)
        except Exception as e:
            print(e)


terms = [10, 15, 20, 25, 30]
cases = [[90000, 72000], [270000, 216000], [450000, 360000]]
barclays(90000, 72000, 10)
# for term in terms:
#     for case in cases:
#         barclays(case[0], case[1], term)

browser.close()
# print(tabulate(table))
#
# order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product",
#          "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type",
#          "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason",
#          "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Bank_Product_Code"]
# column = ["Bank_Product_Name", "Min_Loan_Amount", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt"]
#
# df = pd.DataFrame(table, columns=column)
#
# df["Date"] = now.strftime('%Y-%m-%d')
#
# df["Bank_Native_Country"] = "UK"
# df["State"] = "London"
# df["Bank_Name"] = "Lloyds Bank"
# df["Bank_Local_Currency"] = "GBP"
# df["Bank_Type"] = "Bank"
# df["Bank_Product"] = "Mortgages"
# df["Bank_Product_Type"] = "Mortgages"
# df["Bank_Offer_Feature"] = "Offline"
# df["Mortgage_Down_Payment"] = "20%"
# df["Mortgage_Category"] = "New Purchase"
# df["Mortgage_Reason"] = "Primary Residence"
# df["Mortgage_Pymt_Mode"] = "Principal + Interest"
# df["Bank_Product_Code"] = None
# df["Fixed_Rate_Term"] = df["Bank_Product_Name"].apply(lambda x: re.match('\d\d?', str(x)).group(0))
#
# print(df)
#
# df = df[order]
# df.to_csv(output_path + "Consolidate_Lloyds_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
