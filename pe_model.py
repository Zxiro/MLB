import os
import sys
import xgboost as xgb
import numpy as np
from sklearn.metrics import accuracy_score


stock_num = sys.argv[1]

te_x =np.load('./stock_data/tex/test_x_'+stock_num+'.npy') 
te_y =np.load('./stock_data/tey/test_y_'+stock_num+'.npy') 
tr_x =np.load('./stock_data/trx/train_x_'+stock_num+'.npy') 
tr_y =np.load('./stock_data/try/train_y_'+stock_num+'.npy')
va_x =np.load('./stock_data/vax/val_x_'+stock_num+'.npy')
va_y =np.load('./stock_data/vay/val_y_'+stock_num+'.npy')

model = xgb.XGBClassifier(
                    booster='gbtree',
                    max_depth = 4,
                    learning_rate=0.01,
                    n_estimators= 1000,
                    subsample = 0.8,
                    objective='binary:logitraw',
                    )

eval_set = [(va_x, va_y)]

model.fit(tr_x, tr_y, eval_set = eval_set, verbose=True, eval_metric="error", early_stopping_rounds=800)

y_pred = model.predict(te_x)
print(y_pred)
print(te_y)
acc = accuracy_score(te_y, y_pred)
print(acc)
model.save_model('./xg_model/'+stock_num+'.model')