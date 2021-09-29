import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def gainer_loser():
    url = 'https://www.sharesansar.com/market'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find_all('table', class_='table table-bordered table-striped table-hover')
    data1 = data[6:7]
    data2 = data [ 8:9]
    data = data1 + data2
    tr_list = []
    header = ['Symbol', 'LTP', 'Point Change', '% Change','status']
    for d in data:
        for tr in d.find_all('tr'):
            for td in tr.find_all('td'):
                i_td = td.text.strip()
                tr_list.append(i_td)
    tr_list = [tr_list[x:x+4] for x in range(0,len(tr_list),4)]
    for i,r in enumerate(tr_list):
        if i<5:
            r.append('Gainer')
        else:
            r.append('losers')
    df = pd.DataFrame(data=tr_list, columns=header)
    return df.to_json(orient='records')
















