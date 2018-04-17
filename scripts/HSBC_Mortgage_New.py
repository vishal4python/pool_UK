import requests
from bs4 import BeautifulSoup
from tabulate import  tabulate
import pandas as pd
import re
import datetime
today = datetime.datetime.now()
Excel_Table = []
from maks_lib import output_path
path = output_path+'Consolidate_HSBC_Data_Mortgage_v2_'+today.strftime('%m_%d_%Y')+'.csv'
table_headers = ['Bank_Product_Name', 'Min_Loan_Amount', 'Term (Y)', 'Interest_Type', 'Interest', 'APRC', 'Mortgage_Loan_Amt', 'Fixed_Rate_Term', 'Mortgage_Down_Payment']
# Excel_Table.append(table_headers)
cases = [[90000, 18000], [270000, 54000], [450000, 90000]]
terms = [['Mtp_Hmcib_Mtp023_RepayMortgage_007', 10],['Mtp_Hmcib_Mtp023_RepayMortgage_0012', 15], ['Mtp_Hmcib_Mtp023_RepayMortgage_0022', 25], ['Mtp_Hmcib_Mtp023_RepayMortgage_0027', 30]]

for case in cases:
    print(case, 'Running...')
    for term in terms:
        session = requests.session()
        p = session.get('https://www.hsbc.co.uk/1/2/mortgages/find-and-compare')
        form = BeautifulSoup(p.content, 'html.parser').find_all('form')[-1]
        termCheck = form.find('option', attrs={'value':term[0]})
        if termCheck is not None:
            termCheck = termCheck.text
            if str(term[1]) in termCheck:
                # print(form.find('input', attrs={'name':'es_iid'})['value'])
                data = {"viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form_SUBMIT":1,
                        "jsf_sequence":1,
                        "es_iid":form.find('input', attrs={'name':'es_iid'})['value'],
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:buyertypedropdown-option":"F",
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:propertytypedropdown-option":"P",
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:propertyvalue-field":case[0],
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:mydeposit-field":case[1],
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:outstandingbalance-field":"",
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:furtherborrowing-field":"",
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:mortgagetypedropdown-option":"A",
                        "repaymenttypedropdown-option":"C",
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:mortgagerepaymentdropdown-option":term[0],
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:mortgagerepaymentdropdown-month-option":0,
                        "macmd_findmortgage":"Find+a+mortgage",
                        "WIRE_ACTION":"SendAction",
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:findmortgagebuttonclicked":"findmortgagebuttonclicked",
                        "WIRE_ACTION":"",
                        "viewns_7_H2I8H042HGB810ALVJLGJR00E3_:mortgage-details-form:_idcl":"submit"}

                headers = {"Host":"www.hsbc.co.uk",
                           "Connection":"keep-alive",
                           "Content-Length":"1285",
                           "Cache-Control":"max-age=0",
                           "Origin":"https://www.hsbc.co.uk",
                           "Upgrade-Insecure-Requests":"1",
                           "Content-Type":"application/x-www-form-urlencoded",
                           "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
                           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                           "Referer":"https://www.hsbc.co.uk/1/2/mortgages/find-and-compare",
                           "Accept-Encoding":"gzip, deflate, br",
                           "Accept-Language":"en-US,en;q=0.9"}
                # headers['Referer'] = 'https://www.hsbc.co.uk/1/2/mortgages/find-and-compare'
                resp = session.post('https://www.hsbc.co.uk'+form['action'], data=data, headers = headers,cookies=p.cookies)
                # print(resp.content)
                table = BeautifulSoup(resp.content, 'html.parser').find_all('div', attrs={'class':'csTableContent'})[-1]
                if table is not None:
                    table.find('tbody').find_all()
                    for div in table.find_all("tr", {'class': re.compile('Hide')}):
                        div.decompose()
                    for tr in table.find_all('tr'):
                        try:
                            tds = tr.find_all('td')
                            if 'customer' not in tds[0].text.lower():
                                if '80' in tds[2].text.lower():
                                    a = [tds[0].text.replace('MoreLess',''), None, term[1], 'Variable', tds[3].text, tds[5].text, case[0]-case[1],'Fixed_Rate_Term',tds[2].text]
                                    Excel_Table.append(a)
                        except Exception as e:
                            print(e)
                else:
                    print('table not found')
            else:
                print('Please Check term attribute may be it was changed.')
        else:
            print('term Not found in options')
print(tabulate(Excel_Table))
df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Fixed_Rate_Term'] = df['Bank_Product_Name'].apply(lambda x:re.sub('[^0-9]','',re.findall('\d.* Year',x)[0]) if len(re.findall('\d.* Year',x))!=0 else None)
df['APRC'] = df['APRC'].apply(lambda x: re.sub('[^0-9.%]','',x))
df['Date'] = ' '+today.strftime("%m-%d-%Y")
df['Bank_Native_Country'] = 'UK'
df['State'] = 'London'
df['Bank_Name'] = 'HSBC'
df['Bank_Local_Currency'] = 'GBP'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = 'Offline'
df['Mortgage_Category'] = 'New Purchase'
df['Mortgage_Reason'] = 'Primary Residence'
df['Mortgage_Pymt_Mode'] = 'Principal + Interest'
df['Bank_Product_Code'] = None
df['Ticker'] = None
df['Mortgage_Down_Payment'] = '20%'
order = ["Date","Bank_Native_Country","State","Bank_Name","Bank_Local_Currency","Bank_Type","Bank_Product","Bank_Product_Type","Bank_Product_Name","Min_Loan_Amount","Bank_Offer_Feature","Term (Y)","Interest_Type","Interest","APRC","Mortgage_Loan_Amt","Mortgage_Down_Payment","Mortgage_Category","Mortgage_Reason","Mortgage_Pymt_Mode","Fixed_Rate_Term","Bank_Product_Code"]
df = df[order]
df.to_csv(path, index=False)
# print(df.tolist())
# print(tabulate(df.tolist()))
    # for div in table.find_all("tr", {'class': re.compile('Hide')}):
# print('https://www.hsbc.co.uk'+form['action'])
