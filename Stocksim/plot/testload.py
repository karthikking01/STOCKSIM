import yfinance as yf
import time
import pandas as pd
import datetime
# import requests
# import pandas as pd
tradables = {"ASBL":"AAPL", "COMO":"NVDA", "COSA":"MSFT", "ENEC":"AXP", "HITR":"AMZN", "HOME":"KO", "INPA":"LLY", "REMT":"INTC", "RITM":"WMT", "SHFA":"JPM", "SHIF":"IBM", "THRE":"XOM", "UNRE":"UNH", "UNPO":"ORCL"}
# for i in tradables:
#     url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol={}&apikey=A97HEVFBKYFWOQWM'.format(tradables[i])
#     pd.DataFrame(requests.get(url).json()["Time Series (Daily)"]).T.to_csv("Stocksim/plot/data/{}.csv".format(i),header=False)
# date = "2000-01-08"

for i in tradables:
    tk = yf.Ticker(tradables[i])
    x = pd.DataFrame(tk.history(period="max"))
    x.index = [d.strftime('%Y-%m-%d') for d in x.index.date]
    x = x.drop(columns=["Dividends","Stock Splits"]).loc["2000-01-03":]
    x.to_csv("Stocksim/plot/data/{}.csv".format(i),header=False)
print(x)