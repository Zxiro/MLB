import json
import datetime as dt
import pandas as pd
import yfinance as yf
from pandas_datareader import data as web
from daetime import date, timedelta
def get_usa_index():
    yf.pdr_override()
    usa_dict = 'sp'
    features = ['Close', 'Open', 'High', 'Low', 'Volume']
    start = date.today()-timedelta(days=2)
    end = date.today()
    index_list = []
    for key in usa_dict:
        df = pd.DataFrame(web.get_data_yahoo(key, start, end)) #get the S&P index in past three days
        df = df[df.columns[df.columns.isin(features)]]
        df.rename(columns = { "Open":usa_dict[key]+"_open", "High":usa_dict[key]+"_high", "Low":usa_dict[key]+"_low", "Close":usa_dict[key]+"_close", "Adj Close":usa_dict[key]+"_adj_close"}, inplace = True)
        index_list.append(df)
    df.reset_index(inplace = True)
    df.drop('Date', axis = 1, inplace = True)
    df.drop('Volume', axis = 1, inplace = True)
    print(df)
    print('-------------------------------------')
    return df
