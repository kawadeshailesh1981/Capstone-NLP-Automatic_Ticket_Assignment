import pandas as pd
import numpy as np

def determinsticgroups():
    column_names = ["Group_ID", "Short_Description", "Description"]
    rulesdf = pd.DataFrame(columns=column_names)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_35', 'Short_Description': 'need access to erp', 'Description': 'need access to'},ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_38', 'Short_Description': 'delete the charm', 'Description': 'project fy_13'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_39', 'Short_Description': 'space available', 'Description': 'memotech space consumed'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_43', 'Short_Description': 'shop_floor_app', 'Description': 'production order number'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_46', 'Short_Description': 'erp', 'Description': 'nx9'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_51', 'Short_Description': 'product selector', 'Description': 'credit component monitoring_tool'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_54', 'Short_Description': 'logical warehouse', 'Description': 'reduce stock level'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_55', 'Short_Description': 'finance_app', 'Description': 'how to run the report from finance_app'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_57', 'Short_Description': 'failed in job_scheduler', 'Description': 'i was able to access this before'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_58', 'Short_Description': 'job qeue', 'Description': 'job processor'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_61', 'Short_Description': 'internal error: unable to find any processes', 'Description': 'calibration system'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_64', 'Short_Description': 'change in report', 'Description': 'not an otc report only used by your finance team'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_66', 'Short_Description': 'installing cutview', 'Description': 'update cutview'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_67', 'Short_Description': 'complete forecast', 'Description': 'complete my forecast'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_68', 'Short_Description': 'expense report not working', 'Description': 'expense report will not submit'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_69', 'Short_Description': 'repeat outbound connection for 135/tcp', 'Description': 'expense report will not submit'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_70', 'Short_Description': 'repeat outbound connection for 135/tcp', 'Description': 'create signature'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_71', 'Short_Description': 'na production files not received', 'Description': 'not received the production feed files'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_72', 'Short_Description': 'update to anftgup nftgyair', 'Description': 'account locked'}, ignore_index=True)
    rulesdf = rulesdf.append({'Group_ID': 'GRP_73', 'Short_Description': 'sso portal on the hub', 'Description': 'oneteam sso not working'}, ignore_index=True)
    return rulesdf

def removedeterminsticgroups(df):
    rulesdf = determinsticgroups()
    #df.drop((rulesdf['Description'].str.contains(describe, re.compile('regex_pattern')) & df['Short description'].str.contains(short_describe, re.compile('regex_pattern'))), inplace = True)
    indexNames = df[df['Assignment group'].isin(rulesdf['Group_ID'])].index
    df.drop(indexNames, inplace=True)
    return df

def determinegroup(shortdesc, desc):
    groupid = ''
    rulesdf = determinsticgroups()
    for ind in df.index:
        ispresent = ((rulesdf['Description'][ind] in desc)&(rulesdf['Short_Description'][ind] in shortdesc))
        #print(ispresent)
        if(ispresent):
            groupid = rulesdf['Group_ID'][ind]
    return groupid