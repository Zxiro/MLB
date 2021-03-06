import csv
import datetime
import os
import json
import sys
import numpy as np
import pandas as pd
from statistics import mean
from sklearn import preprocessing
from add_feature import Add_feature
from build_config import index_dic
from build_config import stock_dic
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]=""

def resha(x): #(week, day, features) reshape into (week*day, features) -> (total days, features)
    nptrain = np.array(x)
    nptrain = np.reshape(nptrain,(nptrain.shape[0] * nptrain.shape[1], nptrain.shape[2]))
    return nptrain

def seperate_tr_te(lis):
    te = lis[-90:]
    tr = lis[:-90]
    return tr, te

def save_np(x, y, num, span, open_price, close_price, ordinary):
    scale = preprocessing.StandardScaler()
    train_x, x_test = seperate_tr_te(x)
    train_y, y_test = seperate_tr_te(y)
    open_price = open_price[-90:]
    close_price = close_price[-90:]
    stock_name = num
    ordinary = ordinary[-90:]
    scale = scale.fit(resha(train_x))  #  standard scale, resha(x) = two dim /  (tr + te)
    x_test = scale.transform(resha(x_test)) # two dim standardlized
    train_x = scale.transform(resha(train_x))
    #pca = PCA(n_components=3)
    #transformed = pdpca.transform(x_test)
    train_x, x_val, train_y, y_val = train_test_split(train_x, train_y, test_size=0.2)

    Npdata = ordinary
    x = np.save(os.path.join('./stock_data/low_val/', 'low_val_x_' + stock_name + '.npy'), Npdata)
    #print(Npdata)
    print(num ," low_val_x_: ", Npdata.shape)

    Npdata = x_val
    x = np.save(os.path.join('./stock_data/vax/', 'val_x_' + stock_name + '.npy'), Npdata)
    #print(Npdata)
    print(num ," val_x_: ", Npdata.shape)

    Npdata = y_val
    x = np.save(os.path.join('./stock_data/vay/', 'val_y_' + stock_name + '.npy'), Npdata)
    #print(Npdata)
    print(num ," val_y_: ", Npdata.shape)

    Npdata = train_x
    x = np.save(os.path.join('./stock_data/trx/', 'train_x_' + stock_name + '.npy'), Npdata)
    #print(Npdata)
    print(num ," train_x_: ", Npdata.shape)

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
    print(num, " opentestx  ", npdata.shape)
    #print(npdata)
    npdata = np.array(close_price)
    np.save(os.path.join('./stock_data/trx/', 'close_x_' + stock_name), npdata)
    print(num, " closetestx  ", npdata.shape)
    #print(npdata)

def generate_train_in_day(stock_data, stock_num):
    train_x = []
    train_y = []
    open_price = []
    close_price = []
    span = 1
    name = stock_num
    print(stock_data.shape)
    stock_data.drop(['date'], axis = 1, inplace = True)
    #for i in stock_data.columns:
    #    stock_data[i] = pd.to_numeric(stock_data[i])
    ordinary = (pd.to_numeric(stock_data['pe_com'])-pd.to_numeric(stock_data['pe_i']))/pd.to_numeric(stock_data['pe_i'])  #原本離區間的距離
    one_month = (pd.to_numeric(stock_data['pe_com'].shift(-10))- pd.to_numeric(stock_data['pe_i'].shift(-10)))/pd.to_numeric(stock_data['pe_i'].shift(-20))
    y = np.where(ordinary >=0,np.where((ordinary - one_month)>=0.05,1,0),np.where((one_month - ordinary)>=0.05,1,0)) #公司本益比相較於產業本益比的變動超過5% 
    train_y = y[:-10]
    for i in range(len(stock_data)):#everyday
        if i < len(stock_data) and ((i + span) < len(stock_data)):
            train_x.append([stock_data.iloc[i+j].values.tolist() for j in range(span)])
            i += span
            Open = stock_data.iloc[i]['open']
            Close = stock_data.iloc[i]['close']
            open_price.append(Open)
            close_price.append(Close)
    train_x = train_x[:-(10-span)]
    #print(train_x)
    print(len(train_y))
    print(len(train_x))
    save_np(train_x, train_y, stock_num, span, open_price, close_price, ordinary)

def filter_feature(df, feature):
    df = df[df.columns[df.columns.isin(feature)]] #篩選出需要的feature
    return df

def load_csv(num, start, end):
    stock_data = pd.DataFrame(pd.read_csv('./stock_data/stock/stock'+num+'.csv'))
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    return stock_data

def concat_indust_pe(df, dict_, choose):
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
    df[choose+'_i'] = pe
    df = df[~(df == 0.0).any(axis=1)]
    #print(df)
    #print(dict_)

def concat_pe(df, stock_num):
    dirPath = r"./pe_data"
    result = [f for f in sorted(os.listdir(dirPath)) if os.path.isfile(os.path.join(dirPath, f))]
    pe_dict = {}
    for file_name in result:
        date = file_name.split('.')[0]
        ex_filename = file_name.split('.')[1]
        if(len(date)==8 and date[0]=='2' and ex_filename == "json"):
            with open(dirPath+ '/' + date +'.json') as f:
                        pe_day_dict = json.load(f)
            if stock_num in pe_day_dict.keys():
                pe_dict[date] = pe_day_dict[stock_num]
            #print(date)
    #print(pe_dict)
    pe = []
    #print(pe_dict.keys())
    for i in range(len(df.index)-1):
        date = df.iloc[i]['date']
        yr = date.year
        m = date.month
        day = date.day
        if(m < 10):
            m = '0' + str(m)
        if(day<10):
            day = '0' + str(day)
        date = str(yr)+str(m)+str(day)
        if date in pe_dict.keys():
            #print(date, pe_dict[date])
            if(pe_dict[date]=='-'):
                pe.append(0)
            else:
                pe.append(pe_dict[date])
        else:
            #print(date)
            pe.append(0)
    pe.append(0)
    #print(pe)
    df['pe_com'] = pe
    #print(df[2489:])
    df = df[~(df == 0.0).any(axis=1)]
    #print(df)
    return df
    #print(dict_)

if '__main__' == __name__:
    stock_num = stock_dic['stock_num']
    feature = stock_dic['features']
    span = stock_dic['span']
    close_type = stock_dic['close_type']
    start_date = stock_dic['date']
    end_date = stock_dic['end_date']
    stock_group = index_dic['stock_group'] #stock
    indust = index_dic['indust'] #indust cate
    indust_pe = []
    df_list = []
    #stock_num = sys.argv[1]
    stock_num = '1301'
    stock_data = load_csv(stock_num, start_date, end_date) #load selected stock's data which is in the set timespan
    af = Add_feature(stock_data) #calculate the wanted feature and add on the stock dataframe
    af.data = filter_feature(af.data, feature) #leave the wanted feature
    df = af.data
    #df = pd.DataFrame(stock_data)
    df = df.dropna()
    allratio = ['pe', 'pbr', 'yield']
    for ratio in allratio:
        indust_pe = []
        for ind in indust:
            #print(ind)
            with open('./indust_pe/'+ ind + ratio +'.json') as f:
                indust_dict = json.load(f)
            indust_pe.append(indust_dict)
        concat_indust_pe(df, indust_pe[0], ratio)
    df = concat_pe(df, stock_num)
    avg = []
    for i in range(len(df)):#everyday
        if i > 9:
            tmp = 0
            for j in range(10):
                if(df.iloc[i-j]['pe_com']=='-'):
                    tmp+=0
                else:
                    tmp += float(df.iloc[i-j]['pe_com'])
            avg.append(tmp/10)
        else:
            avg.append(0)
    df['pe_avg'] = avg
    df = df.dropna()
    print(df)
    generate_train_in_day(df,stock_num)
