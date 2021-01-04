import csv
import datetime
import os
import time
import json
import requests as rq
import numpy as np
from bs4 import BeautifulSoup

def crawl_pe(date):
    datetime = str(date).split(' ')[0].replace('-','')
    link="https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=html&date="+datetime +"&selectType=ALL"
    r = rq.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    a = soup.find('tr').find_next_siblings()
    t = a[0].find_all('td')
    pe_pos = 0
    for i in t:
        if(i.text == '本益比'):
            break
        pe_pos+=1
    a_tags = soup.find('tbody')

    if(a_tags == None):
        return a_tags 

    a_tags = a_tags.find_all('tr')
    pe = {}
    for at in a_tags:
        t = at.find_all('td')# list of tr eles
        print(t)
        pe[t[0].text] = t[pe_pos].text
    print(pe)
    exit()

    if not os.path.exists('./pe_data/'):
        print("x")
        os.makedirs('./pe_data/')
    #json.dump(pe, open(f'./pe_data/{datetime}.json', 'w'), indent=4)


y=2020
m=12
d=25
n_days = 3000
date = datetime.datetime.now()
date = datetime.date(2014, 7, 17)
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
