#!/usr/bin/env python

# standard import
import json
import os
import sys

# third-party import
import numpy as np


if '__main__' == __name__:
   
    files_dir = '/home/mlb/res/stock/twse/json/'
    all_files = []
    for (dirpath, dirnames, filenames) in os.walk(files_dir):
        all_files.extend(filenames)
    roi_sum = 0.0
    win = 0
    loss = 0
    n=30
    '''
    for i in range(n):
        day1 = i-n-1
        day2 = i-n-2 
        twoday_before_yesterday_file = sorted(all_files, key=lambda x:int(x.split('.')[0].replace('-', '')))[day2-1]
        day_before_yesterday_file = sorted(all_files, key=lambda x:int(x.split('.')[0].replace('-', '')))[day2]
        yesterday_file = sorted(all_files, key=lambda x:int(x.split('.')[0].replace('-', '')))[day1]
        data_test = json.load(open(f'{files_dir}{yesterday_file}')) #current
        data = json.load(open(f'{files_dir}{day_before_yesterday_file}'))  #yesterday
        data_day2 = json.load(open(f'{files_dir}{twoday_before_yesterday_file}')) #day_before_yesterday
        #, code_test: (float(stock['close'])-float(stock['open']))/float(stock['open'])) 
        #diff_set_day2 = {code: float(stock['close']) - float(stock['open'])  for code, stock in data_day2.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.05  and (float(stock['volume'])/1000 > 4000) } 
        #diff_set = {code: float(stock['close']) - float(stock['open'])  for code, stock in data.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and ( (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.05  and (float(stock['volume'])/1000 > 2000)) }  
        diff_set_day2 = {code: float(stock['close']) - float(stock['open'])  for code, stock in data_day2.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.09 } 
        diff_set = {code: float(stock['close']) - float(stock['open'])  for code, stock in data.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and  (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.09 } 
        diff_set_test = {code: (float(stock['close']) - float(stock['open']))/float(stock['open']) for code, stock in data_test.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL' and float(stock['open']) != 0.0)}
        diff_set_sorted = sorted(diff_set.items(), key=lambda x:abs(x[1]), reverse=True)
        decision_set = []
        #print(diff_set_test)
        roi = 0.0
        count = 0
        for (code, diff) in diff_set_sorted:
            if code in diff_set_day2:
                if code in diff_set_test:
                    roi = roi + diff_set_test[code]
                    count = count + 1
                    #print(diff_set_test[code])
        #print(count)
        if(count!=0):
            roi_sum = roi_sum + float(roi/float(count))
            print(float(roi/float(count)))
        if(roi>0):
            win=win+1
        else:
            loss=loss+1
        #win=win-1
    print(roi_sum)
    print(win)
    print(loss)
    exit()
    '''
    '''below is the forml strategy you can directly copy''' 
    day1 = -1
    day2 = -2 
    twoday_before_yesterday_file = sorted(all_files, key=lambda x:int(x.split('.')[0].replace('-', '')))[day2-1]
    day_before_yesterday_file = sorted(all_files, key=lambda x:int(x.split('.')[0].replace('-', '')))[day2]
    yesterday_file = sorted(all_files, key=lambda x:int(x.split('.')[0].replace('-', '')))[day1]
    data = json.load(open(f'{files_dir}{yesterday_file}')) #yesterday
    data_day1 = json.load(open(f'{files_dir}{day_before_yesterday_file}'))  #current
    data_day2 = json.load(open(f'{files_dir}{twoday_before_yesterday_file}')) #day_before_yesterday
    #, code_test: (float(stock['close'])-float(stock['open']))/float(stock['open'])) 
    #diff_set_day2 = {code: float(stock['close']) - float(stock['open'])  for code, stock in data_day2.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.05  and (float(stock['volume'])/1000 > 4000) } 
    #diff_set = {code: float(stock['close']) - float(stock['open'])  for code, stock in data.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and ( (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.05  and (float(stock['volume'])/1000 > 2000)) }  
    diff_set = {code: float(stock['close']) - float(stock['open'])  for code, stock in data.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.09 and float(stock['close'])} 
    diff_set_day1  = {code: float(stock['close']) - float(stock['open'])  for code, stock in data_day1.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and  (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.09 } 
    #diff_set_day1 = {code: (float(stock['close']) - float(stock['open']))/float(stock['open']) for code, stock in data_day1.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL' and float(stock['open']) != 0.0)}
    diff_set_sorted = sorted(diff_set.items(), key=lambda x:abs(x[1]), reverse=True)
    decision_set = []
    #print(diff_set_test)
    print(len(diff_set))
    print(len(diff_set_day1))
    count = 0
    for (code, diff) in diff_set_sorted:
        if code in diff_set_day1:
            curr_stock = data[code]
            curr_decision = {
                "code": code,
                "life": 1,
                "type": "buy" ,
                "weigth": 1,
                "open_price": float(curr_stock['close'])+10,
                "close_high_price": 10000,
                "close_low_price": float(curr_stock['close']) - abs(diff)       
            }
            decision_set.append(curr_decision)
            count = count+1
    print(count)
    if not os.path.exists('../commit/'):
        print("x")
        os.makedirs('../commit/')
    json.dump(decision_set, open(f'../commit/{sys.argv[1]}_{sys.argv[1]}.json', 'w'), indent=4)


