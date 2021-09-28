import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def market_status():
    response = requests.get('https://www.nepalipaisa.com/')
    soup = BeautifulSoup(response.text, 'lxml')
    status = soup.find('div', id='marketStatus').text
    return status














