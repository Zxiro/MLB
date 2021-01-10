import os
import sys
import xgboost as xgb
import numpy as np
from sklearn.metrics import accuracy_score


#stock_num = sys.argv[1]
company = ['1301','1303','1304','1305','1307','1308','1309','1310','1312','1313','1314','1315','1321','1323','1324','1325','1326','1337','1340','1341','4306']
#stock_num = '1301'
#print(stock_num)
te_x =np.load('./stock_data/tex/test_x_'+stock_num+'.npy') 
te_y =np.load('./stock_data/tey/test_y_'+stock_num+'.npy') 
tr_x =np.load('./stock_data/trx/train_x_'+stock_num+'.npy') 
tr_y =np.load('./stock_data/try/train_y_'+stock_num+'.npy')
va_x =np.load('./stock_data/vax/val_x_'+stock_num+'.npy')
va_y =np.load('./stock_data/vay/val_y_'+stock_num+'.npy')
model = xgb.XGBClassifier(
                    booster='gbtree',
                    max_depth = 3,
                    learning_rate=0.05,
                    n_estimators= 5000,
                    subsample = 0.85,
                    objective='binary:logitraw',
                    )

eval_set = [(va_x, va_y)]

model.fit(tr_x, tr_y, eval_set = eval_set, verbose=True, eval_metric="error", early_stopping_rounds=100)

y_pred = model.predict(te_x)

print(y_pred)

print(te_y)

acc = accuracy_score(te_y, y_pred)

print(acc)

model.save_model('./xg_model/'+stock_num+'.model')