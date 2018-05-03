from selenium import webdriver
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
from selenium.webdriver.firefox.options import Options
import datetime
today = datetime.datetime.now()
Excel_data= []
from maks_lib import output_path
start_time = time.time()
path = output_path+'Consolidate_SantanderBank_Data_Mortgage_'+today.strftime('%m_%d_%Y')+'.csv'
table_headers = ["Bank_Product_name", "Interest", "APRC", "Mortgage_Down_Payment", "Term (Y)", "Mortgage_Loan_Amt"]
# Excel_data.append(table_headers)
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)#firefox_options=options
driver.maximize_window()
print('Browser Loaded')
print('Please wait scraping is runnning...')
cases = [[90000,18000], [270000,54000], [450000,90000]]

terms = [[10,6], [15,11], [25,21],[30,26]]
for case in cases:
    for term in terms:
        try:
            driver.get('https://www.santander.co.uk/info/mortgages/compare-our-mortgages')
            driver.find_element_by_xpath('//*[@id="borrow-compmortgage"]/div/div[1]/div[2]/label').click()
            driver.find_element_by_xpath('//*[@id="borrow-compmortgage"]/div/div[1]/div[2]/label/a').click()
            driver.find_element_by_xpath('//*[@id="btype"]/option[3]').click()
            driver.find_element_by_xpath('//*[@id="field-property"]').clear()
            driver.find_element_by_xpath('//*[@id="field-property"]').send_keys(case[0])
            driver.find_element_by_xpath('//*[@id="field-borrow"]').clear()
            driver.find_element_by_xpath('//*[@id="field-borrow"]').send_keys(case[0]-case[1])
            driver.find_element_by_xpath('//*[@id="mortgage-years"]/option['+str(term[1])+']').click()
            driver.find_element_by_xpath('//*[@id="borrow-compmortgage"]/div/div[2]/div[1]/div/div[2]/a').click()
            try:
                driver.find_element_by_xpath('//*[@id="borrow-compmortgage"]/div/div[2]/div[2]/div[2]/a').click()
            except Exception as e:
                print(e)

            table = BeautifulSoup(driver.page_source).find('table', attrs={'class':'mortgages-table'})
            if table is not None:
                for tr in table.find('tbody').find_all('tr', attrs={'class':re.compile('r eligible')}):
                    try:
                        product_name = tr.find('th').text
                        tds = tr.find_all('td')
                        Mortgage_Down_Payment = tds[0].text
                        Interest = tds[1].text
                        APRC = tds[4].text
                        withFee = re.search('[1-9]', tds[5].text if tds[5] is not None else '')
                        if withFee is not None:
                            product_name = product_name+' With Fee'
                        if '85' in Mortgage_Down_Payment:
                            Mortgage_Down_Payment = '15%'
                            a = [product_name, Interest, APRC, Mortgage_Down_Payment, term[0], case[0]-case[1]]
                            Excel_data.append(a)
                            print(a)
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
def getYear(x):
    if x is not  None:
        if 'tracker' in x.lower():
            return None
        x = re.search('\d.*year',x,re.IGNORECASE)
        if x is not None:
            return re.sub('[^0-9]', '', x.group(0))
        else:
            return  None
    else:
        return None
df = pd.DataFrame(Excel_data, columns=table_headers)
df['Date'] = ''
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'Santander Bank'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Min_Loan_Amount'] = None
df['Bank_Offer_Feature'] = 'Offline'
df['Interest_Type'] = 'Variable'
df['Mortgage_Category'] = 'New Purchase'
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Fixed_Rate_Term'] = df['Bank_Product_name'].apply(getYear)
df['Bank_Product_Code'] = None

order = ["Bank_Product_Type","Bank_Product_name","Min_Loan_Amount","Bank_Offer_Feature","Term (Y)","Interest_Type","Interest","APRC","Mortgage_Loan_Amt","Mortgage_Down_Payment","Mortgage_Category","Mortgage_Reason","Mortgage_Pymt_Mode","Fixed_Rate_Term","Bank_Product_Code"]
df = df[order]
df.to_csv(path, index=False)
print(tabulate(Excel_data))
driver.close()
print('Total Execution Time is ',time.time()-start_time,'Seconds')