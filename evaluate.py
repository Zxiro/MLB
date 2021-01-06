import os
import sys
import numpy as np
import xgboost as xgb
from build_config import indust_dic
from sklearn.metrics import accuracy_score

#stock_num = sys.argv[1]
model = xgb.XGBClassifier()
indust_list = indust_dic['stock_code']
port = {} #Portfolio
class Stock():
    def __init__(self, code, buy, sell):
        self.code = code
        self.buy_price = buy
        self.sell_price = sell
        self.act = 0 #0 for hold, 1 for sell
#indust_list = ['1301']

total_gain = 0
total_port_size = 0
for i in range(0, 10): #0-10
    if i != 0:
        gain = 0
        port_size = len(port.keys())
        if(port_size != 0):
            sell_stock = []
            for key in port.keys():
                if(port[key].act == 1):
                    #print(sell)
                    sell_stock.append(key)
                    gain += float((port[key].sell_price) - float(port[key].buy_price))/ float(port[key].buy_price)
            tot_gain = gain / (port_size)
            total_gain += gain
            total_port_size += port_size
            print('Period ', i+1, ' gain is ', tot_gain, '%')
            for k in sell_stock:
                port.pop(k)
    if i == 9:
        if(port_size != 0):
            for key in port.keys():
                print('key', key)
                gain += (close_price[-1]- float(port[key].buy_price)) / float(port[key].buy_price)
                print('gain', gain)
            print('size', port_size)
            tot_gain = gain / (port_size)
            print('Holding gain is ', tot_gain, '%')
        print(total_gain/9)
        print(total_port_size)
        exit()
    for stock in indust_list:
        if not os.path.isfile('./xg_model/'+stock+'.model'):
            continue
        model.load_model('./xg_model/'+stock+'.model')#load model
        te_x = np.load('./stock_data/tex/test_x_'+stock+'.npy') 
        te_y = np.load('./stock_data/tey/test_y_'+stock+'.npy')
        open_price = np.load('./stock_data/trx/open_x_'+stock+'.npy')
        close_price = np.load('./stock_data/trx/close_x_'+stock+'.npy')
        low_val = np.load('./stock_data/low_val/low_val_x_'+stock+'.npy')
        y_pred = model.predict(te_x)
        pred = y_pred[i * 10] #Get 10 days later's answer
        #print(te_x[i*10][13])
        #print(te_x[i*10][16])
        if(pred == 1):
            if stock in port.keys():
                continue
            elif(low_val[i*10]>0):
                continue
            else:
                print(i)
                print(stock)
                s = Stock(stock, open_price[i], 'None')
                port[stock] = s
        if(pred == 0):
            if stock in port.keys():
                #print(sell)
                port[stock].sell_price = close_price[i]
                port[stock].act = 1 #Sell
            else:
                continue
    '''
        <建立以及改變port>
        for 個股 in 產業:
            獲得該個股在10天後的預測結果
            if Pred結果==1:
                Check是否在Portfolio裡
                if in portfolio:
                    續抱
                if not in portfolio:
                    增持
            else:
                if in portfolio:
                    賣出
                if not in portfolio:
                    pass
        
        <此動作結束後之損益計算>
        tot = 
        for 個股 in 投組:
            get = (df[sell_date] - df[open_date])/df[open_date]
            tot += get
        tot/len(投組)
        
        '''

