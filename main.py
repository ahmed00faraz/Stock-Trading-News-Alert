import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

TWILIO_SID = 'ACb3a9ec9cc87ef804e8185d2c041556f4'
TWILIO_AUTH_TOKEN = '6516eb1268eccd1731426662bc7ca5db'

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "TZN0S2013QS4WDNH"
NEWS_API_KEY = "99e30874204447aabfc7ec321399b887"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}


def get_news():
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
    }
    resp = requests.get(NEWS_ENDPOINT, params=news_params)
    first_3_articles = resp.json()['articles'][:3]
    return first_3_articles


# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]

# Get the yesterday's closing price
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data['4. close'])

# Get the day before yesterday's closing price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data['4. close'])

# Find the positive difference between 1 and 2
difference = (yesterday_closing_price - day_before_yesterday_closing_price)
diff_perc = round(100 * difference / yesterday_closing_price)
up_down = "🔽"
if diff_perc > 0:
    up_down = "🔼"
if abs(diff_perc) > 1:
    three_articles = get_news()

    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_perc}%\nHeadline : {article['title']}. \nBrief: {article['description']}" for
        article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+18159823100',
            to='+917976524328',
        )
