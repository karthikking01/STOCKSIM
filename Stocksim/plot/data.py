import pandas as pd
import yfinance as yf
# import pandas_datareader.data as pdr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
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


def chk_usr_pwd(usr,pwd):
    try:
        x = pd.read_csv("Stocksim/plot/data/userdata.csv", index_col=0)
        # print(x[x["usr"]==usr]["pwd"].values[0])
        print(x)
        if usr in x.index:
            if pd.Series(x.loc[usr]["pwd"]).iloc[-1] == pwd:
                return (200, pd.Series(x.loc[usr]["liq"]).iloc[-1])
            else:
                return (401,None)
        else:
            return (400,None)
    except:
        return(400,None)

def lff(name,sdate:datetime.date,dnrows, forward=True):
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
        if forward:
            nextday = sdate+datetime.timedelta(days=1)
            return lff(name,nextday,dnrows)
        else:
            prevday = sdate-datetime.timedelta(days=1)
            return lff(name,prevday,dnrows,forward=False)

def lfw(name):
    """Loads Ticker from Web"""
    tk = yf.Ticker(TRD[name]) # get ticker (YahooFinance module)
    x = pd.DataFrame(tk.history(period="max"))
    x.index = [d.strftime('%Y-%m-%d') for d in x.index.date]
    x = x.drop(columns=["Dividends","Stock Splits"]).loc["2000-01-03":]
    x.to_csv("Stocksim/plot/data/{}.csv".format(name),header=False)  
    del x
    
class tradable:
    data = None
    def __init__(self, name, sdate, dnrows, lastday = False, forward=True):
        self.name = name
        if name in TRDX:
            self.forward = forward
            self.ld = lastday
            self.dnrows = dnrows
            self.ticker = TRD[name]
            self.sdate = sdate
            self.data = None
        
            try:
                if self.ld == False:
                    self.data, self.sline = lff(name,sdate,dnrows, forward=self.forward)
                else:
                    self.data, self.sline = lff(name,sdate,dnrows, forward=self.forward)
                    self.data = self.data.tail(1)
            except FileNotFoundError or pd.errors.EmptyDataError:
                lfw(name)
                if self.ld == False:
                    self.data, self.sline = lff(name,sdate,dnrows, forward=self.forward)
                else:
                    self.data, self.sline = lff(name,sdate,dnrows, forward=self.forward)
                    self.data = self.data.tail(1)
            self.eline = self.sline+dnrows
        else:
            raise ValueError("Invalid Name: {} is not a valid Material REFER TO TRD".format(self.name))
    
class ledger():
    def __init__(self, file):
        self.file = file
        import pandas as pd
        self.data = pd.read_csv(file,header=None,names=["date","user","token","price","qty","amt"],dtype={"user":str,"token":str,"price":float,"qty":float,"amt":float},index_col=0)
        self.last_index = self.data.index.max()

    def txn(self, date:datetime.date ,user:str ,token:str ,price:float, qty:float):
        amt = price*qty
        txn = pd.DataFrame({"date":date,"user":user,"token":token,"price":price,"qty":qty,"amt":amt},index=[self.last_index+1])
        self.data = pd.concat([txn,self.data],axis=0)
        self.last_index+=1
        return amt
    
    def fetch_user_data(self,user:str):
        return self.data[self.data["user"]==user]

    def fetch_token_data(self,user:str, token:str):
        return self.data[(self.data["user"]==user) & (self.data["token"]==token)]

    def save_to_csv(self):
        self.data.to_csv(self.file,header=False)
    
if __name__ == "__main__":
    test=tradable("ASBL",datetime.date(2000,1,15), 21, False, False)
    x = test.data
    print(x)
    l = ledger(file="Stocksim/plot/data/ledger.csv")
    l.txn(datetime.date(2000,1,15),"user1","ASBL",100,1)
    l.txn(datetime.date(2000,1,15),"user1","ASBL",100,-1)
    token_data=l.fetch_token_data("user1","ASBL")
    print(token_data)