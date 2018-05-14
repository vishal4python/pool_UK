import csv
import pandas as pd
import numpy as np
from tabulate import tabulate


def csvValidator(inputFilePath, outputFilePath, jsonValidation):
    f = open(inputFilePath, 'r')
    reader = csv.reader(f)
    headers = next(reader)
    column = {}
    for h in headers:
        column[h] = []
    for row in reader:
        for h, v in zip(headers, row):
            column[h].append(v)
    validation = jsonValidation
    row_name = validation.get('row_name', None)
    table_headers = ['Error Location', 'Error Type', 'Row Number', 'Value', 'Column Name',row_name if row_name is not None else '']
    errorData = []
    errorData.append(table_headers)

    if row_name is not None:
        row_name = column[row_name]
    for validationKey in validation.keys():
        keyFound = column.get(validationKey, None)
        if keyFound is not None:
            obj = validation[validationKey]
            for j, i in enumerate(column[validationKey]):
                replace_with = obj.get('replace_with', None)
                if replace_with is not None:
                    for rep in replace_with:
                        i = i.replace(rep[0],rep[1])
                _strip = obj.get('strip', None)
                if _strip is not None:
                    if i is not None:
                        for st in _strip:
                            i = i.strip(st)

                skip = obj.get('skip', None)
                if skip is not None:
                    skipFound = False
                    for sk in skip:
                        if i is not None:
                            if len(i) == len(sk):
                                skipFound = True
                                break
                        if i == sk:
                            skipFound = True
                            break
                    if skipFound:
                        continue

                _type = obj.get('type', None)
                if _type is not None:
                    if _type == 'float':
                        try:
                            if '.' in str(i):
                                float(i)
                            else:
                                errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey, row_name[j] if row_name is not None else None])
                                continue

                        except:
                            errorData.append(['typeFieldError', 'Type Not Found', j+2,i, validationKey,row_name[j] if row_name is not None else None])
                            continue
                    elif _type == 'int':
                        try:
                            if '.' not in str(i):
                                int(i)
                            else:
                                errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey,row_name[j] if row_name is not None else None])
                                continue
                        except:
                            errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey,row_name[j] if row_name is not None else None])
                            continue
                    elif _type == 'string':
                        try:
                            str(i)
                        except:
                            errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey,row_name[j] if row_name is not None else None])
                            continue
                    elif _type == 'date':
                        try:
                            if i is not None:
                                if str(i).count('-')!=2:
                                    # print('j', j)
                                    # print('j =', row_name[j + 2])
                                    errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey,row_name[j] if row_name is not None else None])
                                    continue
                        except:
                            # print('j =' , row_name[j])
                            errorData.append(['typeFieldError', 'Type Not Found', j + 2, i, validationKey,row_name[j] if row_name is not None else None])
                            continue
                _allowed = obj.get('allowed',None)

                if _allowed is not None:
                    if len(_allowed)!=0:
                        _allowed = [str(allow).strip() for allow in _allowed]
                        if str(i) not in _allowed:
                            errorData.append(['allowedFieldError', 'Value Not found', j + 2,i, validationKey,row_name[j] if row_name is not None else None])
                            continue

                _required = obj.get('required', None)
                if _required is not None:
                    if i is None:
                        errorData.append(['requireFieldError', 'Filed Not Found', j+2, i, validationKey,row_name[j] if row_name is not None else None])
                        continue
                    elif len(str(i))==0:
                        errorData.append(['requireFieldError', 'Filed Not Found', j + 2, i, validationKey,row_name[j] if row_name is not None else None])
                        continue
                    elif np.nan == i:
                        errorData.append(['requireFieldError', 'Filed Not Found', j + 2, i, validationKey,row_name[j] if row_name is not None else None])
                        continue

        elif validationKey =='compare':

            compare = column[validation['compare']['compare']]
            compare_with = column[validation['compare']['compare_with']]
            for id ,comp in enumerate(zip(compare,compare_with)):
                c1, c2 = comp
                if c1 is not None and c2 is not None:
                    if len(c1) !=0 and len(c2)!=0:
                        try:
                            c = [k.strip('%') for k in [c1,c2]]
                            c = [float(k.strip('%')) for k in c]
                            cmpValue = abs(c[0] - c[1])
                            difference = validation['compare'].get('difference', None)
                            if difference is not None:
                                if float(difference) < cmpValue:
                                        print(cmpValue)
                                        errorData.append(['Comparison Error', 'More Than Expected Value', id + 2, c, validation['compare']['compare_with'], row_name[id] if row_name is not None else None])
                        except Exception as e:
                            errorData.append(['Comparison Error', 'Not Possible to compare the give Two values', id + 2, c,validation['compare']['compare_with'], row_name[id] if row_name is not None else None])
            print(compare)
            print(compare_with)
        elif validationKey == 'match':
            name = column[validation['match']['name']]
            Ticker = column[validation['match']['ticker']]
            match_list = validation['match'].get('match_list', None)
            if match_list is not None:
                for id, comp in enumerate(zip(name, Ticker)):
                    if list(comp) not in match_list:
                        print(list(comp))
                        errorData.append(['Expectation Error', 'Expected data not Found', id + 2, list(comp),[validation['match']['name'],validation['match']['ticker']],row_name[id] if row_name is not None else None])
            else:
                print('Match list data not found.')
        else:
            print(validationKey,'Not Found. Please Check column Name.')
    print(tabulate(errorData))
    df = pd.DataFrame(errorData[1:], columns=table_headers)
    df.to_csv(outputFilePath, index=False)


if __name__ == '__main__':
    validation = {
        'row_name':'Bank_Name',

        'Date':{
            'type': 'date',
            'required': True
        },
        'Bank_Native_Country':{
            'type':'string',
            'allowed':['UK'],
            'required':True
        },
        'State':{
            'type':'string',
            'allowed':['London'],
            'required':True
        },
        'Bank_Name':{
            'type':'string',
            'allowed':['The Co-operative Bank', 'Bank of Ireland', 'Bank of Scotland', 'Halifax', 'Lloyds Bank', 'NatWest', 'Royal Bank Of Scotland', 'Virgin Money Plc'],
            'required':True
        },
        'Ticker':{
            'type':'string',
            'allowed':['Private', 'BIRG', 'Private', 'Private', 'LLOY', 'NWBD', 'RBS', 'VM'],
            'required':True
        },
        'Bank_Local_Currency':{
            'type':'string',
            'allowed':['GBP'],
            'required':True
        },
        'Bank_Type':{
            'type':'string',
            'allowed':['Bank'],
            'required':True
        },
        'Bank_Product': {
            'type': 'string',
            'allowed': ['Deposits'],
            'required': True
        },
        'Bank_Product_Type': {
            'type': 'string',
            'allowed': ['Savings', 'Term Deposits', 'Current'],
            'required': True
        },
        'Bank_Product_Code': {
            'type': 'string',
            'required': True
        },
        'Bank_Product_Name': {
            'type': 'string',
            'required': True
        },
        'Minm_Balance':{
            'type':'int',
            'skip':['']
        },
        'Maxm_Balance': {
            'type': 'int',
            'skip': ['']
        },
        'Bank_Offer_Feature':{
            'type':'string',
            'allowed':['Offline', 'Online'],
            'required':True
        },
        'Term_in_Months':{
            'type':'int',
            'allowed':[6,12,36],
            'skip':['']
        },
        'Interest_Type':{
            'type':'string',
            'allowed':['Variable', 'Fixed'],
            'required':True
        },
        'Interest':{
            'type':'float',
            'skip':[''],
            'strip':['%'],
        },
        'AER': {
            'type': 'float',
            'skip': [''],
            'strip': ['%'],
        },
        'compare': {
            'compare': 'AER',
            'compare_with': 'Interest',
            'difference': '0.01'
        },
        'match': {
            'name': 'Bank_Name',
            'ticker': 'Ticker',
            'match_list': [['The Co-operative Bank', 'Private'], ['Bank of Ireland', 'BIRG'], ['Bank of Scotland', 'Private'], ['Halifax', 'Private'],
                           ['Lloyds Bank', 'LLOY'], ['NatWest', 'NWBD'], ['Royal Bank Of Scotland', 'RBS'], ['Virgin Money Plc', 'VM'],
                           ]
        },
        'match': {
            'name': 'Bank_Product_Type',
            'ticker': 'Bank_Product_Code',
            'match_list': [['Savings', '_MSBF'],
                           ['Savings', '6MSBF'],
                           ['Savings', '12MSBF'],
                           ['Savings', '24MSBF'],
                           ['Savings', '36MSBF'],
                           ['Term Deposits', '6MCDF'],['Term Deposits', '12MCDF'],['Term Deposits', '24MCDF'],
                           ['Term Deposits', '36MCDF'],
                           ['Term Deposits', '_MCDF'],
                           ['Current', '_MCCF']
                                  ]}
         }
    path = 'C:\\Users\\doddsai\\Desktop\\uk deposits\\UK_Deposits_Data_2018_03_20.csv'
    output = 'C:\\Users\\doddsai\\Desktop\\uk deposits\\error.csv'
    csvValidator(path, output, validation)
# Interest: Ally, Synchory and SunTrust if available check it, else ignore the errors
#Interest: for aggregator websites if available check it, else ignore the errors (except us.deposits.org)

# Compare the bank name and Ticker
# compare and publish if Interest and APY difference is more than 1%
