import pandas as pd
import requests
from pandas.errors import EmptyDataError as EDE
"""
Astral Blip         (ASBL)
Confiscated Motive  (COMO)
Corrupted Sample    (COSA)
Entropic Echo       (ENEC)
Hidden Trend        (HITR)
House Memory        (HOME)
Intrusive Pattern   (INPA)
Remote Thought      (REMT)
Ritual Impulse      (RITM)
Shaded Facet        (SHFA)
Shifting Fragment   (SHIF)
Threshold Remnant   (THRE)
Undefined Reading   (UNRE)
Untapped Potential  (UNPO)
"""
def fetch(sym):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol={}&apikey=A97HEVFBKYFWOQWM'.format(sym)
    pd.DataFrame(requests.get(url).json()["Time Series (Daily)"]).T.to_csv("Stocksim/plot/data/{}.csv".format(sym),header=False)
    
    
tradables = {"ASBL":"AAPL", "COMO":"NVDA", "COSA":"MSFT", "ENEC":"AXP", "HITR":"AMZN", "HOME":"KO", "INPA":"LLY", "REMT":"INTC", "RITM":"WMT", "SHFA":"JPM", "SHIF":"IBM", "THRE":"XOM", "UNRE":"UNH", "UNPO":"ORCL"}