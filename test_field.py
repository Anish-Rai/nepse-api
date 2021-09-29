import requests
from bs4 import BeautifulSoup
import pandas as pd



url = 'https://www.sharesansar.com/market'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
data = soup.find_all('table', class_='table table-bordered table-striped table-hover')
data1 =
data2 =
print(data)

