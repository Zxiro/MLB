import os
import sys

company = [2302,2303,2329,2330,2337,2338,2342,2344,2351,2363,2369,2379,2388,2401,2408,2436,2441,2449,2451,2454,2458,2481,3006,3014,3016,3034,3035,3041,3054,3094,3189,3257,3413,3443,3530,3532,3545,3583,3588,3661,3711,4919,4952,4961,4967,4968,5269,5285,5305,5471,6202,6239,6243,6257,6271,6415,6451,6525,6531,6533,6552,6573,8016,8028,8081,8110,8131,8150,8261,8271]

#company = ['1301','1303','1304','1305','1307','1308','1309','1310','1312','1313','1314','1315','1321','1323','1324','1325','1326','1337','1340','1341','4306']


for stock_num in company:
    os.system("python3 build_train_data.py "+str(stock_num))

#for stock_num in company:
#    os.system("python3 pe_all_model.py "+str(stock_num))

exit()



