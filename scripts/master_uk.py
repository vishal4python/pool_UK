"""
Purpose     : Extract data for UK Banks

        #####################     Change log   ###############################
        ##------------------------------------------------------------------##
        ##  Author              ##Date                ##Current Version     ##
        ##------------------------------------------------------------------##
        ## Moody's Analytics    ##16th March,2018    ##V1.0                ##
        ##------------------------------------------------------------------##
        ######################################################################
        Date                   Version     Author      Description
        16th March,2018        v 0.1       Deepak      Initial development
"""
import glob
import subprocess as sp
from maks_lib import log_config
from maks_lib import logpath
import logging
banks = glob.glob("*.py")
Bank_Names = ['Bank_of_scotland_Deposits.py','bank_of_virgin_deposits.py','bank_of_virgin_mortgage.py','BOI_Final.pdf.py',
'co_operative_bank_deposits.py','co_operative_bank_mortgage.py','hailfax.py','hailfax_mortgage.py','Lloyds.py',
'Lloyds_mortgage.py','Natwest_Data_Deposit.py','Natwest_Data_Mortgage.py','royal_bank_scotland_deposits.py',
'royal_bank_scotland_mortgage.py']

log_config(logpath, "UK_BANK_RUNStatus".format(), __doc__)
for bank in Bank_Names:
    logging.info("Web-Scrapping Starting for bank: {}\n".format(bank))
    cmd = "python "+ bank
    stdout = sp.run(cmd, shell=True, stdout=sp.PIPE)
    if 0 == stdout.returncode:
        logging.info("Succesfully Web-Scrapping completed for bank: {}\n".format(bank))
    else:
        logging.error('Got: Error for bank: {}\n'.format(bank))
