import requests as rq
from bs4 import BeautifulSoup
#import beautifulsoup4
import numpy as np

y=2020
m=12
d=25
link="https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=html&date="+str(y)+str(m)+str(d)+"&selectType=ALL"
r = rq.get(link)
soup = BeautifulSoup(r.text, "lxml")
a_tags = soup.find('tbody')
a_tags = a_tags.find_all('tr')
i=2
#print(a_tags)
lis=[]
tmp = 0
pe = {}
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
print(pe)
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
