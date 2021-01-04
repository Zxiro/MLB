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
    if(len(stock_symbol) != 4):    #只看4位數的股票
        return
    first = 0
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
        else:
            stock_data = pd.concat([stock_data,data],axis=0)
        print(i)
    return stock_data


dirPath = r"/home/db/stock_resource_center/resource/twse/json"   #股票資料位置
'''
此為需要抓取多筆資料可用
stock_symbol = data.keys()
stock_symbol = list(stock_symbol)
stock_symbol.remove('id')
'''

stock_group = index_dic['stock_group']

for stock_symbol in stock_group:
    stock_data = stock_read(stock_symbol, dirPath)
    file_name = "./stock_data/stock/stock"+stock_symbol+".csv"
    stock_data.to_csv(file_name, index=False) #存入csv
    print('getting', stock_symbol, 'data done')