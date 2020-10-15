import csv
import datetime
import os
import numpy as np
import pandas as pd
from statistics import mean
from sklearn import preprocessing
from add_feature import Add_feature
from get_usa_data import get_usa_index
from get_chip_data import get_chip_csv
from build_config import index_dic
from build_config import stock_dic
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]=""

def resha(x): #(week, day, features) reshape into (week*day, features) -> (total days, features)
    nptrain = np.array(x)
    nptrain = np.reshape(nptrain,(nptrain.shape[0] * nptrain.shape[1], nptrain.shape[2]))
    return nptrain

def seperate_tr_te(List):
    te = List[-50:]
    tr = List[:-50]
    return tr, te

def save_np(x, y, num, span):
    scale = preprocessing.StandardScaler()
    train_x, x_test = seperate_tr_te(x)
    train_y, y_test = seperate_tr_te(y)
    # open_money = open_money[-50:]
    stock_name = num

    scale = scale.fit(resha(train_x))  #  標準化後的標準scale, resha(x) = two dim /  (tr + te)

    with open('./csv_data/mean_var.csv', 'w', newline='')as csvfile:
        writer = csv.writer(csvfile, delimiter = ' ')
        writer.writerow(['平均', '變異數'])
        writer.writerow([stock_dic['date'], stock_dic['end_date'], scale.mean_, scale.var_])

    x_test = scale.transform(resha(x_test)) # two dim standardlized
    train_x = scale.transform(resha(train_x))

    x_test = x_test.reshape((int(x_test.shape[0]/span), span, -1)) # return to three dim
    train_x  = train_x.reshape((int(train_x.shape[0]/span), span, -1))

    Npdata = train_x
    np.save(os.path.join('./stock_data/trx/', 'train_x_' + stock_name), Npdata)
    print(num ," trainX: ", Npdata.shape)
    #print(Npdata)

    Npdata = x_test
    np.save(os.path.join('./stock_data/tex/', 'test_x_' + stock_name), Npdata)
    print(" testX: ", Npdata.shape)
    #print(Npdata)

    Npdata = np.array(train_y)
    np.save(os.path.join('./stock_data/try/', 'train_y_' + stock_name), Npdata)
    print( " trainY: ", Npdata.shape)
    #print(Npdata)

    Npdata = np.array(y_test)
    np.save(os.path.join('./stock_data/tey/', 'test_y_' + stock_name), Npdata)
    print(" testY: ", Npdata.shape)
    #print(Npdata)
    '''Npdata = np.array(open_money)
    np.save(os.path.join('./StockData/TrainingData/', 'opentestingX_' + stock_name), Npdata)
    #print(num, " opentestX  ", Npdata.shape)
    #print(Npdata)'''
def generate_train_in_day(feature, data, name, span):
    gen_x = []
    gen_y = []
    train_x = []
    train_y = []
    data.drop(['date'], axis = 1, inplace = True)
    gen_x = data.drop(data.index[-1])
    gen_y = data.drop(data.index[0])
    for i in range(len(gen_x)):#everyday
        if i < len(gen_x) and ((i + span) < len(gen_x)):
            train_x.append(list(gen_x.iloc[i+j] for j in range(span)))
            i += span
            Open = gen_y.iloc[i]['open']
            Close = gen_y.iloc[i]['close']
            train_y.append(Open-Close)#the next day's diff

    save_np(train_x, train_y, name, span)

def filter_feature(df, feature):
    df = df[df.columns[df.columns.isin(feature)]] #篩選出需要的feature
    print(df)
    return df

def load_csv(num, start, end):
    stock_data = pd.DataFrame(pd.read_csv('./stock_data/stock'+num+'.csv'))
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    for i in stock_data["date"]:
        if( start_date > i or end_date < i):
            stock_data.drop([count], axis = 0, inplace = True)
        count = count + 1
    stock_data = stock_data.reset_index(drop = True)
    return stock_data

if '__main__' == __name__:
    stock_num = stock_dic['stock_num']
    feature = stock_dic['features']
    span = stock_dic['span']
    start_date = stock_dic['date']
    end_date = stock_dic['end_date']
    
    stock_data = load_csv(stock_num, start_date, end_date) #load selected stock's data which is in the set timespan
    usa = get_usa_index() #get usa index data
    chip_data = get_chip_csv("0050", 3) #get "0050"'s chip data in past three days
    af = Add_feature(stock_data) #calculate the wanted feature and add on the stock dataframe
    af.data = filter_feature(af.data, feature) #leave the wanted feature
    df = pd.concat([af.data, usa], axis=1).reindex(af.data.index) #concat the USA index on the data
    df = pd.concat([df, chip_data], axis=1).reindex(df.index) #concat the chip on the data
    df = df.dropna()
    print(df)
    print('------------------------')
    df.to_csv('./csv_data/train.csv')
    #df = df.set_index('date').resample('w')
    generate_train_in_day(feature, df, stock_num, span)
