import pandas as pd
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import time
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

TR = {
    "AAPL": "APPLE Inc.",
    "NVDA": "NVIDIA Corp.",
    "MSFT": "Microsoft Corp.",
    "AXP": "American Express Co.",
    "AMZN": "Amazon.com Inc.",
    "KO": "The Coca-Cola Co.",
    "LLY": "Eli Lilly and Co.",
    "INTC": "Intel Corp.",
    "WMT": "Walmart Inc.",
    "JPM": "JPMorgan Chase & Co.",
    "IBM": "IBM Corp.",
    "XOM": "Exxon Mobil Corp.",
    "UNH": "UnitedHealth Group Inc.",
    "ORCL": "Oracle Corp."
}

def lff(name,sdate:datetime.date,dnrows):
    """Loads Data from file ranging from sdate to sdate+dnrows"""
    with open("Stocksim/plot/data/{}.csv".format(name), "r") as f:
        for count, l in enumerate(f): #count number of iterations ie lines moved
            if str(l).startswith(str(sdate)): # if line starts with sdate
                df = pd.read_csv("Stocksim/plot/data/{}.csv".format(name),header=None,index_col=0,skiprows=count,nrows=dnrows) #skip number of lines equal to count and read dnrows lines
                df.index = pd.to_datetime(df.index, format='%Y-%m-%d') # convert index to datetime
                df.index.name=None # removing index name
                df.columns = ["Open","High","Low","Close","Volume"] # renaming index columns to simpler ones
                df["D"] = df["Close"]-df["Open"] # change
                df["D%"] = df["D"]/df["Open"]*100 # perc change
                df["height"] = df["High"]-df["Low"] # height
                break
    try:
        return df, count+1
    except UnboundLocalError:
        nextday = sdate+datetime.timedelta(days=1)
        return lff(name,nextday,dnrows)

def lfw(name):
    """Loads Ticker from Web"""
    tk = yf.Ticker[TR[name]] # get ticker (YahooFinance module)
    x = pd.DataFrame(tk.history(period="max"))
    x.index = [d.strftime('%Y-%m-%d') for d in x.index.date]
    x = x.drop(columns=["Dividends","Stock Splits"]).loc["2000-01-03":]
    x.to_csv("Stocksim/plot/data/{}.csv".format(name),header=False)  
    del x
    
class tradable:
    data = None
    def __init__(self, name, sdate, dnrows, lastday = False):
        self.name = name
        if name in TR:
            self.ld = lastday
            self.dnrows = dnrows
            self.ticker = TR[name]
            self.sdate = sdate
            self.data = None
            self.sline = None
        
            try:
                if self.ld == False:
                    self.data, self.sline = lff(name,sdate,dnrows)
                else:
                    self.data, self.sline = lff(name,sdate,dnrows)
                    self.data = self.data.tail(1)
            except FileNotFoundError or pd.errors.EmptyDataError:
                lfw(name)
                if self.ld == False:
                    self.data, self.sline = lff(name,sdate,dnrows)
                else:
                    self.data, self.sline = lff(name,sdate,dnrows)
                    self.data = self.data.tail(1)
            self.eline = self.sline+dnrows
        else:
            raise ValueError("Invalid Name: {} is not a valid Material REFER TO TRD".format(name))
    
    def movedays(self, ndays):
        dx = pd.read_csv("Stocksim/plot/data/{}.csv".format(self.name),header=None,index_col=0,skiprows=self.eline-1,nrows=ndays)
        dx.index=pd.to_datetime(dx.index, format='%Y-%m-%d')
        dx.index.name=None
        dx.columns = ["Open","High","Low","Close","Volume"]
        dx["D"] = dx["Close"]-dx["Open"]
        dx["D%"] = dx["D"]/dx["Open"]*100
        dx["height"] = dx["High"]-dx["Low"]
        self.data = pd.concat([self.data,dx],axis=0).iloc[ndays:]
        self.sline+=1
        self.eline+=1

    def nextday(self):
        self.movedays(1)
    
    
if __name__ == "__main__":
    test=tradable("AAPL",datetime.date(2000,1,15), 21)
    enddate = test.data.index
    print(enddate)