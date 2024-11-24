import pandas as pd
import yfinance as yf
# import pandas_datareader.data as pdr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import *
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

binance_dark = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "#3dc985", "down": "#ef4f60"},  
        "edge": {"up": "#3dc985", "down": "#ef4f60"},  
        "wick": {"up": "#3dc985", "down": "#ef4f60"},  
        "ohlc": {"up": "green", "down": "red"},
        "volume": {"up": "#247252", "down": "#82333f"},  
        "vcedge": {"up": "green", "down": "red"},  
        "vcdopcod": False,
        "alpha": 1
    },
    "mavcolors": ("#ad7739", "#a63ab2", "#62b8ba"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": False,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "binance-dark",
}
    

def get_config(usr,pwd):
    x = pd.read_csv("Stocksim/plot/data/userdata.csv", names=["pwd","sdate","edate","ndays","itertime","liq"], index_col=0)
    x["sdate"] = pd.to_datetime(x["sdate"], format='%Y-%m-%d')
    x["edate"] = pd.to_datetime(x["edate"], format='%Y-%m-%d')
    # print(x[x["usr"]==usr]["pwd"].values[0])
    print(x)
    if usr in x.index:
        if pd.Series(x.loc[usr]["pwd"]).iloc[-1] == pwd:
            return (200, pd.Series(x.loc[usr]["sdate"]).iloc[-1],pd.Series(x.loc[usr]["edate"]).iloc[-1], pd.Series(x.loc[usr]["ndays"]).iloc[-1],pd.Series(x.loc[usr]["itertime"]).iloc[-1],pd.Series(x.loc[usr]["liq"]).iloc[-1])
        else:
            return (401,None,None)
    else:
        return (400,None,None)


def lff(name,sdate:datetime.date,dnrows):
    """Loads Data from file ranging from sdate to sdate+dnrows"""
    with open("Stocksim/plot/data/{}.csv".format(name), "r") as f:
    #read first line as tuple
        fdate = f.readline().split(",")[0]
        fdate = datetime.strptime(fdate, "%Y-%m-%d").date()
        if (fdate-sdate) > timedelta(days=10):
            return pd.DataFrame([[0,0,0,0,0,0,0]]*dnrows, columns=["Open","High","Low","Close","Volume","D","D%"])
        for count, l in enumerate(f): #count number of iterations ie lines moved
            if str(l).startswith(str(sdate)): # if line starts with sdate
                df = pd.read_csv("Stocksim/plot/data/{}.csv".format(name),header=None,index_col=0,skiprows=count,nrows=dnrows) #skip number of lines equal to count and read dnrows lines
                df.index = pd.to_datetime(df.index, format='%Y-%m-%d') # convert index to datetime
                df.index.name=None # removing index name
                df.columns = ["Open","High","Low","Close","Volume"] # renaming index columns to simpler ones
                df["D"] = df["Close"]-df["Open"] # change
                df["D%"] = df["D"]/df["Open"]*100 # perc change
                # df["height"] = df["High"]-df["Low"] # height
                break
    try:
        return df
        print(df)
    except UnboundLocalError:
        nextday = sdate+datetime.timedelta(days=1)
        return lff(name,nextday,dnrows)

def loadhistory(name, edate):
    with open("Stocksim/plot/data/{}.csv".format(name), "r") as f:
        for count, l in enumerate(f): #count number of iterations ie lines moved
            if str(l).startswith(str(edate)): # if line starts with sdate
                df = pd.read_csv("Stocksim/plot/data/{}.csv".format(name),header=None,index_col=0,nrows=count+1) #read number of lines equal to count and read dnrows lines
                df.index = pd.to_datetime(df.index, format='%Y-%m-%d') # convert index to datetime
                df.index.name=None # removing index name
                df.columns = ["Open","High","Low","Close","Volume"] # renaming index columns to simpler ones
                
                return df

def lfw(name):
    try:
        """Loads Ticker from Web"""
        tk = yf.Ticker(name) # get ticker (YahooFinance module)
        x = pd.DataFrame(tk.history(period="max"))
        x.index = [d.strftime('%Y-%m-%d') for d in x.index.date]
        x = x.drop(columns=["Dividends","Stock Splits"]).loc["2000-01-03":]
        x.to_csv("Stocksim/plot/data/{}.csv".format(name),header=False)  
        del x
    except:
        pass
    

def tradable(name,sdate,dnrows,lastday = False):
    try:
        if lastday == False:
            return lff(name,sdate,dnrows)
        else:
            return lff(name,sdate,dnrows).tail(1)
    except FileNotFoundError or pd.errors.EmptyDataError:
        lfw(name)
        if lastday == False:
            return lff(name,sdate,dnrows)
        else:
            return lff(name,sdate,dnrows).tail(1)
    
class ledger():
    def __init__(self, file):
        self.file = file
        import pandas as pd
        self.data = pd.read_csv(file,header=None,names=["date","user","token","price","qty","amt"],dtype={"user":str,"token":str,"price":float,"qty":float,"amt":float},index_col=0)
        if self.data.empty:
            self.last_index = -1
        else:
            self.last_index = self.data.index.max()

    def txn(self, date:datetime.date ,user:str ,token:str ,price:float, qty:float):
        amt = abs(price*qty)
        txn = pd.DataFrame({"date":date,"user":user,"token":token,"price":price,"qty":qty,"amt":amt},index=[self.last_index+1])
        self.data = pd.concat([txn,self.data],axis=0)
        self.last_index+=1
        return amt
    
    def fetch_user_data(self,user:str):
        return self.data[self.data["user"]==user]

    def fetch_token_data(self,user:str, token:str):
        return self.data[(self.data["user"]==user) & (self.data["token"]==token)]
    
    def fetch_token_netval(self,user:str, token:str, cprice:float):
        return self.fetch_token_data(user,token).sum()["qty"]*cprice

    def save_to_csv(self):
        self.data.to_csv(self.file,header=False)
        
    
    
if __name__ == "__main__":
    test=tradable("TCS.NS",date(2000,1,15), 21, False)
    x = test
    print(x)
    l = ledger(file="Stocksim/plot/data/ledger.csv")
    l.txn(date(2000,1,15),"user1","ASBL",100,1)
    l.txn(date(2000,1,15),"user1","ASBL",100,-1)
    token_data=l.fetch_token_data("user1","TCS.NS")
    get_config("admin","admin01")