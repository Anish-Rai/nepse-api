from bs4 import BeautifulSoup
import requests
import json
import pandas as pd



####### Nepse and Sensitive Data Fetcher
def indices():
    title = ['index','close','point change','% change']
    url = requests.get('https://www.sharesansar.com/market')
    soup = BeautifulSoup(url.text, 'lxml')
    table = soup.find('table', class_="table table-bordered table-striped table-hover")
    title = ['index','close','point change','% change']
    body = []
    for tr in table.find_all('tr')[1:]:
        n_tr = tr.text.strip().replace(',','').replace('\n',',').split(',')
        body.append(n_tr)

    df = pd.DataFrame(data=body, columns=title)
    return df.to_json(orient='records')

####### Live Updated Data
def live_data():
    url = "https://merolagani.com/LatestMarket.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find('table', class_="table table-hover live-trading sortable")
    title = []
    body = []
    for span in data.find_all('span'):
        title.append(span.text)

    for tr in data.find_all('tr'):
        for td in tr.find_all('td'):
            body.append(td.text)
    body = list(filter(None, body))

    body_list = [body[x:x+7] for x in range(0,len(body),7)]

    for b in body_list:
        status=float(b[2].replace(',',''))
        if status <0:
           value = "negative"
        elif status == 0:
            value = "neutral"
        else:
            value = "positive"
        b.append(value)

    title = title+['Status']
    df = pd.DataFrame(data=body_list, columns=title)
    live_datas = df.to_json(orient="records")
    return live_datas


#individual company detail
def get_company_detail(name):
    url = ("https://merolagani.com/CompanyDetail.aspx?symbol=")+ name
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find('table', class_='table table-striped table-hover table-zeromargin')
    title = []
    detail = []
    name = ['Company name']
    company_name = [soup.find('span',id='ctl00_ContentPlaceHolder1_CompanyDetail1_companyName').text]
    for d in data.find_all('tr'):
        if d.th is not None:
            title.append(d.th.text.strip())
    title = [i for i in title if  (i != '#') and (i != '% Dividend') and (i != '% Bonus')and (i != 'Right Share')]
    final_title = name+title[0:13]

    for d in data.find_all('tr'):
        if d.td is not None:
            detail.append(d.td.text.strip())
    new_list = [d.replace(' ', '').replace('\r', '').replace('\n', '') for d in detail]
    new_list = [n for n in new_list if n != '']
    final_detail = company_name+new_list[0:13]

    company_detail = dict(zip(final_title,final_detail))
    return (json.dumps(company_detail))



######## Closing Prices Of Nepse Listed Companies
def today_price():
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
    return df.to_json(orient='records')


#Top Gainer and Loser
def loser_gainer():
    final = {}
    indexs = ['losers', 'gainers']
    url = 'https://nepalstockinfo.com/'
    urls = [url + index for index in indexs]
    for i, url in enumerate(urls):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find('tbody').find_all('tr')[2:17]
        title = ['symbol', 'LTP', '% change']
        date = soup.find('td', colspan=3).text.strip()[5:]
        body = []
        for d in data:
            body.append(d.text.strip().split(' '))
        body = [b  for b in body]
        df = pd.DataFrame(data=body, columns=title, )
        json_data = df.to_dict(orient='records')
        if i == 0:
            loser = json_data
        else:
            gainer = json_data
    final['date'] = date
    final['losers'] = loser
    final['gainers'] = gainer

    return json.dumps(final)

'''def closing_price():
    head = ['Company Name','No. Of Transaction', 'Max Price', 'Min Price', 'Closing Price', 'Traded Shares','Amount','Previous Closing', 'Difference Rs.']
    body = []
    base_url = 'http://www.nepalstock.com/main/todays_price/index/'
    urls  = [base_url+str(i) for i in range(1,13)]
    td_list =[]
    for url in urls:
        link = requests.get(url)
        soup = BeautifulSoup(link.text, 'lxml')
        rows = soup.find('table', class_='table table-condensed table-hover').find_all('tr')
        for row in rows[2:-4]:
            for td in row.find_all('td')[1:]:
                data = td.text.strip()
                td_list.append(data)
    body = [td_list[x:x+9] for x in range(0,len(td_list),9)]
    df = pd.DataFrame(data=body, columns=head)
    closing_prices = df.to_json(orient="records")
    return closing_prices'''


####### Nepse Index Data Fetcher
'''
def nepseIndex():
    nepseurl = requests.get('http://www.nepalstock.com/')
    soup = BeautifulSoup(nepseurl.text, 'lxml')
    title = soup.find_all('div', class_="title")[0].text.strip()
    current_index = soup.find_all('div', class_="current-index")[0].text.strip()
    point_change = soup.find_all('div', class_="point-change")[0].text.strip()
    percent_change = soup.find_all('div', class_="percent-change")[0].text.strip()
    dict = {'title': title, 'current_index': current_index, 'point_change': point_change, 'percent_change': percent_change}
    nepseinfo = json.loads(json.dumps(dict, sort_keys=False))
    return nepseinfo
'''

###### Sensitive Index Data Fetcher
'''
def sensitiveIndex():
    nepseurl = requests.get('http://www.nepalstock.com/')
    soup = BeautifulSoup(nepseurl.text, 'lxml')
    title = soup.find_all('div', class_="title")[1].text.strip().upper()
    current_index = soup.find_all('div', class_="current-index")[1].text.strip()
    point_change = soup.find_all('div', class_="point-change")[1].text.strip()
    percent_change = soup.find_all('div', class_="percent-change")[1].text.strip()
    dict = {'title':title, 'current_index': current_index, 'point_change': point_change, 'percentage_change': percent_change}
    sensitiveinfo = json.loads(json.dumps(dict, sort_keys=False))
    return sensitiveinfo
'''

'''
def fetch_index():
    url = requests.get('http://www.nepalstock.com/')
    soup = BeautifulSoup(url.text, 'lxml')
    market_status = soup.find('div',class_="container red-text market-status").text.strip()
    return sensitiveIndex(), nepseIndex()
'''
