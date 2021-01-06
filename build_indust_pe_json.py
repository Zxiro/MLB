import os
import json
import pandas as pd
import sys
from build_config import index_dic
dirPath = r"./pe_data"
indust = index_dic['indust']
choose = sys.argv[1]
if(choose == 'pe'):
    location = 'Unnamed: 5'
elif(choose == 'yield'):
    location = 'Unnamed: 7'
elif(choose == 'pbr'):
    location = 'Unnamed: 9'
def data_read(dirPath):
    result = [f for f in sorted(os.listdir(dirPath)) if os.path.isfile(os.path.join(dirPath, f))]
    return result

dict_ = {}
t = data_read(dirPath)
for ind in indust:
    print(ind)
    for name in t:
        if 'json' in name:
            continue
        #print(name)
        exc = pd.read_excel('./pe_data/'+ name)
        index = exc.index[exc['P/E RATIO AND YIELD OF LISTED STOCKS']==ind]
        #print(index)
        #exit()
        if(len(exc.iloc[index][location].values)==0):
            strr  = ind.replace(" ", "")
            index = exc.index[exc['P/E RATIO AND YIELD OF LISTED STOCKS']==strr]
            if(len(exc.iloc[index][location].values != 0)):
                dict_[name[2:8]] = exc.iloc[index][location].values[0]
                #print(exc.iloc[index])
                #exit()
            continue
        #for i in exc.iloc[index].keys():
        #    print(exc.iloc[index][i])
        dict_[name[2:8]] = exc.iloc[index][location].values[0]
        #print(dict_)
        #exit()
    print(dict_)
    with open("./indust_pe/"+ind+choose+".json", "w") as outfile:
        json.dump(dict_, outfile)
    dict_ = {}
