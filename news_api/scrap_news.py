


import json
# from newsapi import NewsApiClient
import requests
from datetime import datetime
from pandas.tseries.offsets import BDay

# Init
# newsapi = NewsApiClient(api_key='59e5e29b4480414d9ea273f301a48ecf')

# /v2/sources
# sources = newsapi.get_sources()
my_date = datetime.today() - BDay(5)
url = 'https://newsapi.org/v2/everything?q=kickback&from={}&apiKey=59e5e29b4480414d9ea273f301a48ecf'.format(my_date.strftime(format="%Y-%m-%d"))

response = requests.get(url)

# save json file
with open(f'C:/Users/Administrator/PycharmProjects/myscrapper/news_api/kickback_news_{datetime.today():%Y-%m-%d}.json', 'w') as json_file:
    json.dump(response.json(), json_file)

print("done")