import pandas as pd
from datetime import *
from pandas.errors import EmptyDataError as EDE
import numpy as np
dataexists = False
try:
    stock = pd.read_csv('./Stocksim/plot/data.csv',sep=",")
    dataexists = True
except EDE:
    pass
dt = date.today() - timedelta(days=3650)
print(dt)

if not(dataexists):
    cols = []
    for i in range(7):
        cols.append(str(dt+timedelta(days=i)))
    stock = pd.DataFrame(columns=cols)
    print(stock)
    print(cols)