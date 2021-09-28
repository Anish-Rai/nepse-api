import requests
from bs4 import BeautifulSoup
import pandas as pd

url = requests.get('https://www.sharesansar.com/today-share-price')
soup = BeautifulSoup(url.text, 'lxml')
date = soup.find('input', id='fromdate').attrs['value']
data = soup.find('tbody')
titles = ['name', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'previous close', '% difference']
body = []
data_list = []
cname = []
for tdata in data.find_all('td'):
    td = tdata.text.strip().replace('\n', ',')
    body.append(td)
for name in data.find_all('a'):
    cname.append(name.attrs['title'])

body_lists = [body[x:x + 14] for x in range(1, len(body), 21)]
for blist in body_lists:
    for n, i in enumerate(blist):
        if n in [0, 2, 3, 4, 5, 7, 8, 13]:
            data_list.append(i)
data = [data_list[x:x + 8] for x in range(0, len(data_list), 8)]
for i, d in enumerate(data):
    d.insert(0, cname[i])
df = pd.DataFrame(data=data, columns=titles)