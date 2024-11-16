from datetime import date
from plot.data import *
import mplfinance as mpf
trd = tradable("COMO", date(2000,1,3), 730)
mpf.plot(data=trd,type="line",style=binance_dark, volume=True, title="COMO")
print('END')