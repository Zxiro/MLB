import os
import csv
import pandas as pd
import numpy as np
import requests as req
from io import StringIO
from datetime import date, timedelta
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
