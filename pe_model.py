import xgboost as xgb
import numpy as np
from sklearn.metrics import accuracy_score

te_x =np.load('./stock_data/tex/test_x_2330.npy') 
te_y =np.load('./stock_data/tey/test_y_2330.npy') 
tr_x =np.load('./stock_data/trx/train_x_2330.npy') 
tr_y =np.load('./stock_data/try/train_y_2330.npy') 

model = xgb.XGBClassifier(
                    max_depth = 4,
                    learning_rate=0.01,
                    n_estimators= 1400,
                    objective='binary:logitraw',
                    early_stopping_rounds=50
                    )
eval_set = [(te_x, te_y)]
model.fit(tr_x, tr_y, eval_set=eval_set, verbose=True, eval_metric="logloss")

y_pred = model.predict(te_x)
print(y_pred)
print(te_y)
acc = accuracy_score(te_y, y_pred)
print(acc)