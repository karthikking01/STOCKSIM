import pandas as pd
from datetime import *
from plot.data import *

trx = yf.Ticker("AAPL")
print(trx.info)