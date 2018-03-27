import pandas as pd
import numpy as np
import re
import datetime
import warnings
from maks_lib import input_path
from maks_lib import output_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

df0=pd.read_excel(input_path+"hsbc.xlsx",sheet_name="page-2")
df1=pd.read_excel(input_path+"hsbc.xlsx",sheet_name="page-8")
df2=pd.read_excel(input_path+"hsbc.xlsx",sheet_name="page-16")


df01=df0[3:5]
df00=pd.DataFrame(df01["Unnamed: 1"].str.split(' ').tolist(),columns=["Int","PY",'i','j'])
df01["Interest"]=df00["Int"].values
df01["AER"]=df01["Interest"]
df01= df01.rename(columns={2: 'Balance'})
df01['Bank_Product_Name'] = 'Online Bonus Saver'
df01['Bank_Offer_Feature']='Online'
df01.drop(df01.columns[[1,2,3,4]], axis=1, inplace=True)


df02=df1[3:4]
df00=pd.DataFrame(df02["Unnamed: 2"].str.split(' ').tolist(),columns=["Int","PY"])
df02["Interest"]=df00["Int"].values
df02["AER"]=df02["Interest"]
df02= df02.rename(columns={8: 'Balance'})
df02['Balance'] = 'All balances'
df02['Bank_Product_Name'] = 'Flexible Saver'
df02['Bank_Offer_Feature']='Offline'
df02.drop(df02.columns[[1,2,3,4]], axis=1, inplace=True)


df03=df2[3:5]
df00=pd.DataFrame(df03["Unnamed: 2"].str.split(' ').tolist(),columns=["Int","PY"])
df03["Interest"]=df00["Int"].values
df03["AER"]=df03["Interest"]
df03= df03.rename(columns={'Unnamed: 1': 'Balance'})
df03= df03.rename(columns={16: 'Term in Months'})
df03.drop(df03.columns[[2,3,4]], axis=1, inplace=True)
df03["Term in Months"]=3*12
df03['Bank_Product_Name'] = 'Fixed Rate Saver'
df03['Bank_Offer_Feature']='Offline'
df03['Bank_Product_Type']='Term Deposits'


df04=df2[7:9]
df00=pd.DataFrame(df04["Unnamed: 2"].str.split(' ').tolist(),columns=["Int","PY"])
df04["Interest"]=df00["Int"].values
df04["AER"]=df04["Interest"]
df04= df04.rename(columns={'Unnamed: 1': 'Balance'})
df04= df04.rename(columns={16: 'Term in Months'})
df04.drop(df04.columns[[2,3,4]], axis=1, inplace=True)
df04["Term in Months"]=1*12
df04['Bank_Product_Name'] = 'Fixed Rate Saver'
df04['Bank_Offer_Feature']='Offline'
df04['Bank_Product_Type']='Term Deposits'

df05=df2[9:11]
df00=pd.DataFrame(df05["Unnamed: 2"].str.split(' ').tolist(),columns=["Int","PY"])
df05["Interest"]=df00["Int"].values
df05["AER"]=df05["Interest"]
df05= df05.rename(columns={'Unnamed: 1': 'Balance'})
df05= df05.rename(columns={16: 'Term in Months'})
df05.drop(df05.columns[[2,3,4]], axis=1, inplace=True)
df05["Term in Months"]=6
df05['Bank_Product_Name'] = 'Fixed Rate Saver'
df05['Bank_Offer_Feature']='Offline'
df05['Bank_Product_Type']='Term Deposits'

frames = [df01,df02,df03,df04,df05]
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
df_final["Bank_Name"]="HSBC"
df_final["Bank_Local_Currency"]="GBP"
df_final["Bank_Type"]="Bank"
df_final["Bank_Product"]="Deposits"
df_final['Bank_Offer_Feature']=result['Bank_Offer_Feature'].values
df_final["Interest_Type"]="Variable"
df_final['Balance'] = df_final['Balance'].apply(lambda x:re.sub('[^0-9a-zA-Z,.]','',str(x)))
df_final.to_csv(output_path+"Consolidate_HSBC_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False )
