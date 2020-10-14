#!/usr/bin/env python
#coding=utf-8
# standard import
import json
import os
import sys

# third-party import
import xgboost
import csv
import time
import requests as req
import numpy as np
import pandas as pd
from io import StringIO
from datetime import date, timedelta
from pandas.io.json import json_normalize


def get_chip_csv(stock_id):
    for i in range(3):
        day = (date.today()-timedelta(days = i)).strftime("%Y%m%d")
        print(day)
        tse_csv = req.get('https://www.twse.com.tw/fund/T86?response=csv&date='+day+'&selectType=ALLBUT0999')
        try:
            df = pd.read_csv(StringIO(tse_csv.text), header = 1, encoding = 'utf-8').dropna(how='all', axis=1).dropna(how='any')
        except Exception:
            i+=1
            print("e")
            continue
        except IndexError:
            i+=1
            print("i")
            continue
        except ValueError:
            i+=1
            print("v")
            continue
        df['tmp'] = df.iloc[:, 0:1]
        df['stock_id'] = df['tmp'].str.replace('=','').str.replace('"','')
        df['inv_trust'] = df.iloc[:, 10:11]
        df['dealer'] = df.iloc[:, 11:12]
        df['foregin_inv'] = df.iloc[:, 7:8]
        df['total_inv_overview'] = df.iloc[:, 18:19]
        df.drop(df.columns[ :-5],inplace = True, axis = 1)
        mask = (df['stock_id'] == stock_id)
        print(df[mask])
        time.sleep(2)

if '__main__' == __name__:
    files_dir = '/home/mlb/res/stock/twse/json/'# file direction
    all_files = [] 
    for (dirpath, dirnames, filenames) in os.walk(files_dir):
        all_files.extend(filenames)
    get_chip_csv("2603")
    day_before_yesterday_file = sorted(all_files, key = lambda x:int(x.split('.')[0].replace('-', '')))[-2]
    yesterday_file = sorted(all_files, key = lambda x:int(x.split('.')[0].replace('-', '')))[-1]
    yes_data = json.load(open(f'{files_dir}{yesterday_file}')) 
    day_be_yes_data = json.load(open(f'{files_dir}{day_before_yesterday_file}'))
    #code -> ªÑ¸¹
    diff_set = {code: float(stock['close']) - float(stock['open']) for code, stock in data.items() if code != 'id' and stock['close'] != 'NULL' and stock['open'] != 'NULL'}
    
    diff_set_sorted = sorted(diff_set.items(), key=lambda x:abs(x[1]), reverse = True)
    decision_set = []
    #diff the prcie difference
    
    #~~~~~~~~~~ insert model to decie the proce



    #~~~~~~~~~~
    for (code, diff) in diff_set_sorted[:10]: #[:10] take final 10 stocks
        curr_stock = data[code]
        curr_decision = {
	    "code": code,
	    "life": 3,#if condition doesn;t happen it wi;; sell after 3 day with close price
	    "type": "buy" if diff > 0 else "short",
	    "weight": 1,
	    "open_price": float(curr_stock['close']),
	    "close_high_price": float(curr_stock['close']) + abs(diff),
	    "close_low_price": float(curr_stock['close']) - abs(diff)       
        }
        decision_set.append(curr_decision)
    if not os.path.exists('../commit/'):
        os.makedirs('../commit/')

    json.dump(decision_set, open(f'../commit/{sys.argv[1]}_{sys.argv[1]}.json', 'w'), indent=4)
