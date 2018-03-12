#!/usr/bin/env python
"""
Purpose     : Write all commonly used scripts here

        #####################     Change log   ###############################
        ##------------------------------------------------------------------##
        ##  Author              ##Date                ##Current Version     ##
        ##------------------------------------------------------------------##
        ## Moody's Analytics    ##27th FEB,2017       ##V1.0                ##
        ##------------------------------------------------------------------##
        ######################################################################
        Date              Version     Author      Description
        27th Feb,2017     v 0.1       Deepak      Logging
"""

import datetime
import logging
from os import path

logpath = path.join(path.dirname(path.dirname(path.realpath(__file__))), "logs\\")
output_path = path.join(path.dirname(path.dirname(path.realpath(__file__))), "data\output\\")
input_path = path.join(path.dirname(path.dirname(path.realpath(__file__))), "data\input\\")


def log_config(logpath,log_file_name,change_log):
    """
    Purpose: This function will Configure Log file

    Args: Absolute path of 'logfile'

    Returns: Log File Path
    You can refer following examples for logging the context.
     logging.debug('This message will get printed in log file')
     logging.info('This message will get printed in log file')
     logging.warning('This message will get printed in log file')
     Logging.error('This message will get printed in log file')
     Logging.critical('This message will get printed in log file')

    """

    now = datetime.datetime.now()
    today = now.strftime("%d-%m-%Y")
    time_stamp = today + "_" + now.strftime("%H-%M-%S")
    logfile = logpath +log_file_name+ "_" + time_stamp + ".log"
    #Logging the Doc String
    with open(logfile,mode= 'a') as ftr:
        ftr.write(change_log+"\n\n")
    #Log Configuration
    logging.basicConfig(filename=logfile,level=logging.DEBUG,
                        format='%(asctime)s- %(name)-12s - %(levelname)-8s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.info('Starting the program execution\n')
    return logfile



