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
    #print(twoday_before_yesterday_file)
    #exit()
    data = json.load(open(f'{files_dir}{yesterday_file}')) #yesterday
    data_day1 = json.load(open(f'{files_dir}{day_before_yesterday_file}'))  #current
    data_day2 = json.load(open(f'{files_dir}{twoday_before_yesterday_file}')) #day_before_yesterday
    #, code_test: (float(stock['close'])-float(stock['open']))/float(stock['open'])) 
    #diff_set_day2 = {code: float(stock['close']) - float(stock['open'])  for code, stock in data_day2.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.05  and (float(stock['volume'])/1000 > 4000) } 
    #diff_set = {code: float(stock['close']) - float(stock['open'])  for code, stock in data.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and ( (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.05  and (float(stock['volume'])/1000 > 2000)) }
    diff_set = {}
    curr_set = {}
    '''
    diff_set = {code: float(stock['close']) - float(stock['open'])  for code, stock in data.items() if code == '2454' or code =='5274'or code =='1590' or (code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.03 and float(stock['close'])>5)} 
    diff_set_day1  = {code: float(stock['close']) - float(stock['open'])  for code, stock in data_day1.items() if code == '2454' or code == '5274' or code =='1590' or (code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL'  and float(stock['open']) != 0.0) and  (float(stock['close'])-float(stock['open']))/float(stock['open']) > 0.03) } 
    #diff_set_day1 = {code: (float(stock['close']) - float(stock['open']))/float(stock['open']) for code, stock in data_day1.items() if code != 'id' and stock['close'] != 'NULL' and (stock['open'] != 'NULL' and float(stock['open']) != 0.0)}
    diff_set_sorted = sorted(diff_set.items(), key=lambda x:abs(x[1]), reverse=True)
    '''
    decision_set = []
    predict = ['3037', '8046', '2313', '6269', '4927']
    related = ['3037', '8046', '2313', '3044', '4958','6269', '2383', '3189', '4927']
    for (code, stock) in data.items():
        if code != 'id' and stock['close'] != 'NULL' and stock['open'] != 'NULL' and float(stock['open']) != 0.0  and (code in data_day1) and (code in data_day2) and data_day1[code]['close'] != 'NULL' and data_day1[code]['open'] != 'NULL'  and float(data_day1[code]['open']) != 0.0  and data_day2[code]['close'] != 'NULL' and data_day2[code]['open'] != 'NULL'  and float(data_day2[code]['open']) != 0.0:
            if code == '2454' or code == '1590':
                #curr_set = {
                #    code: float(stock['close']) - float(stock['open']),
                #}
                diff_set[code] = (float(stock['close']) - float(stock['open']))
            elif (float(stock['close'])-float(data_day1[code]['close']))/float(data_day1[code]['close']) > 0.05 and float(stock['close'])>10:
                #print(code)
                if (float(data_day1[code]['close'])-float(data_day2[code]['close']))/float(data_day2[code]['close']) > 0.03 :
                    #curr_set = {
                    #    code: float(stock['close']) - float(stock['open']),
                    #}
                    #diff_set.append(curr_set)
                    diff_set[code] = (float(stock['close']) - float(stock['open']))
            ''' 
            if code in predict:
                data[code]['Open-Close'] = (data[code]['open'] - data[code]['close'])/data[code]['high']
                data[code]['High-Low'] = (data[code]['high'] - data[code]['low'])/data[code]['low']
                data[code]['percent_change'] = data[code]['adj_close'].pct_change()

                data[code]['std_5'] = data[code]['percent_change'].rolling(5).std()
                data[code]['ret_5'] = data[code]['percent_change'].rolling(5).mean()
                data[code]['std_30'] = data[code]['percent_change'].rolling(20).std()
                data[code]['ret_30'] = data[code]['percent_change'].rolling(20).mean()
                data[code]['std_15'] = data[code]['percent_change'].rolling(10).std()
                data[code]['ret_15'] = data[code]['percent_change'].rolling(10).mean()
                data[code]['std_20'] = data[code]['percent_change'].rolling(10).std()
                data[code]['ret_20'] = data[code]['percent_change'].rolling(10).mean()
                data[code]['ema_12'] = data[code]['percent_change'].ewm(12).mean()
                data[code]['ema_26'] = data[code]['percent_change'].ewm(26).mean()
                data[code]['dif'] = data[code]['ema_12'] - data[code]['ema_26']
                data[code]['dem'] = data[code]['dif'].ewm(9).mean()
                data[code]['osc'] = data[code]['dif'] - data[code]['dem']
                for relate in related:
                    #tmp_data = pd.DataFrame(pd.read_csv('./stock_data/stock/stock'+relate+'.csv'))
                    tmp_data = sorted(all_files, key=lambda x:int(x.split('.')[0].replace('-', '')))[day1]
                    tmp_data = tmp_data[relate]
                    scalor=load(f'./mean_save/{relate}.bin')
                    tmp_data = scalor.transform(tmp_data)
                    tmp_data['percent_change'] = tmp_data['adj_close'].pct_change()
                    #stock_data[relate] = data['percent_change'].rolling(5).std()
                    #data[relate] = tmp_data['percent_change'].rolling(1).mean()
                    stock_data[relate] = (data.open - data.close)/data.open           
                    X = data[['Open-Close', 'High-Low', 'percent_change','std_5', 'ret_5','volume', 'ret_20', 'std_20', 'ret_15', 'std_15','osc', '3037', '8046', '2313', '3044', '4958','6269', '2383', '3189', '4927']]
               '''     
    #print(diff_set)
    #print(len(diff_set))
    diff_set_sorted = sorted(diff_set.items(), key=lambda x:abs(x[1]), reverse=True)
    print(diff_set_sorted)
    #exit()
    #print(diff_set_test)
    #print(len(diff_set))
    #print(len(diff_set_day1))
    
    count = 0
    day = 1
    for (code, diff) in diff_set_sorted:
         curr_stock = data[code]
         if code == '2454' or code == '1590':
             day = 5
         else:
             day = 1
         curr_decision = {
             "code": code,
             "life": day,
             "type": "buy" ,
             "weight": 1,
             "open_price": round(float(curr_stock['close'])+float(curr_stock['close'])*0.01,2),
             "close_high_price": round(float(curr_stock['close']) + float(curr_stock['close'])*0.07,2),
             "close_low_price": round(float(curr_stock['close']) - float(curr_stock['close'])*0.01,2)       
         }
         decision_set.append(curr_decision)
         count = count+1
    print(count)
    if not os.path.exists('../commit/'):
        print("x")
        os.makedirs('../commit/')
    json.dump(decision_set, open(f'../commit/{sys.argv[1]}_{sys.argv[1]}.json', 'w'), indent=4)


