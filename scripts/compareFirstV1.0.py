"""
Purpose     : Extract data from comparefirst
        #####################     Change log   ###############################
        ##------------------------------------------------------------------##
        ##  Author              ##Date                ##Current Version     ##
        ##------------------------------------------------------------------##
        ## Moody's Analytics    ##11th July, 2018     ##V1.0                ##
        ##------------------------------------------------------------------##
        ######################################################################
        Date              Version     Author      Description
        11th July, 2018   v 1.0       Sairam      Data Extraction
"""
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
from dateutil.relativedelta import relativedelta
from datetime import datetime
today = datetime.now().strftime('%B-%y')
print(today)
import pandas as pd

TableData = []
TableHeaders = ['Annual premium', today, 'Age at purchase', 'Sex', 'Smoker?', 'Sum insured(S$)', 'Interest rate', 'SI features',
                'Policy term(years)', 'Premium term', 'Death cover?', 'Terminal illness?', 'TPD?', 'Critical illness?', 'Other benefits?',
                'Par or Non-par?', 'Renewability',]

order = ['Annual premium','Age at purchase', 'Sex', 'Smoker?', 'Sum insured(S$)', 'Interest rate', 'SI features', 'Policy term(years)', 'Premium term',
         'Death cover?', 'Terminal illness?','TPD?', 'Critical illness?', 'Other benefits?', 'Par or Non-par?', 'Renewability', today]
requiredInsurers = {
    'AIA Singapore': 'AIA',
    'Aviva': 'Aviva',
    'AXA Insurance Pte Ltd': 'AXA',
    'Etiqa Insurance Pte. Ltd.': 'Etiqa',
    'FWD SINGAPORE PTE. LTD.': 'FWD',
    'Great Eastern Life': 'GE',
    'HSBC Insurance (Singapore) Pte. Limited': 'HSBC',
    'Manulife (Singapore) Pte. Ltd.': 'MFC',
    'NTUC Income Insurance Co-operative Limited': 'NTUC',
    'Prudential Assurance Company Singapore (Pte) Limited': 'PRU',
    'Tokio Marine Life Insurance Singapore Ltd': 'Tokio Marine'

}
def ClickFunction(checkValue, driver, ele, subele):
    try:
        driver.find_element_by_xpath(ele).click()
        time.sleep(2)
        found = False
        for id, li in enumerate(
                driver.find_element_by_xpath(subele).find_elements_by_tag_name('li')):
            sumdropDownNumber = re.search('[0-9,]+', li.text)
            if sumdropDownNumber is not None:
                sumdropDownNumber = re.sub('[^0-9]', '', sumdropDownNumber.group(0))
                if int(checkValue) == int(sumdropDownNumber):
                    driver.find_element_by_xpath(subele+'/li[' + str(id + 1) + ']').click()
                    found = True
                    break
        if found:
            return 0
        else:
            return checkValue
    except:
        return checkValue

def conditionClick(driver, conditionValue, checkValue, path):
    if conditionValue == checkValue:
        element = driver.find_element_by_xpath(path)
        driver.execute_script("arguments[0].click();", element)

def getData(driver,row,TableData):
    sheetName = row['Category'] + ' ' + str(row['Year']) + ' ' + str(row['Age']) + row['Gender'][0]
    if row['Critical Illness Benefits'] == 'Yes':
        sheetName = sheetName+ 'CI'
    Table = []


    if row['Category'] == 'WL':
        element = driver.find_element_by_xpath('//*[@id="bips-option"]/li[2]')
        driver.execute_script("arguments[0].click();", element)

        # Coverage Term
        time.sleep(5)
        if ClickFunction(row['Year'], driver, '//*[@id="s2id_premiumTermDcips"]', '//*[@id="select2-results-14"]') != 0:
            print('Please check the input value', row['Year'])
            return

        # Sum Assured
        if ClickFunction(row['Sum Assured'], driver, '//*[@id="s2id_SADCIPWLAn"]', '//*[@id="select2-results-6"]') != 0:
            print('Please check the input value', row['Sum Assured'])
            return

            # Sort Result By
        driver.find_element_by_xpath('// *[ @ id = "s2id_sortWLGroup"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="select2-results-17"]/li[6]').click()
    else:
        # Coverage Term
        time.sleep(5)
        if ClickFunction(row['Year'], driver, '//*[@id="s2id_coverageTermTLDCIPs"]', '//*[@id="select2-results-9"]') != 0:
            print('Please check the input value', row['Year'])
            return


            # Sum Assured
        if ClickFunction(row['Sum Assured'], driver, '//*[@id="s2id_SADCIPTermAn"]',  '//*[@id="select2-results-4"]') != 0:
            print('Please check the input value', row['Sum Assured'])
            return

        # Sort Result By
        driver.find_element_by_xpath('//*[@id="s2id_sortNonWLGroup"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="select2-results-16"]/li[4]').click()

    #Date Element
    d = datetime.now() - relativedelta(years=int(row['Age']))
    driver.find_element_by_id('date').send_keys(d.strftime("%d/%m/%Y"))
    driver.find_element_by_tag_name('body').click()

    #Gender Element
    conditionClick(driver, row['Gender'], 'Male', '//*[@id="step4"]/div[2]/ul/li[4]/ul/li[1]')

    #Smoker
    conditionClick(driver, row['smoker'], 'Yes', '//*[@id="smoker"]/li[1]')

    #Critical illness
    conditionClick(driver, row['Critical Illness Benefits'], 'Yes', '//*[@id="illness-benefit"]/li[1]')

    #Submit Button
    try:
        time.sleep(3)
        driver.find_element_by_class_name('close-disclaimer').click()
    except Exception as e:
        print(e)


    element = driver.find_element_by_xpath('//*[@id="viewPopup"]')
    driver.execute_script("arguments[0].click();", element)

    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='iUnderstant']"))
        )
    element.click()
    try:
        count = int(driver.find_element_by_xpath('//*[@id="showingProducts"]').text.split()[-1])
        print('count = ', count)
    except:
        count = 10

    for k in range(count):
        print('-'.center(100,'-'))
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        source_element = driver.find_element_by_id('result_container')
        for kl in range(10):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', source_element)
        time.sleep(3)
        li = BeautifulSoup(driver.find_element_by_id(str(k)).get_attribute('innerHTML'))
        Heading = li.find('h3').text
        for key, name in requiredInsurers.items():
            if name in Heading:
                Heading = name
                break
        Amount = li.find('span', attrs={'id':'TGpayoutDisp'}).text
        tpdRideApp = driver.find_element_by_id(str(k)).find_element_by_class_name('tpdRideApp').find_element_by_tag_name('img').get_attribute('src')
        TPD = 'Yes' if 'active' in tpdRideApp else 'No'
        driver.find_element_by_id(str(k)).find_element_by_class_name('search_detail').click()

        time.sleep(3)
        jsoup = BeautifulSoup(driver.page_source)
        for rem in jsoup.find_all('div', attrs={'class':re.compile('tab-area'), 'style':'display: none;'}):
            rem.decompose()


        PremiumTerm = jsoup.find('div', attrs={'class':re.compile('pay-period')})
        PremiumTerm = PremiumTerm.text if PremiumTerm is not None else None
        policyTerm = jsoup.find('div', attrs={'class':re.compile('(policy-term|policy-coverage-term)')})
        policyTerm = policyTerm.text if policyTerm is not None else None
        print(PremiumTerm)
        print(policyTerm)

        wl_tab_area = jsoup.find('div', attrs={'class': 'product_details_right'})
        ben = wl_tab_area.find('div', attrs={'class': re.compile('product-description')})
        ben = ben.text if ben is not None else ''

        par = 'non-par' if 'non-participating' in ben else ('par' if 'participating' in ben else 'non-par')
        print('par = ', par)
        print('ben = ', ben)
        benefits = {'Terminal': ['Terminal illness', 'Yes'],
                    'Critical': ['Critical illness', 'No'],
                    'Renewa': ['Renewability', 'No'],
                    'Other': ['Other', 'No'],
                    'Total and Permanent Disability': ['TPD', TPD],
                    'TPD': ['TPD', TPD],
                    'Death':['Death', 'No'],
                    }

        if 'Benefits :' in ben:
            ben = ben[ben.index('Benefits :') + len('Benefits :'):]
            ben = ben[:ben.index(':')] if ':' in ben else ben
            print(ben)

            for key in benefits.keys():
                if key.lower() in ben.lower():
                    benefits[key][1] = 'Yes'

        data = [Heading, Amount, row['Age'], row['Gender'], row['smoker'], row['Sum Assured'], '', row['SI Feature'],
         policyTerm, PremiumTerm, benefits['Death'][1], benefits['Terminal'][1], benefits['Total and Permanent Disability'][1],
         benefits['Critical'][1], 'No',
         par, benefits['Renewa'][1]]
        print(data)
        Table.append(data)
        driver.execute_script("window.history.go(-1)")
        time.sleep(3)
        break
    df = pd.DataFrame(Table, columns=TableHeaders)
    df[today] = df[today].apply(lambda x:re.sub('[^0-9,]', '', x))
    df['Policy term(years)'] = df['Policy term(years)'].apply(lambda x:x.replace('years', '') if x is not None else x)
    df['Premium term'] = df['Premium term'].apply(lambda x: x.replace('years', '') if x is not None else x)
    df = df.T #.set_index('Annual premium')
    df = df.reindex(order)
    TableData[sheetName] = df
    return TableData


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    df = pd.read_excel('C:\\Users\\doddsai.BU1-D2208N62\\Desktop\\compareFirst.xlsx')
    print(df.to_dict(orient='records'))
    TableData = dict()
    # TableData.append(TableHeaders)
    for row in df.to_dict(orient='records'):
        driver.delete_all_cookies()
        # row = df.to_dict(orient='records')[-2]
        print(row)
        urls = [[False,"http://www.comparefirst.sg/wap/homeEvent.action#"],
                [True,"http://www.comparefirst.sg/wap/homeEvent.action#"]]
        for url in urls[:1]:
            driver.get("http://www.comparefirst.sg/wap/homeEvent.action#")
            try:
                element = driver.find_element_by_class_name('introjs-overlay')
                driver.execute_script("arguments[0].click();", element)
            except Exception as e:
                print(e)
            getData(driver,row,TableData)
        break
    #Close The Driver
    driver.close()
    with pd.ExcelWriter('excel_file.xlsx',engine='xlsxwriter') as writer:
        for ws_name, df_sheet in TableData.items():
            df = pd.DataFrame([['PRICE QUOTES:', 'Term Life'],['Source:', 'http://www.comparefirst.sg']],columns=['source1', 'source2'])
            df.to_excel(writer, sheet_name=ws_name, header=None, index=None,startrow=0, startcol=0)
            df_sheet.to_excel(writer, sheet_name=ws_name, header=None, startrow=4, startcol=1)
            # df_sheet.to_excel(writer, sheet_name=ws_name, header=None)

    # writer = pd.ExcelWriter('hello2.xlsx', engine='xlsxwriter')
    # for key in TableData.keys():
    #     # df = TableData[key]
    #     TableData[key].to_excel(writer, sheet_name=key)


    # print(tabulate(TableData))
    # df = pd.DataFrame(TableData[1:], columns=TableHeaders)
    # df.to_csv('compareFirst.csv', index=False)
    # df.set_index('Annual premium').T.to_csv('hello.csv', index=False)



