import pandas as pd
import requests
from datetime import datetime, timedelta
import yfinance as yf
import plotext
import time
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
def lff(name,sdate,dnrows):
    """Loads Data from file ranging from sdate to sdate+dnrows"""
    with open("Stocksim/plot/data/{}.csv".format(name), "r") as f:
        for count, l in enumerate(f): #count number of iterations ie lines moved
            if str(l).startswith(sdate): # if line starts with sdate
                df = pd.read_csv("Stocksim/plot/data/{}.csv".format(name),header=None,index_col=0,skiprows=count,nrows=dnrows) #skip number of lines equal to count and read dnrows lines
                df.index.name=None # removing index name
                df.columns = ["O","H","L","C","V"] # renaming index columns to simpler ones
                df["D"] = df["C"]-df["O"] # change
                df["D%"] = df["D"]/df["O"]*100 # perc change
                break
    return df, count+1
def lfw(name):
    """Loads Ticker from Web"""
    tk = yf.Ticker[TRD[name]] # get ticker (YahooFinance module)
    x = pd.DataFrame(tk.history(period="max"))
    x.index = [d.strftime('%Y-%m-%d') for d in x.index.date]
    x = x.drop(columns=["Dividends","Stock Splits"]).loc["2000-01-03":]
    x.to_csv("Stocksim/plot/data/{}.csv".format(name),header=False)  
    del x
        
TRD = {"ASBL":"AAPL", "COMO":"NVDA", "COSA":"MSFT", "ENEC":"AXP", "HITR":"AMZN", "HOME":"KO", "INPA":"LLY", "REMT":"INTC", "RITM":"WMT", "SHFA":"JPM", "SHIF":"IBM", "THRE":"XOM", "UNRE":"UNH", "UNPO":"ORCL"}
class tradable:
    data = None
    def __init__(self, name, sdate, dnrows ,line=False):
        self.name = name
        if name in TRD:
            self.dnrows = dnrows
            self.ticker = TRD[name]
            self.sdate = sdate
            self.data = None
            self.sline = None
    
            try:
                self.data, self.sline = lff(name,sdate,dnrows)
            except FileNotFoundError or pd.errors.EmptyDataError:
                lfw(name)
                self.data, self.sline = lff(name,sdate)
            self.eline = self.sline+dnrows
        else:
            raise ValueError("Invalid Name: {} is not a valid Material REFER TO TRD".format(self.name()))
    
    def movedays(self, ndays):
        dx = pd.read_csv("Stocksim/plot/data/{}.csv".format(self.name),header=None,index_col=0,skiprows=self.eline-1,nrows=ndays)
        dx.index.name=None
        dx.columns = ["O","H","L","C","V"]
        dx["D"] = dx["C"]-dx["O"]
        dx["D%"] = dx["D"]/dx["O"]*100
        self.data = pd.concat([self.data,dx],axis=0).iloc[ndays:]

    def nextday(self):
        self.movedays(1)
    
test=tradable("ASBL","2001-02-21", 100)
plotext.plot(range(100),test.data["C"])
plotext.show()