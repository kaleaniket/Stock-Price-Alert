import requests
from twilio.rest import Client

STOCK = "STOCK NAME" #Ex. if company is Tesla then TSLA
COMPANY_NAME = "COMPANY NAME" #Ex. if company is Tesla then Tesla Inc

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_KEY = "YOUR STOCK API KEY"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_KEY = "YOUR NEWS API KEY"

account_sid = "ACCOUNT id" #YOU HAVE TO SIGN IN TO THE twilio.com FOR ID AND TOKEN
auth_token = "TOKEN"


stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCK_KEY
}


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stock = response.json()["Time Series (Daily)"]

# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.

stock_list = [value for (key, value) in stock.items()]
yesterdays_data = float(stock_list[0]["4. close"])
print(yesterdays_data)
day_before_yesterdays_data = float(stock_list[1]["4. close"])
print(day_before_yesterdays_data)
diff = round(yesterdays_data - day_before_yesterdays_data, 4)
print(diff)

#Work out the value of 5% of yerstday's closing stock price.

percentage = round(abs(diff / yesterdays_data * 100), 2)
print(percentage)
up_down = None
if percentage > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


if percentage > 0:
    news_parameters = {
        "apiKey": NEWS_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    # news_response.raise_for_status()
    news = news_response.json()["articles"]
    three_articles = news[:3]
    print(three_articles)


# Send a separate message with each article's title and description to your phone number.
#Considered using a List Comprehension.

    formatted_articles = [f"{STOCK}{up_down}{percentage}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="NUMBER WHICH YOU GET FROM TWILIO",
            to="YOUR TWILIO REGISTERED MOBILE NUMBER" #YOU WILL RECIEVE MESSAGE NOTIFICATION ON THIS NUMBER AS SOON AS THE STOCK GOES HIGH OR LOW
        )
        print(message.status)

