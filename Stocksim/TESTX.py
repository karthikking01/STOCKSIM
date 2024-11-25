import pandas as pd
import yfinance as yf
from plot.data import *

# t = ("BEL","ONGC","BPCL","SHRIRAMFIN","LT")


# for i in t:
#     with open("Stocksim/plot/data/tickers.csv","a") as f:
#         tick = yf.Ticker("{}.NS".format(i))
#         curr = tick.info["financialCurrency"]
#         sym = tick.info["symbol"]
#         name = str(tick.info["longName"]).replace("Limited","Ltd.")
#         f.write("{},{},admin \n".format(sym,name))

bse = yf.Ticker("^BSESN")
x = pd.DataFrame(bse.history(period="max"))
x.index = [d.strftime('%Y-%m-%d') for d in x.index.date]
x = x.loc["2000-01-03":]
x = pd.DataFrame(x.index)
x.to_csv("Stocksim/plot/data/datelist.csv", index=False)
# x.to_csv("Stocksim/plot/data/datelist.csv")