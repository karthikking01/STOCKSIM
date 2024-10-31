import pandas as pd
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
"""
1.Astral Blip         (ASBL)
2.Confiscated Motive  (COMO)
3.Corrupted Sample    (COSA)
4.Entropic Echo       (ENEC)
5.Hidden Trend        (HITR)
6.House Memory        (HOME)
7.Intrusive Pattern   (INPA)
8.Remote Thought      (REMT)
9.Ritual Impulse      (RITM)
10.Shaded Facet        (SHFA)
11.Shifting Fragment   (SHIF)
12.Threshold Remnant   (THRE)
13.Undefined Reading   (UNRE)
14.Untapped Potential  (UNPO)
"""
TRDX = {
    "ASBL": "Astral Blip",
    "COMO": "Confiscated Motive",
    "COSA": "Corrupted Sample",
    "ENEC": "Entropic Echo",
    "HITR": "Hidden Trend",
    "HOME": "House Memory",
    "INPA": "Intrusive Pattern",
    "REMT": "Remote Thought",
    "RITM": "Ritual Impulse",
    "SHFA": "Shaded Facet",
    "SHIF": "Shifting Fragment",
    "THRE": "Threshold Remnant",
    "UNRE": "Undefined Reading",
    "UNPO": "Untapped Potential"
}

TRD = {
    "ASBL": "AAPL",
    "COMO": "NVDA",
    "COSA": "MSFT",
    "ENEC": "AXP",
    "HITR": "AMZN",
    "HOME": "KO",
    "INPA": "LLY",
    "REMT": "INTC",
    "RITM": "WMT",
    "SHFA": "JPM",
    "SHIF": "IBM",
    "THRE": "XOM",
    "UNRE": "UNH",
    "UNPO": "ORCL"
}
def lff(name,sdate,dnrows):
    """Loads Data from file ranging from sdate to sdate+dnrows"""
    with open("Stocksim/plot/data/{}.csv".format(name), "r") as f:
        for count, l in enumerate(f): #count number of iterations ie lines moved
            if str(l).startswith(sdate): # if line starts with sdate
                df = pd.read_csv("Stocksim/plot/data/{}.csv".format(name),header=None,index_col=0,skiprows=count,nrows=dnrows) #skip number of lines equal to count and read dnrows lines
                df.index = pd.to_datetime(df.index, format='%Y-%m-%d') # convert index to datetime
                df.index.name=None # removing index name
                df.columns = ["Open","High","Low","Close","Volume"] # renaming index columns to simpler ones
                df["D"] = df["Close"]-df["Open"] # change
                df["D%"] = df["D"]/df["Open"]*100 # perc change
                df["height"] = df["High"]-df["Low"] # height
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
    
class tradable:
    data = None
    def __init__(self, name, sdate, dnrows):
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
    
    # def movedays(self, ndays):
    #     dx = pd.read_csv("Stocksim/plot/data/{}.csv".format(self.name),header=None,index_col=0,skiprows=self.eline-1,nrows=ndays)
    #     dx.index=pd.to_datetime(dx.index, format='%Y-%m-%d')
    #     dx.index.name=None
    #     dx.columns = ["Open","High","Low","Close","Volume"]
    #     dx["D"] = dx["Close"]-dx["Open"]
    #     dx["D%"] = dx["D"]/dx["Open"]*100
    #     dx["height"] = dx["High"]-dx["Low"]
    #     self.data = pd.concat([self.data,dx],axis=0).iloc[ndays:]
    #     self.sline+=1
    #     self.eline+=1

    # def nextday(self):
    #     self.movedays(1)
    
if __name__ == "__main__":
    test=tradable("ASBL","2023-08-01", 100)
    for i in range(1000):
        print(test.data)
        time.sleep(1)