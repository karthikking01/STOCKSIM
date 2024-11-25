import pandas as pd
import yfinance as yf
from datetime import *

datelist = pd.read_csv("Stocksim/plot/data/datelist.csv", header=None)[0].tolist()

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
    
def get_tickers(usr):
    x = pd.read_csv("Stocksim/plot/data/tickers.csv",header=None, index_col=0, names=["ticker","name"])
    x = x[x.index == usr]
    x.index = x["ticker"]
    del x["ticker"]
    return x


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


def lff(name,sdate,dnrows):
    """Loads Data from file ranging from sdate to sdate+dnrows"""
    with open("Stocksim/plot/data/{}.csv".format(name), "r") as f:
        for count, l in enumerate(f): #count number of iterations ie lines moved
            print(l)
            if str(l).startswith(str(sdate)): # if line starts with sdate
                df = pd.read_csv("Stocksim/plot/data/{}.csv".format(name),header=None,index_col=0,skiprows=count,nrows=dnrows) #skip number of lines equal to count and read dnrows lines
                df.index = pd.to_datetime(df.index, format='%Y-%m-%d') # convert index to datetime
                df.index.name=None # removing index name
                df.columns = ["Open","High","Low","Close","Volume"] # renaming index columns to simpler ones
                df["D"] = df["Close"]-df["Open"] # change
                df["D%"] = df["D"]/df["Open"]*100 # perc change
                # df["height"] = df["High"]-df["Low"] # height
                break
    # try:
    #     return df
    # except UnboundLocalError:
    #     nextday = sdate+timedelta(days=1)
    #     return lff(name,nextday,dnrows)


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
    """Loads Ticker from Web"""
    tk = yf.Ticker(name) # get ticker (YahooFinance module)
    x = pd.DataFrame(tk.history(period="max"))
    x.index = [d.strftime('%Y-%m-%d') for d in x.index.date]
    x = x.drop(columns=["Dividends","Stock Splits"]).loc["2000-01-03":]
    if x.index[0] != "2000-01-03":
        finalindex = x.index[0]
        print(datelist.index("2001-01-03"))
        print(datelist[datelist.index("2000-01-03"):datelist.index(finalindex)])
        zeroindex = datelist[datelist.index("2000-01-03"):datelist.index(finalindex)]
        zdf = pd.DataFrame(0,columns=["Open","High","Low","Close","Volume"],index=zeroindex)
        x = pd.concat([zdf,x])
    x.to_csv("Stocksim/plot/data/{}.csv".format(name),header=False)
    del x
    

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
    # test=tradable("TCS.NS",date(2000,1,15), 21, False)
    # x = test
    # print(x)
    # l = ledger(file="Stocksim/plot/data/ledger.csv")
    # l.txn(date(2000,1,15),"user1","ASBL",100,1)
    # l.txn(date(2000,1,15),"user1","ASBL",100,-1)
    # token_data=l.fetch_token_data("user1","TCS.NS")
    # get_config("admin","admin01")
    print(get_tickers("user"))
    trx = tradable("LT.NS",date(2000,1,3), 21, False)
    print(trx)