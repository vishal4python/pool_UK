 # Library to be imported
import os, sys
import win32com.client

# Path and file name to be used for opening
path = ("C:\\Users\\vishal\\PycharmProjects\\pool_UK-master\\scripts\\")

# Change to our current directory where macro exists
os.chdir(path)

uk_banks = ["Clydesdale Bank_80per.xlsm","Bank of Ireland_Mortgage.xlsm","SantanderBank_85per.xlsm","MetroBank_80per.xlsm"]

# Run us_banks
for uk_banks in uk_banks:
    if os.path.exists(uk_banks):
        xl=win32com.client.Dispatch("Excel.Application")
        xl.Workbooks.Open(path+str(uk_banks), ReadOnly=1)
    del xl
