import requests
from twilio.rest import Client


account_sid = 'ID HERE'
auth_token = 'Token Here'

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_Endpoint = "https://www.alphavantage.co/query?"
api_key = "Your KEy"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "full",
    "apikey": api_key
}


response = requests.get(STOCK_Endpoint, params=params)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
day1 = float(data_list[0]['4. close'])
day2 = float(data_list[3]['4. close'])
difference = day1-day2

up_down = None

if difference > 0:
    up_down = "UP"
else:
    up_down = "DOWN"

percent = abs((difference / day1) * 100)
if abs(percent) >= 5:
    NEWS_Endpoint = "https://newsapi.org/v2/everything?"
    api_key_news = "95fcf5d4911440cfaa3f7b7f18c4d453"

    params_news = {
        "q": "tesla",
        "from": "2021-06-07",
        "sortBy": "publishedAt",
        "apikey": api_key_news
    }
    response = requests.get(NEWS_Endpoint, params=params_news)
    response.raise_for_status()
    article = response.json()["articles"]
    three_articles = article[:3]
    formatted_article = [f"{COMPANY_NAME}: {up_down} {abs(percent)}%\nHeadline:{article['title']}. \nBrief: " 
                         f"{article ['description']}"for article in three_articles]
    client = Client(account_sid, auth_token)
    for articles in formatted_article:
        message = client.messages.create(
         body=articles,
         from_='+14782421829',
         to='+2348107723143'
        )

        print(message.status)
