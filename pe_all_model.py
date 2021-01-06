import os
import sys
import xgboost as xgb
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report
#company = ['1301','1303','1304','1305','1307','1308','1309','1310','1312','1313','1314','1315','1321','1323','1324','1325','1326','1337','1340','1341','4306']
#stock_num = sys.argv[1]
company = [sys.argv[1]]
i = 0
for stock_num in company:
    if(i == 0):
        i = i+1
        te_x =np.load('./stock_data/tex/test_x_'+stock_num+'.npy')
        te_y =np.load('./stock_data/tey/test_y_'+stock_num+'.npy')
        tr_x =np.load('./stock_data/trx/train_x_'+stock_num+'.npy')
        tr_y =np.load('./stock_data/try/train_y_'+stock_num+'.npy')
        va_x =np.load('./stock_data/vax/val_x_'+stock_num+'.npy')
        va_y =np.load('./stock_data/vay/val_y_'+stock_num+'.npy')
    else:
        if not os.path.isfile('./stock_data/tex/test_x_'+stock_num+'.npy'):
            continue
        te_x = np.concatenate((te_x, np.load('./stock_data/tex/test_x_'+stock_num+'.npy')), axis=0)
        te_y = np.concatenate((te_y, np.load('./stock_data/tey/test_y_'+stock_num+'.npy')), axis=0)
        tr_x = np.concatenate((tr_x, np.load('./stock_data/trx/train_x_'+stock_num+'.npy')), axis=0)
        tr_y = np.concatenate((tr_y, np.load('./stock_data/try/train_y_'+stock_num+'.npy')), axis=0)
        va_x = np.concatenate((va_x, np.load('./stock_data/vax/val_x_'+stock_num+'.npy')), axis=0)
        va_y = np.concatenate((va_y, np.load('./stock_data/vay/val_y_'+stock_num+'.npy')), axis=0)
print(te_x.shape)

#pca = PCA(n_components = 10)
#pca.fit(tr_x)
#tr_x = pca.transform(tr_x)
print(tr_x)
#va_x = pca.transform(va_x)
#te_x = pca.transform(te_x)
model = xgb.XGBClassifier(
                    booster='gbtree',
                    max_depth = 3,
                    learning_rate=0.2,
                    n_estimators= 800,
                    subsample = 0.85,
                    objective='binary:logitraw',
                    )

eval_set = [(va_x, va_y)]

model.fit(tr_x, tr_y, eval_set = eval_set, verbose=True, eval_metric="error", early_stopping_rounds=30)

y_pred = model.predict(te_x)
print(y_pred[:100])
print(te_y[:100])
acc = accuracy_score(te_y, y_pred)
print(acc)
pca_report = classification_report(te_y, y_pred)
print(str(pca_report))
model.save_model('./xg_model/'+company[0]+'.model')
