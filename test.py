import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


def loser_gainer():
    final = {}
    indexs = ['losers', 'gainers']
    url = 'https://nepalstockinfo.com/'
    urls = [url + index for index in indexs]
    for i, url in enumerate(urls):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find('tbody').find_all('tr')[2:17]
        title = ['symbol', 'LTP', '% change', 'date', 'status']
        date = soup.find('td', colspan=3).text.strip()[5:]
        body = []
        for d in data:
            body.append(d.text.strip().split(' '))
        body = [b + [date]+[indexs[i]] for b in body]
        df = pd.DataFrame(data=body, columns=title, )
        mero = df.to_dict(orient='records')
        if i == 0:
            loser = mero
        else:
            gainer = mero
    final['losers'] = loser
    final['gainers'] = gainer


    return json.dumps(final)

print(loser_gainer())













