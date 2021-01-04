import requests as req
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'}
payload = {
    'submitTag': 1,
    'startDate': 20040101,
    'endDate': 20201201,
    'yy': 2004,
    'mm': 1,
    'dd': 1,
    'yy': 2020,
    'mm': 12,
    'dd': 1,
}
res = req.post('https://www.twse.com.tw/zh/statistics/statisticsList?type=04&subType=220', data = payload)
soup = BeautifulSoup(res.content, 'html.parser')
a = soup.find_all('a')
hr = []
for h in a:
    k = h.get('href')
    if k is not None:
        if('/statistics/count') in h.get('href'):
            hr.append(h.get('href'))