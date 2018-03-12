from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import warnings
from maks_lib import output_path
warnings.simplefilter(action='ignore')

now = datetime.datetime.now()

class App:

    def __init__(self, url = 'https://www.synchronybank.com/banking/cd/ '):
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        sleep(3)
        self.data_page()
        sleep(5)

    def data_page(self):
        html = self.driver.execute_script("return document.documentElement.outerHTML")
        soup = bs(html, 'html.parser')
        df = pd.read_html(html)
        li = soup.find_all('li')
        min_open = li[28].getText()
        #li = soup.find_all('div', attrs={'class':'col-md-6 col-xs-12 no-padding vert-rule-white'})
        #print(li[0])
        Pd = soup.find_all('h2', attrs={'class':'heading-level-1'})
        Pd = Pd[1].getText()
        Mini = soup.find_all('p', attrs={'class':'para-text'})
        Mini = Mini[0].getText()
        term = soup.find_all('p', attrs={'class':'heading-level-2'})
        term = term[1].getText()
        return Pd, Mini, term, df, min_open

if __name__ == '__main__':
    app = App()
    Pd, Mini, term, df, min_open = app.data_page()
    df_0 = df[0].iloc[0:9, 0:2]
    df_0['Date'] = now.strftime("%m/%d/%Y")
    df_0['Bank Name'] = 'Synchrony'
    df_0['Product Type'] = Pd
    df_0['Product Name'] = 'TERM'
    df_0['Minimum opening balance'] = min_open
    df_0['Minimum Deposite'] = Mini
    df_0.rename(columns={"\n\t\tDEPOSIT AMOUNT\n\t\t$2,000+\n\t  ": "APY", "\n\t\t\n\t\t  TERM\n\t\t\n\t  ": "Term"},
                inplace=True)
    df_0["Product Name"] = "CD_" + df_0["Term"].str.strip()
    df_0 = df_0.reindex(columns=["Date", "Bank Name", "Product Name", "Minimum opening balance", "Minimum Deposite", "APY"])
    df_0.to_csv(output_path + "Sync_Data_Deposit{}.csv".format(now.strftime("%m_%d_%Y")), index=False)

