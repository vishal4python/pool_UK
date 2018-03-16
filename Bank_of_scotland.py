# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import input_path
from maks_lib import output_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

df1=pd.read_excel(input_path+"interest-rates (1).xlsx",sheet_name="page-1")
df2=pd.read_excel(input_path+"interest-rates (1).xlsx",sheet_name="page-2")
df3=pd.read_excel(input_path+"interest-rates (1).xlsx",sheet_name="page-3",header=None)


df01=df1[4:5]
df01= df01.rename(columns={'Savings Rates': 'Bank_Product_Name'})
df=df1[7:8]
df01["Balance"] = df["Unnamed: 1"].values
df01["Interest"] = df["Unnamed: 2"].values
df01["Interest"]=(df01["Interest"]*100).astype(str)+'%'
df01["AER"]=df01["Interest"]
df01.drop(df01.columns[[1,2,3]], axis=1, inplace=True)
######################################################################
df02=df2[2:3]
df02= df02.rename(columns={'Access Saver': 'Bank_Product_Name','Savings Rates': 'Bank_Product_Name','Unnamed: 1': 'Balance','Unnamed: 3': 'Interest','Unnamed: 4': 'AER'})
df02["Interest"]=(df02["Interest"]*100).astype(str)+'%'
df02["AER"]=df02["Interest"]
df02["Bank_Product_Name"]="Access Saver"
df02.drop(df02.columns[[2]], axis=1, inplace=True)

df03=df2[12:13]
df03= df03.rename(columns={'Access Saver': 'Bank_Product_Name'})
df=df2[15:16]
df= df.rename(columns={'Access Saver': 'Bank_Product_Name','Unnamed: 1': 'Balance','Unnamed: 2': 'Interest','Unnamed: 3': 'AER'})
df["Interest"]=(df["Interest"]*100).astype(str)+'%'
df["AER"]=df["Interest"]
df["Bank_Product_Name"]=df03["Bank_Product_Name"].values
df.drop(df.columns[[4]], axis=1, inplace=True)
df03=pd.DataFrame(df["Bank_Product_Name"].str.split('–').tolist(),columns=["Int","PY"])
df["Term in Months"]=df03["PY"].values
df03=pd.DataFrame(df["Term in Months"].str.split(' ').tolist(),columns=["Int","PY",'f'])
df["Term in Months"]=df03["PY"].values
df["Term in Months"]=df["Term in Months"].apply(int)
df["Term in Months"]=(df["Term in Months"]*12)
df["Bank_Product_Type"]="Term Deposits"

###########################################################################
df03=df3[0:1]
df03= df03.rename(columns={0: 'Bank_Product_Name'})
df04=df3[3:4]
df04= df04.rename(columns={0: 'Bank_Product_Name',1: 'Balance',2: 'Interest',3: 'AER'})
df04["Interest"]=(df04["Interest"]*100).astype(str)+'%'
df04["AER"]=df04["Interest"]
df04["Bank_Product_Name"]=df03["Bank_Product_Name"].values
df04.drop(df04.columns[[4]], axis=1, inplace=True)
df03=pd.DataFrame(df04["Bank_Product_Name"].str.split('–').tolist(),columns=["Int","PY"])
df04["Term in Months"]=df03["PY"].values
df03=pd.DataFrame(df04["Term in Months"].str.split(' ').tolist(),columns=["Int","PY",'f'])
df04["Term in Months"]=df03["PY"].values
df04["Term in Months"]=df04["Term in Months"].apply(int)
df04["Term in Months"]=(df04["Term in Months"]*12)
df04["Bank_Product_Type"]="Term Deposits"

df03=df3[12:13]
df03= df03.rename(columns={0: 'Bank_Product_Name'})
df05=df3[15:16]
df05= df05.rename(columns={0: 'Bank_Product_Name',1: 'Balance',2: 'Interest',3: 'AER'})
df05["Interest"]=(df05["Interest"]*100).astype(str)+'%'
df05["AER"]=df05["Interest"]
df05["Bank_Product_Name"]=df03["Bank_Product_Name"].values
df05.drop(df05.columns[[4]], axis=1, inplace=True)

frames = [df01,df02,df,df04,df05]
result=pd.concat(frames)
result['Bank_Product_Type'].fillna("Savings",inplace=True)

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
df_final["Bank_Name"]="Bank of Scotland "
df_final["Bank_Local_Currency"]="GBP"
df_final["Bank_Type"]="Bank"
df_final["Bank_Product"]="Deposits"
df_final["Bank_Offer_Feature"]="Offline"
df_final["Interest_Type"]="Variable"
df_final.to_csv(output_path+"Consolidate_Bank of Scotland_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False )
