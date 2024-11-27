import yfinance as yf
import time
import pandas as pd
import datetime
# import requests
# import pandas as pd
#     url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol={}&apikey=A97HEVFBKYFWOQWM'.format(tradables[i])
#     pd.DataFrame(requests.get(url).json()["Time Series (Daily)"]).T.to_csv("Stocksim/plot/data/{}.csv".format(i),header=False)
# date = "2000-01-08"

tk = yf.Ticker("SBIN.NS")
x = pd.DataFrame(tk.history(period="max"))
x.index = [d.strftime('%Y-%m-%d') for d in x.index.date]
x = x.drop(columns=["Dividends","Stock Splits"]).loc["2010-01-01":]
x = x.index.to_series()
x.to_csv("bin/plot/data/datelist.csv", index=False, header=None)