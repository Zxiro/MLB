import requests as rq
from bs4 import BeautifulSoup
#import beautifulsoup4
import numpy as np
import csv
import datetime
import os
import time
import json

def crawl_pe(date):
    datetime = str(date).split(' ')[0].replace('-','')
    link="https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=html&date="+datetime +"&selectType=ALL"
    print(link)
    r = rq.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    a_tags = soup.find('tbody')
    print(a_tags)
    if(a_tags == None):
        return a_tags
    a_tags = a_tags.find_all('tr')
    i=2
    #print(a_tags)
    lis=[]
    tmp = 0
    pe = {}
    stock_num = 0
    stock_pe = 0
    for tag in a_tags:
        for x in tag:
            if(tmp == 1):
                print(x.string)
                stock_num = x.string
            if(tmp == 11):
                #print(x)
                print(x.string)
                stock_pe = x.string
            tmp = tmp + 1
        #exit()
        pe[stock_num] = stock_pe
        tmp = 0
        #print(tag)
    #print(pe)
    #with open('test.csv', 'w') as f:
    #    for key in pe.keys():
    #            f.write("%s,%s\n"%(key,pe[key]))
    #
    if not os.path.exists('../pe_data/'):
        print("x")
        os.makedirs('./pe_data/')
    json.dump(pe, open(f'./pe_data/{datetime}.json', 'w'), indent=4)


y=2020
m=12
d=25
n_days = 3000
date = datetime.datetime.now()
date = datetime.date(2017, 4, 13)
fail_count = 0
allow_continuous_fail_count = 5
data = {}
i = 0
while i < n_days:
    crawl_pe(date)
    date -= datetime.timedelta(days=1)
    i = i+1
    time.sleep(5)


'''
#print(a_tags)
for tag in a_tags:
    #print(tag)
    tmp = 0
    for x in tag:
        for tag_data in x:
            print(tag_data)
            #if(tmp==0):
            #    print(tag_data)
            #tmp=tmp+1
        #tmp=0
        #print(x[0])
    #print("")
    #exit()
    #i=i+1
    #if i%7==0:
    #    if i!=7 :
    #        lis.append(tag.string)
#print(lis)
'''
