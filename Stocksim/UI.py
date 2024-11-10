"""
TODO:
CLI(Text and minimal visuals) based modern looking stock market simulator
working principal
1) will fetch week wise stock price over an year or so of about 10 tradables
2) assign random code to each stock (ADBE, TSLA)
k) at every 10 second update the price according to the data (ie simulate actual holding of stock but squeeze yearlong waiting period into a few minutes)
4) allow user to simulate the buying/selling stocks
5) show percentage loss/profit at end of each week
6) show the graph of the stock price
7) have a watchlist
8) have a portfolio

www.16colo.rs
"""
from plot.data import TRD, TRDX
from plot.data import tradable, chk_usr_pwd, ledger
import mplfinance as mpf
from functools import partial
import customtkinter as ctk
import tkinter.messagebox as mb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import sys

xledger = ledger("Stocksim/plot/data/ledger.csv")
liq = 9000
xcode = "COMO"
ddays = 21
sdate = datetime(2023,2,4).date()
edate = None
bw = 110
tw = (bw*2)+48
usr = "admin"
pwd = "admin"
tasv = sum(xledger.fetch_user_data(usr)["amt"].round(2))
tval = liq+tasv

def on_exit():
    xledger.data.to_csv("Stocksim/plot/data/ledger.csv")
    sys.exit()

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

class customcandlestick(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        global xcode, ddays, edate, sdate, bw, tw
        self.date = sdate
        self.ndays = ddays
        self.trd = tradable(xcode,self.date,ddays)
        self.configure(width=1280, height=720)
        
        sdate = self.trd.data.index[0].date()
        edate = self.trd.data.index[-1].date()
        self.fig, self.ax = mpf.plot(self.trd.data,title=TRDX[xcode], type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=1, panel_ratios=(3,1),tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        
        self.canvas.draw()
        self.canvas.get_tk_widget()
        self.canvas.get_tk_widget().grid(row=0,column=0)

    def upd(self, ndate=sdate, ndays=ddays, isforward=True):
        global xcode, ddays, edate, sdate, bw, tw
        print(xcode)
        plt.close()
        del self.fig, self.ax, self.canvas, self.trd
        self.code = xcode
        self.trd = tradable(self.code,ndate,ndays, forward=isforward)
        sdate = self.trd.data.index[0].date()
        edate = self.trd.data.index[-1].date()
        self.fig, self.ax = mpf.plot(self.trd.data, title=TRDX[xcode], type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=1, panel_ratios=(3,1),tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,column=0)
    
class tab(ctk.CTkFrame):
    def __init__(self, parent, Code, Curr, Dperc):
        global xcode, ddays, edate, sdate, bw, tw
        super().__init__(parent)
        labelc="#000"
        self.Tcode = Code
        self.code = ctk.CTkLabel(self, text=Code,font=("Arial", 12, "bold"),padx=5,width=bw, height=24,anchor="w",bg_color=labelc)
        self.name = ctk.CTkLabel(self, text=TRDX[Code],width=bw,font=('Helevtica',10, "italic"),text_color="grey",padx=5, height=24,anchor="w",bg_color=labelc)
        self.curr = ctk.CTkLabel(self, text=str(Curr)+" USD",width=bw, height=24,anchor="e",bg_color=labelc)
        self.Dperc = ctk.CTkLabel(self, text=str(Dperc)+"%",width=bw, height=24,anchor="e",bg_color=labelc)
        self.tradbutton = ctk.CTkButton(self, text="View", width=48, height=48, corner_radius=10, fg_color="#202020",anchor="c")
        
        if Dperc > 0:
            self.Dperc.configure(text_color="#3dc985")
        else:
            self.Dperc.configure(text_color="#ef4f60")
        
        self.code.grid(row=0,column=0)
        self.name.grid(row=1,column=0)
        self.curr.grid(row=0,column=1)
        self.Dperc.grid(row=1,column=1)
        self.tradbutton.grid(row=0,column=2,rowspan=2)

    def upd(self,Curr,Dperc):
        global xcode, ddays, edate, sdate, bw, tw
        self.curr.configure(text=str(Curr)+" USD")
        self.Dperc.configure(text=str(Dperc)+"%")
        if Dperc > 0:
            self.Dperc.configure(text_color="#3dc985")
        else:
            self.Dperc.configure(text_color="#ef4f60")


class UI(ctk.CTk):
    def __init__(self):
        global xcode, ddays, edate, sdate, bw, tw, tasv
        super().__init__()
        self.title("StockSim")
        x = (self.winfo_screenwidth()-1280)//2
        y = (self.winfo_screenheight()-720)//2
        self.resizable(False, False)
        self.geometry('%dx%d+%d+%d' % (1280, 720, x, y))
        self.wm_attributes("-alpha","0.9")
        # self.login()
    
    def login(self):
        global xcode, ddays, edate, sdate, bw, tw, usr, pwd, liq
        self.loginw = ctk.CTkToplevel(self)
        self.loginw.title("Login")
        self.loginw.geometry("200x200")
        # self.loginw.resizable(False, False)
        self.loginw.wm_attributes("-alpha","0.9","-topmost","True")
        self.loginw.protocol("WM_DELETE_WINDOW",sys.exit)

        def loginx(event): # Event for bind 
            global xcode, ddays, edate, sdate, bw, tw, usr, pwd, liq, tasv, tval
            usr = self.usren.get()
            pwd = self.pwden.get()
            print(usr)
            print(pwd)
            
            match chk_usr_pwd(usr,pwd)[0]: # fancy if-elif
                case 200:
                    liq = chk_usr_pwd(usr,pwd)[1]
                    tasv = sum(xledger.fetch_user_data(usr)["amt"].round(2))
                    tval = tasv+liq
                    print(tasv)
                    self.loginw.destroy()
                    self.home()
                case 401:
                    mb.showerror(title="Error", message="Check your password".format(usr), icon="info", type=mb.OK)
                case 400:
                    msg = mb.showerror(title="Error", message="No user named {}, Do you want to create one?".format(usr), icon="info", type=mb.YESNO)
                    
                    if msg == "yes" and len(pwd)>5:
                        self.loginw.destroy()
                        with open("Stocksim/plot/data/userdata.csv","a") as file:
                            file.write("{},{},{},\n".format(usr,pwd,10000))
                        self.login()
                    else:
                        mb.showerror(title="Error", message="Check your password".format(usr), icon="info", type=mb.OK)
                    
                        
                    
        self.usren = ctk.CTkEntry(self.loginw, width=200, height=32, placeholder_text="Username")
        self.pwden = ctk.CTkEntry(self.loginw, width=200, height=32, placeholder_text="Password", show="*")
        self.loginbtn = ctk.CTkButton(self.loginw, text="Login", width=100, height=32, command=partial(loginx,None))

        self.pwden.bind("<Return>", command=loginx)
        
        self.usren.grid(row=0,column=0,pady=10)
        self.pwden.grid(row=1,column=0,pady=10)
        self.loginbtn.grid(row=2,column=0,pady=10)
        
    def home(self):
        print(usr,pwd)
        global xcode, ddays, edate, sdate, bw, tw, tasv
        i = None
        self.btndict = {}
        self.lddict = {i:tradable(i,sdate,ddays,True).data for i in TRD}
        self.tokenledger = xledger.fetch_token_data(usr,xcode)
        self.userledger = xledger.fetch_user_data(usr)
        print(self.tokenledger)
        
        def Trade(Tcode):
            global xcode, ddays, edate, sdate, bw, tw
            del xcode
            xcode = Tcode
            print(xcode)
            for i in self.btndict:
                if i == Tcode:
                    self.btndict[i].tradbutton.configure(state="disabled")
                else:
                    self.btndict[i].tradbutton.configure(state="normal")
            self.trf_name.configure(text=TRDX[Tcode])
            self.trf_code.configure(text=Tcode)
            self.trf_curr.configure(text=str(self.lddict[Tcode]["Close"].iloc[0].round(1)))
            self.trf_d.configure(text=str(self.lddict[Tcode]["D"].iloc[0].round(1))+" USD")
            self.trf_dperc.configure(text=str(self.lddict[Tcode]["D%"].iloc[0].round(1))+"%")

            self.graphspace.upd(ndate=sdate, ndays=ddays)
            self.currd.configure(text="Curently Displaying: {} thru {}".format(sdate, edate))

        
        def go(date, ndays, isforward=True):
            global xcode, ddays, edate, sdate, bw, tw
            if date == "exit":
                self.destroy()
            ddays = ndays
            sdate = datetime.strptime(date, "%d/%m/%Y").date()
            ddays = int(ndays.strip().split(" ")[0])
            self.graphspace.upd(ndate=sdate, ndays=ddays, isforward=isforward)
            self.lddict = {i:tradable(i,sdate,ddays,True,isforward).data for i in TRDX}
            
            for i in self.btndict:
                self.btndict[i].upd(self.lddict[i]["Close"].iloc[0].round(1), self.lddict[i]["D%"].iloc[0].round(1))
            self.currd.configure(text="Curently Displaying: {} thru {}".format(sdate, edate))

        def buy():
            self.buy.configure(height=24,text="Confirm?", command=confirm)
            self.entry.grid(row=4,column=0,rowspan=1,columnspan=1)
            self.buy.grid_configure(row=5,column=0,rowspan=1,columnspan=1)
            self.sell.configure(text="Cancel",command=cancel)
        def sell():
            self.sell.configure(height=24, text="Confirm?", command=confirm)
            self.entry.grid(row=4,column=1,rowspan=1,columnspan=1)
            self.sell.grid_configure(row=5,column=1,rowspan=1,columnspan=1)
            self.buy.configure(text="Cancel",command=cancel)
        def confirm():
            self.buy.configure(text="Buy", command=buy,height=48)
            self.sell.configure(text="Sell", command=sell,height=48)
            self.entry.grid_forget()
            self.buy.grid_configure(row=4,column=0,rowspan=2,columnspan=1)
            self.sell.grid_configure(row=4,column=1,rowspan=2,columnspan=1)
        def cancel():
            self.buy.configure(text="Buy", command=buy,height=48)
            self.sell.configure(text="Sell", command=sell,height=48)
            self.entry.grid_forget()
            self.buy.grid_configure(row=4,column=0,rowspan=2,columnspan=1)
            self.sell.grid_configure(row=4,column=1,rowspan=2,columnspan=1)
            
        self.leftframe = ctk.CTkFrame(self, width=tw, height=720, corner_radius=0,fg_color="#000")
        self.tlable = ctk.CTkLabel(self.leftframe, text="Tradables",height=48, width=tw, font=("Arial", 20),bg_color="#2b2b2b").pack()
        for i in TRDX:
            self.btndict[i]= tab(self.leftframe, i, self.lddict[i]["Close"].iloc[0].round(1), self.lddict[i]["D%"].iloc[0].round(1))
        for i in self.btndict:
            self.btndict[i].tradbutton.configure(command=partial(Trade, i))
            self.btndict[i].pack(anchor="w")
        
        self.graphspace = customcandlestick(self)
        
        self.topbar = ctk.CTkFrame(self, width=1280-60-2*tw,height=48)
        self.usrname = ctk.CTkLabel(self.topbar, text="User: {}".format(usr), width=tw, height=24, padx=10, fg_color="#000")
        self.tlab = ctk.CTkLabel(self.topbar, text="Total Value", width=610-tw, height=10, fg_color="#000")
        self.tvlab = ctk.CTkLabel(self.topbar, text=tval, width=610-tw, height=36, fg_color="#000")
        self.liqlab = ctk.CTkLabel(self.topbar, text="Liquid Assets", width=305-tw//2, height=10, fg_color="#000")
        self.liqvlab = ctk.CTkLabel(self.topbar, text=liq, width=305-tw//2, height=36, fg_color="#000")
        self.taslab = ctk.CTkLabel(self.topbar, text="Assets Value", width=305-tw//2, height=10,  fg_color="#000")
        self.tasvlab = ctk.CTkLabel(self.topbar, text=tasv, width=305-tw//2, height=36,  fg_color="#000")
        # self.usrname.pack()
        
        
        
        self.currd = ctk.CTkLabel(self,text="Curently Displaying: {} thru {}".format(sdate, edate), fg_color="#000", width=tw//2+2, height=6, anchor="w",padx=5)
        self.toprightframe = ctk.CTkFrame(self, width=tw, height=360, corner_radius=0, fg_color="#000",border_color="#000",border_width=5)
        self.trf_name = ctk.CTkLabel(self.toprightframe, text=TRDX[xcode],width=tw, height=24,anchor="w", bg_color="#000",pady=10,padx=5)
        self.trf_code = ctk.CTkLabel(self.toprightframe, font=("Helvetica",18),text=xcode, width=tw ,height=24,anchor="w", bg_color="#000",pady=10, padx=5)
        self.trf_curr = ctk.CTkLabel(self.toprightframe,text=str(self.lddict[xcode]["Close"].iloc[0].round(1)), font=("Helvetica",40,"bold"),width=tw//2 ,height=48,anchor="w", bg_color="#000",pady=10,padx=5)
        self.trf_d = ctk.CTkLabel(self.toprightframe,text=str(self.lddict[xcode]["D"].iloc[0].round(1))+" USD",width=tw//2 ,height=24,anchor="e", bg_color="#000",pady=10,padx=5)
        self.trf_dperc = ctk.CTkLabel(self.toprightframe,text=str(self.lddict[xcode]["D%"].iloc[0].round(1))+"%",width=tw//2 ,height=24,anchor="e", bg_color="#000",pady=10,padx=5)
        self.buy = ctk.CTkButton(self.toprightframe, text="Buy", width=tw//2, height=48, command=buy)
        self.sell = ctk.CTkButton(self.toprightframe, text="Sell", width=tw//2, height=48, command=sell)
        self.entry = ctk.CTkEntry(self.toprightframe, width=tw//2, height=24, placeholder_text="Enter Units")
        
        self.aag = ctk.CTkLabel(self.toprightframe, text="At A Glance {}".format(edate), fg_color="#000", width=tw, height=24)
        self.lopen = ctk.CTkLabel(self.toprightframe, text="Open", fg_color="#000", width=tw//2, height=24, anchor="w", padx=5)
        self.lhigh = ctk.CTkLabel(self.toprightframe, text="High", fg_color="#000", width=tw//2, height=24, anchor="w",padx=5)
        self.llow = ctk.CTkLabel(self.toprightframe, text="Low", fg_color="#000", width=tw//2, height=24, anchor="w",padx=5)
        self.lclose = ctk.CTkLabel(self.toprightframe, text="Close", fg_color="#000", width=tw//2, height=24, anchor="w",padx=5)
        self.lshares = ctk.CTkLabel(self.toprightframe, text="Shares",justify="center", fg_color="#000", width=tw//2, height=24)
        self.lnetval = ctk.CTkLabel(self.toprightframe, text="Net Value",justify="center", fg_color="#000", width=tw//2, height=24)
        
        self.lopenv = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["Open"].iloc[0].round(1), fg_color="#000", width=tw//2, height=24, anchor="w")
        self.lhighv = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["High"].iloc[0].round(1), fg_color="#000", width=tw//2, height=24, anchor="w")
        self.llowv = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["Low"].iloc[0].round(1), fg_color="#000", width=tw//2, height=24, anchor="w")
        self.lclosev = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["Close"].iloc[0].round(1), fg_color="#000", width=tw//2, height=24, anchor="w")
    
    
        self.shares = ctk.CTkLabel(self.toprightframe, text="$Shares", fg_color="#000",justify="center", width=tw//2, height=48)
        self.netval = ctk.CTkLabel(self.toprightframe, text="$Net Value", fg_color="#000",justify="center", width=tw//2, height=48)
        self.prev = ctk.CTkButton(self,text="<",font=("Helvetica",30,"bold"),width=28,height=34,corner_radius=1024, command= lambda: go(date = (sdate-timedelta(days=1)).strftime('%d/%m/%Y'), ndays = str(ddays)+" Days", isforward=False))
        self.next = ctk.CTkButton(self,text=">",font=("Helvetica",30,"bold"),width=28,height=34,corner_radius=1024, command= lambda: go(date = (sdate+timedelta(days=1)).strftime('%d/%m/%Y'), ndays = str(ddays)+" Days"))
        
        self.botrightframe = ctk.CTkFrame(self, width=tw, height=360, corner_radius=0, fg_color="#fff",border_color="#000",border_width=5)
        
        self.iconframe = ctk.CTkFrame(self,fg_color="gray", width=60, height=720, corner_radius=0)
        
        
        # print(self.btndict)
        self.tlab.grid(row=0,column=0)
        self.tvlab.grid(row=1,column=0)
        self.liqlab.grid(row=0,column=1)
        self.liqvlab.grid(row=1,column=1)
        self.taslab.grid(row=0,column=2)
        self.tasvlab.grid(row=1,column=2)
        
        self.btndict["ASBL"].tradbutton.configure(state="disabled")
        self.trf_name.grid(row=0,column=0, columnspan=2, rowspan=1)
        self.trf_code.grid(row=1,column=0, columnspan=2, rowspan=1)
        self.trf_curr.grid(row=2,column=0,columnspan=1, rowspan=2)
        self.trf_d.grid(row=2,column=1,columnspan=1, rowspan=1)
        self.trf_dperc.grid(row=3,column=1,columnspan=1, rowspan=1)
        self.buy.grid(row=4,column=0,columnspan=1, rowspan=2)
        self.sell.grid(row=4,column=1,columnspan=1, rowspan=2)
        self.aag.grid(row=6,column=0,columnspan=2, rowspan=1)
        self.lopen.grid(row=7,column=0,columnspan=1, rowspan=1)
        self.lopenv.grid(row=7,column=1,columnspan=1, rowspan=1)
        self.lhigh.grid(row=8,column=0,columnspan=1, rowspan=1)
        self.lhighv.grid(row=8,column=1,columnspan=1, rowspan=1)
        self.llow.grid(row=9,column=0,columnspan=1, rowspan=1)
        self.llowv.grid(row=9,column=1,columnspan=1, rowspan=1)
        self.lclose.grid(row=10,column=0,columnspan=1, rowspan=1)
        self.lclosev.grid(row=10,column=1,columnspan=1, rowspan=1)
        self.lshares.grid(row=11,column=0,columnspan=1, rowspan=1)
        self.lnetval.grid(row=11,column=1,columnspan=1, rowspan=1)
        self.shares.grid(row=12,column=0,columnspan=1, rowspan=2)
        self.netval.grid(row=12,column=1,columnspan=1, rowspan=2)
        
        self.graphspace.place(x=60+tw, y=48+48)
        self.iconframe.place(x=0,y=0)
        self.currd.place(x=20+tw,y=48)
        self.leftframe.place(x=60,y=0)
        self.topbar.place(x=60+tw,y=0)
        self.toprightframe.place(x=1280-tw,y=0)
        self.botrightframe.place(x=1280-tw,y=360)
        # self.prev.place(x=1280-500,y=0)
        # self.next.place(x=1280-80-500,y=0)
        
    def next_day(self):
        sdate = sdate + timedelta(days=1)

app = UI()
app.protocol("WM_DELETE_WINDOW", sys.exit)
app.home()
app.mainloop()