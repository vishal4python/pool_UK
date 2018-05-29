import subprocess as sp
from maks_lib import log_config
from maks_lib import logpath
import logging
import time
import concurrent.futures
start_time = time.time()
# banks = glob.glob("*.py")



Bank_Names = ['reading_vba_files_uk.py','BOI_Final.py','Bank_of_scotland_Deposits.py','bank_of_virgin_mortgage.py','Virgin_Bank_Deposits_New.py',
'barclays_deposite.py','barclays_mortgage.py',
'co_operative_bank_deposits.py','co_operative_bank_mortgage.py',
'hailfax.py','hailfax_mortgage.py','HSBC.py','HSBC_bank_mortgage_v2.py','Lloyds.py','Lloyds_mortgage.py','MoneyMarket_deposits.py','MoneyMarket_mortgage.py',
'mertobank_deposits_v2.py','metrobank_mortgage_v2.py',
'CompareTheMarket.py','CompareTheMarket_Mortgage.py','royal_bank_scotland_deposits.py','royal_bank_scotland_mortgage.py','Uk_Deposits.py','Uk_Mortgage.py',
'santander_mortgage_v2.py','santander_deposits_v2.py',
'TSB_bank_deposits.py','TSB_bank_mortgage.py','Natwest_Data_Deposit.py','Natwest_Data_Mortgage.py',
'clydesdale_deposits_v2.py','clydesdale_mortgage_v2.py']


# log_config(logpath, "UK_BANK_RUNStatus".format(), __doc__)
def runBank(bankName):
    print(bankName)
    # log_config(logpath, "UK_BANK_RUNStatus".format(), __doc__)
    logging.info("Web-Scrapping Starting for bank: {}\n".format(bankName))
    cmd = "python " + bankName
    stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
    if 0 == stdout.returncode:
        logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bankName))
    else:
        logging.error('Got: Error for bank: {}\n'.format(bankName))


# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(runBank, bankName): bankName for bankName in Bank_Names}
    for future in concurrent.futures.as_completed(future_to_url):
        resp = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print( exc)
print('End Time:', (time.time()-start_time)/60, 'min')



try:
    consolidated_banks = ['Final_Consolidated_Deposits_UK.py','Final_Consolidation_MORTGAGE_UK.py']

    log_config(logpath, "UK_BANK_RUNStatus".format(), __doc__)
    for bank in consolidated_banks:
        logging.info("Web-Scrapping Starting for bank: {}\n".format(bank))
        cmd = "python "+ bank
        stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
        if 0 == stdout.returncode:
            logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bank))
        else:
            logging.error('Got: Error for bank: {}\n'.format(bank))
except Exception as e:
    print(e)

try:
    aggregator_banks = ['Agg_UK_Deposit.py','Agg_UK_Mortgage.py']

    log_config(logpath, "UK_BANK_RUNStatus".format(), __doc__)
    for bank in aggregator_banks:
        logging.info("Web-Scrapping Starting for bank: {}\n".format(bank))
        cmd = "python "+ bank
        stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
        if 0 == stdout.returncode:
            logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bank))
        else:
            logging.error('Got: Error for bank: {}\n'.format(bank))

except Exception as p:
    print(p)

try:
    uk_bank_and_agg = ['UK_bank_and_agg.py']

    log_config(logpath, "UK_BANK_RUNStatus".format(), __doc__)
    for bank in uk_bank_and_agg:
        logging.info("Web-Scrapping Starting for bank: {}\n".format(bank))
        cmd = "python "+ bank
        stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
        if 0 == stdout.returncode:
            logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bank))
        else:
            logging.error('Got: Error for bank: {}\n'.format(bank))

except Exception as c:
    print(c)