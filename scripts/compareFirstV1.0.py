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
from dateutil.relativedelta import relativedelta
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
# import compareFirstV1.2
# from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


TODAY = datetime.now().strftime('%B-%y')
OUTPUT_LOCATION = 'excel_file.xlsx'
# table_data = []

#All Columns
TABLE_HEADERS = ['Annual premium', TODAY, 'Age at purchase', 'Sex', 'Smoker?', 'Sum insured(S$)', 'Interest rate',
                 'SI features', 'Policy term(years)', 'Premium term', 'Death cover?', 'Terminal illness?', 'TPD?',
                 'Critical illness?', 'Other benefits?', 'Par or Non-par?', 'Renewability'
                ]

#Arrange the columns in required format
ORDER = ['Annual premium', 'Age at purchase', 'Sex', 'Smoker?', 'Sum insured(S$)', 'Interest rate', 'SI features',
         'Policy term(years)', 'Premium term', 'Death cover?', 'Terminal illness?', 'TPD?', 'Critical illness?',
         'Other benefits?', 'Par or Non-par?', 'Renewability', TODAY]
HORIZONTAL_ORDER = ['Annual premium', 'AIA', 'Aviva', 'AXA', 'Etiqa', 'FWD', 'GE', 'HSBC', 'MFC', 'NTUC', 'PRU', 'Tokio Marine', 'Zurich']
#Short Names
REQUIRED_INSURERS = {
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
    'Tokio Marine Life Insurance Singapore Ltd': 'Tokio Marine',
    'Zurich': 'Zurich'

}


def click_function(check_value, driver, ele, subele):
    """
        click_function:
            Function is used to select drop down button and click the required argument.
    """
    try:
        driver.find_element_by_xpath(ele).click()
        time.sleep(2)
        found = False
        for _id, _li in enumerate(
                driver.find_element_by_xpath(subele).find_elements_by_tag_name('li')):
            sumdrop_down_number = re.search('[0-9,]+', _li.text)
            if sumdrop_down_number is not None:
                sumdrop_down_number = re.sub('[^0-9]', '', sumdrop_down_number.group(0))
                if int(check_value) == int(sumdrop_down_number):
                    driver.find_element_by_xpath(subele+'/li[' + str(_id + 1) + ']').click()
                    found = True
                    break
        if found:
            return 0
        else:
            return check_value
    except:
        return check_value


def condition_click(driver, condition_value, check_value, path):
    """
        condition_click:
            Funtion is used like toggle button
    """
    if condition_value == check_value:
        element = driver.find_element_by_xpath(path)
        driver.execute_script("arguments[0].click();", element)


def get_data(driver, row, table_data):
    '''
        get_data:
            Get All Product Details
    '''
    sheet_name = row['Category'] + ' ' + str(row['Year']) + 'Y ' + str(row['Age']) + row['Gender'][0]
    if row['Critical Illness Benefits'] == 'Yes':
        sheet_name = sheet_name+ 'CI'
    table = []


    if row['Category'] == 'WL':
        element = driver.find_element_by_xpath('//*[@id="bips-option"]/li[2]')
        driver.execute_script("arguments[0].click();", element)

        # Coverage Term
        time.sleep(5)
        if click_function(row['Year'], driver, '//*[@id="s2id_premiumTermDcips"]', '//*[@id="select2-results-14"]') \
                != 0:
            print('Please check the input value', row['Year'])
            return

        # Sum Assured
        if click_function(row['Sum Assured'], driver, '//*[@id="s2id_SADCIPWLAn"]', '//*[@id="select2-results-6"]') \
                != 0:
            print('Please check the input value', row['Sum Assured'])
            return

            # Sort Result By
        driver.find_element_by_xpath('// *[ @ id = "s2id_sortWLGroup"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="select2-results-17"]/li[6]').click()
    else:
        # Coverage Term
        time.sleep(5)
        if click_function(row['Year'], driver, '//*[@id="s2id_coverageTermTLDCIPs"]', '//*[@id="select2-results-9"]') != 0:
            print('Please check the input value', row['Year'])
            return


            # Sum Assured
        if click_function(row['Sum Assured'], driver, '//*[@id="s2id_SADCIPTermAn"]', '//*[@id="select2-results-4"]') \
                != 0:
            print('Please check the input value', row['Sum Assured'])
            return

        # Sort Result By
        driver.find_element_by_xpath('//*[@id="s2id_sortNonWLGroup"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="select2-results-16"]/li[4]').click()

    #Date Element
    date = datetime.now() - relativedelta(years=int(row['Age']))
    driver.find_element_by_id('date').send_keys(date.strftime("%d/%m/%Y"))
    driver.find_element_by_tag_name('body').click()

    #Gender Element
    condition_click(driver, row['Gender'], 'Male', '//*[@id="step4"]/div[2]/ul/li[4]/ul/li[1]')

    #Smoker
    condition_click(driver, row['smoker'], 'Yes', '//*[@id="smoker"]/li[1]')

    #Critical illness
    condition_click(driver, row['Critical Illness Benefits'], 'Yes', '//*[@id="illness-benefit"]/li[1]')

    #Submit Button
    try:
        time.sleep(3)
        driver.find_element_by_class_name('close-disclaimer').click()
    except Exception as error:
        print(error)


    #Click Extra popup
    try:
        element = driver.find_element_by_xpath('//*[@id="viewPopup"]')
        driver.execute_script("arguments[0].click();", element)
    except Exception as error:
        print('Extra popup not Found\n', error)
    # Click Agree Button
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='iUnderstant']")))
    element.click()

    #Find the count of number of products
    try:
        count = int(driver.find_element_by_xpath('//*[@id="showingProducts"]').text.split()[-1])
        print('count = ', count)
    except:
        count = 10

    for k in range(count):
        print('-'.center(100, '-'))
        time.sleep(5)

        #Scroll Down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        #Scoll down inside div
        source_element = driver.find_element_by_id('result_container')
        for _kl in range(10):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', source_element)
        time.sleep(3)
        _li = BeautifulSoup(driver.find_element_by_id(str(k)).get_attribute('innerHTML'))

        #Product Heading
        heading = _li.find('h3').text

        # Interest
        projected_rate = _li.find('span', attrs={'class':'projectedRate'})
        projected_rate = projected_rate.text if projected_rate is not None else None

        #Assign Short Names to products
        req_not_found = True
        for key, name in REQUIRED_INSURERS.items():
            if key in heading.strip():
                heading = name
                req_not_found = False
                break
        if req_not_found:
            continue

        # Product amount
        amount = _li.find('span', attrs={'id':'TGpayoutDisp'}).text

        #Find TPD
        tpd_ride_app = driver.find_element_by_id(str(k)).find_element_by_class_name('tpdRideApp').\
            find_element_by_tag_name('img').get_attribute('src')
        tpd = 'Yes' if 'active' in tpd_ride_app else 'No'
        driver.find_element_by_id(str(k)).find_element_by_class_name('search_detail').click()

        time.sleep(3)
        #Remove Extra tabs
        jsoup = BeautifulSoup(driver.page_source)
        for rem in jsoup.find_all('div', attrs={'class':re.compile('tab-area'), 'style':'display: none;'}):
            rem.decompose()

        #Find Premium Term
        premium_term = jsoup.find('div', attrs={'class':re.compile('pay-period')})
        premium_term = premium_term.text if premium_term is not None else None

        #Find Policy Term
        policy_term = jsoup.find('div', attrs={'class':re.compile('(policy-term|policy-coverage-term)')})
        policy_term = policy_term.text if policy_term is not None else None

        #Get product description for finding the benefits
        wl_tab_area = jsoup.find('div', attrs={'class': 'product_details_right'})
        ben = wl_tab_area.find('div', attrs={'class': re.compile('product-description')})
        ben = ben.text if ben is not None else ''

        #non-par or par variable
        par = 'non-par' if 'non-participating' in ben else ('par' if 'participating' in ben else 'non-par')

        benefits = {'Terminal': ['Terminal illness', 'Yes'],
                    'Critical': ['Critical illness', 'No'],
                    'Renewa': ['Renewability', 'No'],
                    'Other': ['Other', 'No'],
                    'Total and Permanent Disability': ['TPD', tpd],
                    'TPD': ['TPD', tpd],
                    'Death':['Death', 'No']
                    }

        if 'Benefits :' in ben:
            ben = ben[ben.index('Benefits :') + len('Benefits :'):]
            ben = ben[:ben.index(':')] if ':' in ben else ben
            print(ben)

            #Get Benifits
            for key in benefits.keys():
                if key.lower() in ben.lower():
                    benefits[key][1] = 'Yes'

        #Store All Data into data variable
        data = [heading, amount, row['Age'], row['Gender'], row['smoker'], row['Sum Assured'], projected_rate,
                row['SI Feature'], policy_term, premium_term, benefits['Death'][1], benefits['Terminal'][1],
                benefits['Total and Permanent Disability'][1], benefits['Critical'][1], 'No', par,
                benefits['Renewa'][1]
        ]
        print(data)
        table.append(data) #Append Data to TABLE
        driver.execute_script("window.history.go(-1)") #Go Back to previous page
        time.sleep(3)
        break
    _df = pd.DataFrame(table, columns=TABLE_HEADERS)
    _df[TODAY] = _df[TODAY].apply(lambda x: re.sub('[^0-9,]', '', x))
    _df['Policy term(years)'] = _df['Policy term(years)'].apply(lambda x: x.replace('years', '') if x is not None else x)
    _df['Premium term'] = _df['Premium term'].apply(lambda x: x.replace('years', '') if x is not None else x)
    print(_df['Annual premium'].tolist())
    for required_key,req_item in REQUIRED_INSURERS.items():
        if req_item not in _df['Annual premium'].tolist():
            _df[req_item] = 'dummy'
    print(_df)
    # try:
    #     for _df['']
    # except:
    #     pass
    _df = _df.T
    _df = _df.reindex(ORDER)
    print('before = ',_df)

    # _df = _df[HORIZONTAL_ORDER]
    print('-'.center(100))
    print('after df = ', _df)
    print(_df)
    table_data[sheet_name] = _df
    return table_data


if __name__ == '__main__':

    startTime = time.time()

    #Open Firefox Browser
    driver = webdriver.Firefox()
    driver.maximize_window()

    #Load All Records
    DF = pd.read_excel('C:\\Users\\doddsai.BU1-D2208N62\\Desktop\\compareFirst.xlsx')
    print(DF.to_dict(orient='records'))
    table_data = dict()

    #Loop All Records
    for row in DF.to_dict(orient='records'):
        driver.delete_all_cookies()
        print(row)
        urls = [[False, "http://www.comparefirst.sg/wap/homeEvent.action#"],
                [True, "http://www.comparefirst.sg/wap/homeEvent.action#"]]
        for url in urls[:1]:
            driver.get("http://www.comparefirst.sg/wap/homeEvent.action#")
            try:
                element = driver.find_element_by_class_name('introjs-overlay')
                driver.execute_script("arguments[0].click();", element)
                get_data(driver, row, table_data)
            except Exception as error:
                print(error)

        break

    #Close The Driver
    driver.close()

    #Move The Data to Excel File.
    with pd.ExcelWriter(OUTPUT_LOCATION, engine='xlsxwriter') as writer:
        for ws_name, df_sheet in table_data.items():
            _df = pd.DataFrame([['PRICE QUOTES:', 'Term Life'], ['Source:', 'http://www.comparefirst.sg']],
                              columns=['source1', 'source2'])
            _df.to_excel(writer, sheet_name=ws_name, header=None, index=None, startrow=0, startcol=0)
            df_sheet.to_excel(writer, sheet_name=ws_name, header=None, startrow=4, startcol=1)

    print('Total Execution TIme = ', time.time()-startTime)
