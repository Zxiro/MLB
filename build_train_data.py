import csv
import datetime
import os
import numpy as np
import pandas as pd
import json
from statistics import mean
from sklearn import preprocessing
from build_config import index_dic
from build_config import stock_dic
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]=""

def resha(x): #(week, day, features) reshape into (week*day, features) -> (total days, features)
    nptrain = np.array(x)
    print(nptrain.shape)
    nptrain = np.reshape(nptrain,(nptrain.shape[0] * nptrain.shape[1], nptrain.shape[2]))
    return nptrain

def seperate_tr_te(lis):
    te = lis[-90:]
    tr = lis[:-90]
    return tr, te

def save_np(x, y, num, span, open_price, close_price):
    scale = preprocessing.StandardScaler()
    train_x, x_test = seperate_tr_te(x)
    train_y, y_test = seperate_tr_te(y)
    open_price = open_price[-90:]
    close_price = close_price[-90:]
    stock_name = num
    scale = scale.fit(resha(train_x))  #  standard scale, resha(x) = two dim /  (tr + te)
    with open('./csv_data/mean_var.csv', 'w', newline='')as csvfile:
        writer = csv.writer(csvfile, delimiter = ' ')
        writer.writerow(['mean', 'deviation'])
        writer.writerow([stock_dic['date'], stock_dic['end_date'], scale.mean_, scale.var_])
    x_test = scale.transform(resha(x_test)) # two dim standardlized
    train_x = scale.transform(resha(train_x))
    x_test = x_test.reshape((int(x_test.shape[0]/span), span, -1)) # return to three dim
    train_x  = train_x.reshape((int(train_x.shape[0]/span), span, -1))
    Npdata = train_x
    np.save(os.path.join('./stock_data/trx/', 'train_x_' + stock_name), Npdata)
    # print(num ," train_x_: ", Npdata.shape)
    Npdata = x_test
    np.save(os.path.join('./stock_data/tex/', 'test_x_' + stock_name), Npdata)
    print(" test_x_: ", Npdata.shape)
    # print(Npdata)
    Npdata = np.array(train_y)
    np.save(os.path.join('./stock_data/try/', 'train_y_' + stock_name), Npdata)
    print( " train_y_: ", Npdata.shape)
    # print(Npdata)
    Npdata = np.array(y_test)
    np.save(os.path.join('./stock_data/tey/', 'test_y_' + stock_name), Npdata)
    print(" test_y_: ", Npdata.shape)
    #print(Npdata)
    npdata = np.array(open_price)
    np.save(os.path.join('./stock_data/trx/', 'open_x_' + stock_name), npdata)
    #print(num, " opentestx  ", npdata.shape)
    #print(npdata)
    npdata = np.array(close_price)
    np.save(os.path.join('./stock_data/trx/', 'close_x_' + stock_name), npdata)
    #print(num, " closetestx  ", npdata.shape)
    #print(npdata)

def generate_train_in_day(feature, data, name, span):
    train_x = []
    train_y = []
    open_price = []
    close_price = []
    data.drop(['date'], axis = 1, inplace = True)
    for i in range(len(data)):#everyday
        if i < len(data) and ((i + span) < len(data)):
            train_x.append([data.iloc[i+j].values.tolist() for j in range(span)])
            i += span
            Open = data.iloc[i]['open']
            Close = data.iloc[i]['close']
            open_price.append(Open)
            close_price.append(Close)
            if Close - Open >0:
                train_y.append(1)
            else:
                train_y.append(0)
            #train_y.append(Close-Open)#the next day's diff
    save_np(train_x, train_y, name, span, open_price, close_price)

def filter_feature(df, feature):
    df = df[df.columns[df.columns.isin(feature)]] #篩選出需要的feature
    return df

def load_csv(num, start, end):
    stock_data = pd.DataFrame(pd.read_csv('./stock_data/stock/stock'+num+'.csv'))
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    return stock_data

def concat_indust_pe(df, dict_):
    pe = []
    for i in range(len(df.index)-1):
        date = df.iloc[i]['date']
        #print(date)
        yr = date.year
        m = date.month
        if(m < 10):
            m = '0' + str(m)
        date = str(yr)+str(m)
        if date in dict_.keys():
            pe.append(dict_[date])
        else:
            pe.append(0)
    pe.append(0)
    df['pe_i'] = pe
    df = df[~(df == 0.0).any(axis=1)]
    print(df)
    print(dict_)

if '__main__' == __name__:
    stock_num = stock_dic['stock_num']
    span = stock_dic['span']
    close_type = stock_dic['close_type']
    start_date = stock_dic['date']
    end_date = stock_dic['end_date']
    stock_group = index_dic['stock_group'] #stock
    indust = index_dic['indust'] #indust cate
    indust_pe = []
    df_list = []
    for ind in indust:
        print(ind)
        with open('./indust_pe/'+ ind +'.json') as f:
            indust_dict = json.load(f)
        indust_pe.append(indust_dict)
    stock_num = '2330'
    stock_data = load_csv(stock_num, start_date, end_date) #load selected stock's data which is in the set timespan
    df = pd.DataFrame(stock_data)
    df = df.dropna()
    concat_indust_pe(df, indust_pe[0])