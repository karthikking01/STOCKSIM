import pandas as pd
import yfinance as yf
from plot.data import *

txr = yf.Ticker("AXISBANK.BO")
print(txr.info)