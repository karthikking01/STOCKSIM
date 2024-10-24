# import pandas as pd
# import requests
import os
# # # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

# tradables = {"ASBL":"AAPL", "COMO":"NVDA", "COSA":"MSFT", "ENEC":"AXP", "HITR":"AMZN", "HOME":"KO", "INPA":"LLY", "REMT":"INTC", "RITM":"WMT", "SHFA":"JPM", "SHIF":"IBM", "THRE":"XOM", "UNRE":"UNH", "UNPO":"ORCL"}
# for i in tradables:
#     url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol={}&apikey=A97HEVFBKYFWOQWM'.format(tradables[i])
#     pd.DataFrame(requests.get(url).json()["Time Series (Daily)"]).T.to_csv("Stocksim/plot/data/{}.csv".format(i),header=False)

for file in os.listdir("Stocksim/plot/data"):
    with open("Stocksim/plot/data/{}".format(file), "r") as f:
        print(f.readlines()[-1:])