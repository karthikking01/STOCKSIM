import pandas as pd
import requests
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=IBM&apikey=4GWAYFQ65WWQM9IF'
pd.DataFrame(requests.get(url).json()["Time Series (Daily)"]).T.to_csv("Stocksim/plot/data/SHIF.csv",header=False)