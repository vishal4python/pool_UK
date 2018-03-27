#-*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import input_path
from maks_lib import output_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

df0=pd.read_excel(input_path+"Lioyds.xlsx",sheet_name="page-1")
df1=pd.read_excel(input_path+"Lioyds.xlsx",sheet_name="page-2")
df2=pd.read_excel(input_path+"Lioyds.xlsx",sheet_name="page-3")
df01=df0[5:6]
df01= df01.rename(columns={'Unnamed: 2': 'Bank_Product_Name'})
df01.drop(df01.columns[[0,1,3,4]], axis=1, inplace=True)
df=df0[8:9]

df01["Balance"] = df["Unnamed: 1"].values
df01["Interest"] = df["Unnamed: 2"].values
df01["Interest"]=(df01["Interest"]*100).astype(str)+'%'
df01["AER"]=df01["Interest"]


df02=df0[20:21]
df02= df02.rename(columns={'Unnamed: 4': 'Bank_Product_Name'})
df02.drop(df02.columns[[0,1,2,3]], axis=1, inplace=True)
df=df0[23:24]
df02["Balance"]=df["Unnamed: 2"].values
df02["Interest"]=df["Unnamed: 4"].values
df02["AER"]=df02["Interest"]
df02["Interest"]=(df02["Interest"]).astype(str)+'%'
df02["AER"]=(df02["AER"]).astype(str)+'%'

df03=df0[26:27]
df03= df03.rename(columns={'                                                           Savings rates': 'Bank_Product_Name'})
df03.drop(df03.columns[[1,2,3,4]], axis=1, inplace=True)
df=df0[29:30]
df03["Balance"]=df["Unnamed: 1"].values
df03["Interest"]=df["Unnamed: 2"].values
df03["AER"]=df03["Interest"]
df03["Interest"]=(df03["Interest"]*100).astype(str)+'%'
df03["AER"]=(df03["AER"]*100).astype(str)+'%'

df04=df0[31:32]
df04= df04.rename(columns={'                                                           Savings rates': 'Bank_Product_Name'})
df04.drop(df04.columns[[3,4]], axis=1, inplace=True)
df04["Bank_Product_Name"]=df03["Bank_Product_Name"].values
df04= df04.rename(columns={'Unnamed: 1': 'Balance','Unnamed: 2': 'Interest'})
df04["Interest"]=(df04["Interest"]*100).astype(str)+'%'
df04["AER"]=df04["Interest"]

frames_page1 = [df01,df02,df03,df04]
result_page1=pd.concat(frames_page1)
result_page1["Bank_Product_Type"]="Savings"

df01=df1[0:1]
df01= df01.rename(columns={'Unnamed: 3': 'Bank_Product_Name'})
df01.drop(df01.columns[[0,1,2,4,5]], axis=1, inplace=True)
df=df1[3:4]
df01["Balance"] = df["Unnamed: 2"].values
df01["Interest"] = df["Unnamed: 3"].values
df01["Interest"]=(df01["Interest"]*100).astype(str)+'%'
df01["AER"]=df01["Interest"]

df02=df1[10:11]
df02= df02.rename(columns={'                                                            Savings rates': 'Bank_Product_Name'})
df02.drop(df02.columns[[1,2,3,4]], axis=1, inplace=True)
df=df1[13:14]
df02["Balance"]=df["Unnamed: 1"].values
df02["Interest"]=df["Unnamed: 3"].values
df02["Interest"]=(df02["Interest"]*100).astype(str)+'%'
df02["AER"]=df02["Interest"]
df02.drop(df02.columns[[1]], axis=1, inplace=True)
df=pd.DataFrame(df02["Bank_Product_Name"].str.split('–').tolist(),columns=["Int","PY"])
df02["Term in Months"]=df["PY"].values
df=pd.DataFrame(df02["Term in Months"].str.split(' ').tolist(),columns=["Int","PY",'f'])
df02["Term in Months"]=df["PY"].values
df02["Term in Months"]=df02["Term in Months"].apply(int)
df02["Term in Months"]=(df02["Term in Months"]*12)
df02["Bank_Product_Type"]="Term Deposits"

df03=df1[14:15]
df03= df03.rename(columns={'                                                            Savings rates': 'Bank_Product_Name'})
df03.drop(df03.columns[[1,2,3,4,5]], axis=1, inplace=True)
df=df1[17:18]
df03["Balance"]=df["Unnamed: 1"].values
df03["Interest"]=df["Unnamed: 2"].values
df03["Interest"]=(df03["Interest"]*100).astype(str)+'%'
df03["AER"]=df03["Interest"]
df=pd.DataFrame(df03["Bank_Product_Name"].str.split('–').tolist(),columns=["Int","PY"])
df03["Term in Months"]=df["PY"].values
df=pd.DataFrame(df03["Term in Months"].str.split(' ').tolist(),columns=["Int","PY",'f'])
df03["Term in Months"]=df["PY"].values
df03["Term in Months"]=df03["Term in Months"].apply(int)
df03["Term in Months"]=(df03["Term in Months"]*12)
df03["Bank_Product_Type"]="Term Deposits"

# df04=df1[30:31]
# df04= df04.rename(columns={'Unnamed: 2': 'Bank_Product_Name'})
# df04.drop(df04.columns[[0,1,3,4,5]], axis=1, inplace=True)
# df=df1[33:34]
# df04["Balance"]=df["Unnamed: 1"].values
# df04["Interest"]=df["Unnamed: 2"].values
# df04["Interest"]=(df04["Interest"]*100).astype(str)+'%'
# df04["AER"]=df04["Interest"]

frames_page2 = [df01,df02,df03]
result_page2=pd.concat(frames_page2)
result_page2['Bank_Product_Type'].fillna("Savings",inplace=True)

# df01=df2[0:1]
# df01= df01.rename(columns={'Unnamed: 2': 'Bank_Product_Name'})
# df01.drop(df01.columns[[0,1,3]], axis=1, inplace=True)
# df=df2[3:4]
# df01["Balance"]=df["Unnamed: 1"].values
# df01["Interest"]=df["Unnamed: 2"].values
# df01["Interest"]=(df01["Interest"]*100).astype(str)+'%'
# df01["AER"]=df01["Interest"]


df02=df2[5:6]
df02= df02.rename(columns={'Unnamed: 2': 'Bank_Product_Name'})
df02.drop(df02.columns[[0,1,3]], axis=1, inplace=True)
df=df2[8:9]
df02["Balance"]=df["Unnamed: 1"].values
df02["Interest"]=df["Unnamed: 2"].values
df02["Interest"]=(df02["Interest"]*100).astype(str)+'%'
df02["AER"]=df02["Interest"]
df=pd.DataFrame(df02["Bank_Product_Name"].str.split('–').tolist(),columns=["Int","PY"])
df02["Term in Months"]=df["PY"].values
df=pd.DataFrame(df02["Term in Months"].str.split(' ').tolist(),columns=["Int","PY",'f'])
df02["Term in Months"]=df["PY"].values
df02["Term in Months"]=df02["Term in Months"].apply(int)
df02["Term in Months"]=(df02["Term in Months"]*12)
df02["Bank_Product_Type"]="Term Deposits"

frames_page3 = [df02]
result_page3=pd.concat(frames_page3)
result_page3['Bank_Product_Type'].fillna("Savings",inplace=True)

frames = [result_page1,result_page2,result_page3]
result=pd.concat(frames)
for index in range(len(result.index)):
    result['Bank_Product_Name'].iloc[index] = result['Bank_Product_Name'].iloc[index].replace("–", " - ")
   

df_final = pd.DataFrame(columns=["Date", "Bank_Native_Country", 'State', "Bank_Name", 'Bank_Local_Currency', 'Bank_Type',
             'Bank_Product', 'Bank_Product_Type', 'Bank_Product_Name',
             'Balance', 'Bank_Offer_Feature', 'Term in Months', 'Interest_Type', 'Interest','AER','Bank_Product_Code'])

df_final['AER'] = result['AER'].values
df_final['Balance'] = result['Balance'].values
df_final['Bank_Product_Name'] = result['Bank_Product_Name'].values
df_final['Bank_Product_Type'] = result['Bank_Product_Type'].values
df_final['Interest'] =result['Interest'].values
df_final['Term in Months'] = result['Term in Months'].values
df_final['Date'] = now.strftime("%m-%d-%Y")
df_final["Bank_Native_Country"]="UK"
df_final["State"]="London"
df_final["Bank_Name"]="Lloyds Bank"
df_final["Bank_Local_Currency"]="GBP"
df_final["Bank_Type"]="Bank"
df_final["Bank_Product"]="Deposits"
df_final["Bank_Offer_Feature"]="Offline"
df_final["Interest_Type"]="Variable"

for index in range(len(result.index)):
    #result['Bank_Product_Name'].iloc[index] = result['Bank_Product_Name'].iloc[index].replace("–", " - ")

    if "Online" in df_final['Bank_Product_Name'].iloc[index]:
        df_final["Bank_Offer_Feature"].iloc[index] = 'Online'

df_final.to_csv(output_path+"Consolidate_Lloyds_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False )
