from selenium import webdriver
import time
from tabulate import tabulate
import json
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import requests
import datetime
from maks_lib import output_path
today  = datetime.datetime.now()
startTime = time.time()
path = output_path+"Consolidate_MoneySuperMarket_Data_Mortgage_"+str(today.strftime('%Y_%m_%d'))+'.csv'
today = datetime.datetime.now()
browser = webdriver.Firefox()
browser.maximize_window()
Excel_Table = []
neededUkBanks = {'royal bank of scotland':'Royal Bank Of Scotland',
                 'natwest':'NatWest',
                 'lloyds bank':'Lloyds Bank',
                 'lloyds':'Lloyds Bank',
                 'hsbc':'HSBC',
                 'tsb':'TSB',
                 'barclays':'Barclays',
                 'bank of ireland':'Bank of Ireland',
                 'bank of ireland uk':'Bank of Ireland',
                 'metro bank':'Metro Bank',
                 'bank of scotland':'Bank of Scotland',
                 'the co-operative bank':'The Co-operative Bank',
                 'cooperative bank':'The Co-operative Bank',
                 'halifax':'Halifax',
                 'santander Bank':'Santander Bank',
                 'santander':'Santander Bank',
                 'clydesdale bank':'Clydesdale Bank',
                 'clydesdale':'Clydesdale Bank',
                 'virgin money plc.':'Virgin Money Plc.',
                 'virgin money':'Virgin Money Plc.'
                 }

table_headers = ['Bank_Name', 'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature', 'Term (Y)', 'Interest_Type', 'Interest', 'APRC', 'Mortgage_Loan_Amt', 'Mortgage_Down_Payment', 'Fixed_Rate_Term']
# Excel_Table.append(table_headers)


cases = [[90000, 72000], [270000, 216000], [450000, 360000]]
terms = [10, 15, 25, 30]

#A method for getting all pages data
def pageData(pageId,start_page, pages,case):
    for i in range(start_page, pages):
        try:
            #API for getting all pages data
            page = "https://www.moneysupermarket.com/bin/services/aggregation?channelId=55&enquiryId=" + pageId + "&limit=20&offset=" + str(20 * i) + "&sort=initialMonthlyPayment"
            # browser.get(page)
            # soup = BeautifulSoup(browser.page_source,'lxml')
            # #Converting text into json format
            # dict_from_json = json.loads(soup.find("body").text)
            dict_from_json = requests.get(page).json()
            for Bank in dict_from_json['results']:
                # print(Bank)
                Bank_Name = Bank['brandName']
                Interest = Bank['quote']['initialRate']
                Year = Bank['quote']['paymentSteps'][0]['numberOfPayments']
                if Year!=0 or Year is not None:
                    Year = int(Year/12)
                Balance = str(int(Bank['quote']['minBorrowingAmount'])) #+ '-' + str(int(Bank['quote']['maxBorrowingAmount']))
                LTV = Bank['quote']['maxRMTGSLTV']
                if LTV == 0:
                    LTV = Bank['quote'].get('maxFTBLTV') if Bank['quote'].get('maxFTBLTV') is not None else 0

                APRC = Bank['quote']['aprc']
                if int(LTV) == 80:
                    for k in neededUkBanks:
                        if Bank_Name is not  None:
                            if k in Bank_Name.lower().strip():
                                if Bank['strapline'] is None:
                                    a = [neededUkBanks[k], str(Year)+ 'Year Fixed', Balance, 'Offline', term, 'Fixed', str(Interest)+'%', str(APRC)+'%',
                                         case[1], 100-int(LTV), Year]
                                    Excel_Table.append(a) #Appending data to table for making csv file
                                    break

            Result = dict_from_json['totalResults']
            print("Result=", Result, "No of offset", int(Result / 20)+1, 'page : ',i, 'pageId : ',pageId)
        except Exception as p:
            print(p)
    return int(Result / 20) + 1

for case in cases:
    for term in terms:
        try:
            print(str(str(case)+' Term '+str(term)).center(100,'-'))
            browser.get('https://www.moneysupermarket.com/mortgages/results/#?borrow='+str(case[1])+'&page=1&term='+str(term)+'&goal=1&property='+str(case[0]))
            time.sleep(5)
            page = browser.page_source
            page = page[page.index('enquiryId=')+len('enquiryId='):]
            pageId = page[:page.index('&')]
            print(pageId)
            pages = pageData(pageId,0,2,case)
            print('No of Pages:',pages)
            pageData(pageId, 1, pages,case)
        except Exception as p:
            print(p)

print(tabulate(Excel_Table))

df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type']= 'Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Product_Code'] = None
df['Ticker'] = None
df['Mortgage_Category'] = 'New Purchase'
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Source'] = 'moneysupermarket.com'
order = ["Date", "Bank_Native_Country", "State", "Bank_Name","Ticker", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APRC", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Fixed_Rate_Term", "Source"]
df = df[order]
browser.close()
df.to_csv(path, index=False)

print('Execution completed in {time.time()-startTime} seconds')
