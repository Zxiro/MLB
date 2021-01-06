import sys
import time
import datetime
import json
import os
import numpy as np
import pandas as pd
from datetime import timedelta
from pandas.io.json import json_normalize
from build_config import index_dic

def data_read(dirPath):  #找出資料夾的所有檔案並且回傳檔案列表
    result = [f for f in sorted(os.listdir(dirPath)) if os.path.isfile(os.path.join(dirPath, f))]
    return result

#讀取指定股票的資料
def stock_read(stock_symbol, dirPath):
    result = data_read(dirPath)
    #if(len(stock_symbol) != 4):    #只看4位數的股票
    #    return
    #print(result)
    first = 0
    #stock_data = 0
    k = 0
    for i in result:   #瀏覽每個檔案
        data_locate = os.path.join(dirPath, i)   #檔案名稱
        with open(data_locate, 'r') as f:    #讀取檔案內容
            data = json.load(f)
        data = data.get(stock_symbol)   #抓取所需股票的資訊
        if(data == None): #該檔案沒有此股票資訊
            continue
        #此為插入時間的colume
        data = pd.DataFrame.from_dict(data, orient='index').T
        column = data.columns.tolist()
        column.insert(0, "date")     #插入時間column
        data = data.reindex(columns = column)
        data["date"] = i.split('.')[0] #檔案名字最前面為時間
        #print(data)
        if first == 0: #第一支股票要先建立新的data資訊
            stock_data = data
            first = first + 1
            k = 1
        else:
            stock_data = pd.concat([stock_data,data],axis=0)
        print(stock_data)
    '''
    if(k == 0):
        return None
    '''
    return stock_data


dirPath = r"/home/db/stock_resource_center/resource/twse/json"   #股票資料位置
'''
此為需要抓取多筆資料可用
stock_symbol = data.keys()
stock_symbol = list(stock_symbol)
stock_symbol.remove('id')
'''
if '__main__' == __name__:
    stock_group = index_dic['stock_group']
    #company = ['2302','2303','2329','2330','2337','2338','2342','2344','2351','2363','2369','2379','2388','2401','2408','2436','2441','2449','2451','2454','2458','2481','3006','3014','3016','3034','3035','3041','3054','3094','3189','3257','3413','3443','3530','3532','3545','3583','3588','3661','3711','4919','4952','4961','4967','4968','5269','5285','5305','5471','6202','6239','6243','6257','6271','6415','6451','6525','6531','6533','6552','6573','8016','8028','8081','8110','8131','8150','8261','8271']
    #半導體

    company = ['1301','1303','1304','1305','1307','1308','1309','1310','1312','1313','1314','1315','1321','1323','1324','1325','1326','1337','1340','1341','4306']
    #for stock_symbol in stock_group:
    for stock_symbol in company:
        stock_data = stock_read(stock_symbol, dirPath)
        #if stock_data == None:
        #    continue
        file_name = "./stock_data/stock/stock"+str(stock_symbol)+".csv"
        stock_data.to_csv(file_name, index=False) #存入csv
        print('getting', stock_symbol, 'data done')
