from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import  BeautifulSoup as bs
import pandas as pd
import time
import warnings
import datetime
import os
from maks_lib import output_path

now = datetime.datetime.now()

warnings.simplefilter(action='ignore')


class Hailfax:
    def __init__(self, url, pvalue, dvalue, term):
        self.url = url
        self.pvalue = pvalue
        self.dvalue = dvalue
        self.term = term

    def start_driver(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def close_driver(self):
        return self.driver.close()

    def get_url(self):
        self.driver.get(self.url)

    def fillform(self):
        time.sleep(6)
        no_button = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/form/div/div[1]/div/div[1]/div[1]/fieldset/div[2]/div[1]/label[2]/span")
        no_button.click()
        select = Select(self.driver.find_element_by_id('goal'))
        select.select_by_value('1')
        how_much_cost = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/form/div/div[1]/div/div[2]/div[2]/div[1]/span")
        how_much_cost.click()
        #self.driver.find_element_by_xpath('//*[@id="test-error-stepper"]').send_keys("90000") #property value
        self.driver.find_element_by_name("valueOfprop").send_keys("90000")#self.pvalue[1])
        self.driver.find_element_by_name("depositAmount").send_keys("18000")#self.dvalue[1])
        select = Select(self.driver.find_element_by_name("mortgageTerm"))
        select.select_by_value("10")#self.term)
        self.driver.find_element_by_class_name("button button-primary show-mortgages button-full-width ajax").click()


    def get_current_url(self):
        return self.driver.current_url

    def save_page(self):
        page = self.driver.page_source
        with open("hailfax_mortgage_"+self.dvalue[0]+"_"+self.term+".html", 'w')as file:
            file.write(page)

# class ExtractInfo(Citi_mortgage):
#
#     def __init__(self, page,tab, eprice, dprice):
#         self.page = page
#         self.tab = tab
#         self.eprice = eprice
#         self.dprice = dprice
#
#     def findtables_tab1(self):
#         soup = bs(self.page, "lxml")
#         file = open("test.txt",'w')
#         h = [ f.text for f in soup.find_all('h1', {'class':self.tab[0]})]
#         d = [j.text for j in soup.find_all('div', {'class':self.tab[1]})]
#         for l in zip(h,d):
#             la= l[1].split('\n')
#             if 'points' in la[30]:
#                 #f = l[0]+","+la[5]+","+la[12]+","+la[30]+'\n'
#                 f = l[0] + "\t" + la[5] + "\t" + la[12]+'\n'
#                 file.write(f)
#
#             elif "points" in la[27]:
#                 f = l[0]+"\t"+la[5]+"\t"+la[12]+'\n'
#                 #f = l[0] + "," + la[5] + "," + la[12] + "," + la[27] + '\n'
#                 file.write(f)
#         file.close()
#         time.sleep(3)
#         dataset = pd.read_table('test.txt',sep='\t',delimiter=None, header=None)
#         #dataset['Expected_Price'] = self.eprice[1]
#         dataset['Mortgage_Loan'] = self.dprice
#         dataset["Product_Term"] = dataset.iloc[:,0].str.replace("Year Fixed","")
#         for i in range(0, len(dataset)):
#             if "Libor ARM" in dataset.ix[i]['Product_Term']:
#                 dataset.ix[i]['Product_Term'] = 30
#
#         loan_type = pd.DataFrame(dataset.iloc[:,0].str.split(" ").tolist())
#         dataset["Loan_Type"] = loan_type.iloc[:,2].str.replace("ARM","Variable")
#
#         dataset.columns = ['Bank_Product_Name','Product_Interest','Mortgage_Apr',"Mortgage_Loan","Product_Term",'Loan_Type']
#         #print(dataset)
#         dataset.to_csv("Citi_Mortgage_"+self.eprice[0]+".csv",index=False)


if __name__ == "__main__":
    print("Starting scraping")

    property_values = [('case1','90000'),('case2','270000'),('case3','450000')]
    deposite_values = [('case1','18000'),('case2','54000'),('case3','90000')]
    url = "https://www.halifax.co.uk/mortgages/mortgage-calculator/calculator/"
    obj = Hailfax(url, property_values[0], deposite_values[0], 10)
    obj.start_driver()
    obj.get_url()
    obj.fillform()
    # for i in range(len(expected_price)):
    #     for term in [10,15,25,30]:
    #         obj = Hailfax(url, pvalue[i], dvalue[i], term)
    #         obj.start_driver()
    #         obj.get_url()
    #         obj.fillform()
    #         #obj.save_page()
    #         obj.close_driver()

#     tab1 = ['header-3 rate-card-panel-header-white', 'row rate-card-panel-items tb-hide']
#     for i in range(len(expected_price)):
#         extract = ExtractInfo(open("citi_mortgage_"+expected_price[i][0]+".html",'r'),tab1, expected_price[i], desired_price[i][1])
#         extract.findtables_tab1()
#     df1 = pd.read_csv("Citi_Mortgage_case1.csv")
#     df2 = pd.read_csv("Citi_Mortgage_case2.csv")
#     df3 = pd.read_csv("Citi_Mortgage_case3.csv")
#     df = pd.concat([df1, df2, df3])
#     df['Date'] = now.strftime("%m-%d-%Y")
#     df['Bank_Name'] = "CITIGROUP INC"
#     df['Bank_Product'] = "Mortgage"
#     df['Bank_Product_Type'] = "Mortgage"
#     df["Bank_Offer_Feature"] = "Offline"
#     df['Mortgage_Down_Payment'] = "20%"
#     df['Min_Credit_Score_Mortagage'] = "720+"
#
#
#  #   for val, row in df.iterrows():
# #        if "ARM" in row["Product_Term"]:
# #            df.ix[val,"Product_Term"] = "30 Year"
#     dff = df.reindex(columns=["Date", "Bank_Name" , "Bank_Product" ,
#                               'Bank_Product_Type', 'Bank_Offer_Feature' ,
#                               'Bank_Product_Name' , 'Product_Term' , 'Balance',
#                               'Product_Interest','Product_Apy',
#                               'Mortgage_Down_Payment','Mortgage_Loan',
#                               'Min_Credit_Score_Mortagage', 'Mortgage_Apr','Loan_Type'])
#
#     dff_consolidate = df.reindex(columns=["Date", "Bank_Name", "Bank_Product",
#                               'Bank_Product_Type', 'Bank_Offer_Feature',
#                               'Bank_Product_Name', 'Product_Term', 'Balance',
#                               'Product_Interest', 'Product_Apy',
#                               'Mortgage_Down_Payment', 'Mortgage_Loan',
#                               'Min_Credit_Score_Mortagage', 'Mortgage_Apr'])
#
#     dff.to_csv(output_path + "CITI_Data_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
#     dff_consolidate.to_csv(output_path + "Consolidate_CITI_Data_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
#
#     for rm in range(len(expected_price)):
#         os.remove("Citi_Mortgage_"+expected_price[rm][0]+".html")
#         os.remove("Citi_Mortgage_"+expected_price[rm][0]+".csv")
#
#     print("Finished Scraping ")
