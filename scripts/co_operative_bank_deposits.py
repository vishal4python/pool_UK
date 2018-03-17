# import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from tabulate import  tabulate
import re
import pandas as pd
from maks_lib import output_path
today = datetime.datetime.now()
path = output_path+"Consolidate_ CoOp_Data_Deposits_"+str(today.strftime('%Y_%m_%d'))+'.csv'
# path = "Consolidate_COOB_Data_Deposits_"+str(today.strftime('%Y_%m_%d'))+'.csv'
table = []
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name",
         "Min_Opening_Bal", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER"]
table_headers = ["Bank_Product_Type", "Bank_Product_Name", "Min_Opening_Bal", "Balance", "Bank_Offer_Feature", "Term in Months", "Interest_Type", "Interest", "AER"]
# table.append(table_headers)

resp = requests.get("https://www.co-operativebank.co.uk/savings/interest-rates")
jsoup = BeautifulSoup(resp.content, "lxml")
comparisonTable = jsoup.find("div", attrs={"class":"row cComparisonTable"})
headings = comparisonTable.find_all('dl', attrs={"class":"results-provider"})

if len(headings)!=0:

    #Britannia
    provider_1 = headings[0]
    britannia_heading = provider_1.find("h3")

    #Find Britannia Heading
    if britannia_heading is not None:
        britannia_heading = britannia_heading.text

    results_items = provider_1.find_all("div", attrs={"class":"results-item"})
    for results_item in results_items:
        # print(results_item)
        britannia_sub_heading = results_item.find("h5").text
        # print(britannia_sub_heading)
        britannia_table = results_item.find("table")
        # print(britannia_table)

        if britannia_table is not None:
            trs = britannia_table.find_all("tr")
            if trs is not None:
                for tr in trs:
                    # print(tr)

                    tds = tr.find_all("td")
                    britannia_data = [td.text for td in tds]
                    # print(britannia_data)
                    if len(britannia_data)>4:
                        # print(britannia_data)
                        britannia_data = britannia_data[1:]
                    if len(britannia_data) == 4:

                        try:
                            float(britannia_data[1].strip('%'))

                            if "annually" in britannia_data[-1].lower() or 'year' in britannia_data[-1].lower():
                                # print(britannia_data[-1])
                                terms_in_month = re.findall('\d.?yr',britannia_sub_heading)
                                if len(terms_in_month)>=1:
                                    terms_in_month = int(re.sub('[^0-9]','',terms_in_month[0]))*12
                                else:
                                    terms_in_month = None
                                if 'Online' in britannia_sub_heading:
                                    Bank_Offer_Feature = "Online"
                                else:
                                    Bank_Offer_Feature = "Offline"
                                # print(tds)


                                if "fixed" in britannia_table.text.lower():
                                    Interest_Type = "Fixed"
                                else:
                                    Interest_Type = 'Variable'

                                check_balance_type = britannia_table.text
                                # print(check_balance_type)
                                if "opening" in check_balance_type.lower():
                                    opening_balance = britannia_data[0]
                                    balance = None
                                else:
                                    opening_balance = None
                                    balance = britannia_data[0]
                                # print(check_balance_type)
                                a = ['Savings', britannia_heading.strip()+' '+britannia_sub_heading.strip(), opening_balance, balance, Bank_Offer_Feature, terms_in_month,Interest_Type,britannia_data[1], britannia_data[2] ]
                                table.append(a)
                        except Exception as e:
                            pass


        # print("============================================================")

    print('----------------------------------------------------------------------')
    #The Co-operative Bank
    provider_2 = headings[1]
    co_operative_bank_heading = provider_2.find("h3").text
    # print(co_operative_bank_heading)

    results_items_2 = provider_2.find_all("div", attrs={"class": "results-item"})
    if results_items_2 is not None:
        for results_item_2 in results_items_2:
            co_operative_sub_heading = results_item_2.find("h5").text
            # print(co_operative_sub_heading)
            co_operative_table = results_item_2.find("table")
            trs = co_operative_table.find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
                co_operative_data = [td.text for td in tds]
                # print(co_operative_data)
                if len(co_operative_data) > 4:

                    co_operative_data = co_operative_data[1:]
                if len(co_operative_data) == 4:
                    try:
                        float(co_operative_data[1].strip('%'))
                        if "annually" in co_operative_data[-1].lower() or 'year' in co_operative_data[-1].lower():
                            terms_in_month = re.findall('\d.?yr', co_operative_sub_heading)
                            if len(terms_in_month) >= 1:
                                terms_in_month = int(re.sub('[^0-9]', '', terms_in_month[0]))*12
                            else:
                                terms_in_month = None

                            if 'online' in co_operative_sub_heading.lower():
                                Bank_Offer_Feature = "Online"
                            else:
                                Bank_Offer_Feature = "Offline"
                            variable_type = ' '.join([t.text for t in trs])
                            if "fixed" in co_operative_table.text.lower():
                                Interest_Type = "Fixed"
                            else:
                                Interest_Type = 'Variable'
                            check_balance_type = co_operative_table.text
                            if "opening" in check_balance_type.lower():
                                opening_balance = co_operative_data[0]
                                balance = None
                            else:
                                opening_balance = None
                                balance = co_operative_data[0]
                            # print(trs[1])
                            a = ["Savins", co_operative_bank_heading.strip() + ' ' + co_operative_sub_heading.strip(),opening_balance, balance,
                                 Bank_Offer_Feature, terms_in_month, Interest_Type, co_operative_data[1], co_operative_data[2]]
                            table.append(a)
                    except Exception as e:
                        print(e)

        # print("============================================================")




try:
    current_account = requests.get("https://www.co-operativebank.co.uk/currentaccounts/compare-current-accounts")
    current_account = BeautifulSoup(current_account.content, "lxml")
    current_trs = current_account.find("tbody", attrs={"class":"js-comp-table-tbody"}).find_all("tr")
    cc = [tr.find("a", attrs={"class":"u-epsilon u-text-thin"}).text for tr in current_trs]
    # print(cc)
    for c in cc:
        table.append(["Current", c, None, None, "Offline", None,None, None, None])
except Exception as e:
    print(e)
print(tabulate(table))

def Change_bank_product_name(x):
    if "fixed" in str(x).lower():
        return "Term Deposits"
    elif "variable" in str(x).lower():
        return "Savings"
    else:
        return 'Current'

df = pd.DataFrame(table, columns=table_headers)
df['Balance'] = df['Balance'].apply(lambda x: re.sub('[^0-9.]', '', str(x)) if len(re.sub('[^0-9.]', '', str(x)))!=0 else None)
df['Min_Opening_Bal'] = df['Min_Opening_Bal'].apply(lambda x: re.sub('[^0-9.]', '', str(x)) if len(re.sub('[^0-9.]', '', str(x)))!=0 else None)
df['Interest'] = df['Interest'].apply(lambda x: re.sub('[^0-9.]', '', str(x)) if len(re.sub('[^0-9.]', '', str(x)))!=0 else None)
df['AER'] = df['AER'].apply(lambda x: re.sub('[^0-9.]', '', str(x)) if len(re.sub('[^0-9.]', '', str(x)))!=0 else None)
df['Bank_Product_Type'] = df['Interest_Type'].apply(Change_bank_product_name)
df.loc[:,"Date"] = today.strftime('%m-%d-%Y')
df.loc[:,"Bank_Native_Country"] = "UK"
df.loc[:,"State"] = "London"
df.loc[:,"Bank_Name"] = "The Co-operative Bank"
df.loc[:,"Bank_Local_Currency"] = "GBP"
df.loc[:,"Bank_Type"] = "Bank"
df.loc[:,"Bank_Product"] = "Deposits"
df = df[order]
df.to_csv(path, index=False)
# print(df)
# print(jsoup)

# df = pd.read_html(str(tables))
# print(df)

