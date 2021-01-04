import json

stock_dic = {
    'stock_num':'0050',
    'date':'2004-02-11', #永豐給lab最早的資料時間
    'end_date':'2020-12-31',
    #'features' :  ['date', 'close', 'open', 'high', 'low', 'volume', 'k','d','rsv','MA5','MA30','MA60', 'MACD', 'MACDsignal', 'MACDhist'],
    'features' :  ['date', 'close', 'open', 'high', 'low', 'volume', 'k','d','rsv', 'MA5','MA30','MA60'],
    'span': 1,
    'close_type' :'close', #['close','adj_close']
}

index_dic = {
    'stock_group':['2330', '2303', '2454', '3034', '2344', '2337', '2342', '2379'],
    'indust':['半導體類', '電子零組件類', '電子工業類']
}
