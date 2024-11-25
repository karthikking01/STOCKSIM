import pandas as pd
from datetime import *
from plot.data import *

TRDX = get_tickers("admin")

for i in TRDX.index:
    x = tradable(i,date(2000,1,3),25)
    print(x)