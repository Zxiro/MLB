import os
import json
import pandas as pd
from build_config import index_dic
dirPath = r"./pe_data"
indust = index_dic['indust']

def data_read(dirPath):
    result = [f for f in sorted(os.listdir(dirPath)) if os.path.isfile(os.path.join(dirPath, f))]
    return result

dict_ = {}
t = data_read(dirPath)
for ind in indust:
    print(ind)
    for name in t:
        exc = pd.read_excel('./pe_data/'+ name)
        index = exc.index[exc['P/E RATIO AND YIELD OF LISTED STOCKS']==ind]
        if(len(exc.iloc[index]['Unnamed: 9'].values)==0):
            strr  = ind.replace(" ", "")
            index = exc.index[exc['P/E RATIO AND YIELD OF LISTED STOCKS']==strr]
            if(len(exc.iloc[index]['Unnamed: 9'].values != 0)):
                dict_[name[2:8]] = exc.iloc[index]['Unnamed: 9'].values[0]
            continue
        dict_[name[2:8]] = exc.iloc[index]['Unnamed: 9'].values[0]
    print(dict_)
    with open("./indust_pe/"+ind+".json", "w") as outfile:  
        json.dump(dict_, outfile) 
    dict_ = {}
        
