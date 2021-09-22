from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

####### Nepse Index Data Fetcher
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


###### Sensitive Index Data Fetcher
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


####### Nepse and Sensitive Data Fetcher
def fetch_index():
    url = requests.get('http://www.nepalstock.com/')
    soup = BeautifulSoup(url.text, 'lxml')
    market_status = soup.find('div',class_="container red-text market-status").text.strip()
    return sensitiveIndex(), nepseIndex()


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
    df = pd.DataFrame(data=body_list,columns=title)
    live_data = df.to_json(orient="records")
    return live_data


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



