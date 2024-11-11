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
from dataVo import TR, TRD, TRDX
from plot.data import tradable
import mplfinance as mpf
from functools import partial
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import sys

xcode = "KO"
ddays = 21
sdate = datetime(2023,2,4).date()
edate = None
bw = 150
tw = (bw*2)+48

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
        self.fig, self.ax = mpf.plot(self.trd.data,title=TR[xcode], type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=1, panel_ratios=(3,1),tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        
        self.canvas.draw()
        self.canvas.get_tk_widget()
        self.canvas.get_tk_widget().grid(row=0,column=0)
        
    def upd(self, ncode=xcode, ndate=sdate, ndays=ddays, isforward=True):
        global xcode, ddays, edate, sdate, bw, tw
        plt.close()
        del self.fig, self.ax, self.canvas, self.trd
        self.code = ncode
        self.trd = tradable(self.code,ndate,ndays, forward=isforward)
        sdate = self.trd.data.index[0].date()
        edate = self.trd.data.index[-1].date()
        self.fig, self.ax = mpf.plot(self.trd.data, title=TR[xcode], type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=1, panel_ratios=(3,1),tight_layout=True)
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
        self.name = ctk.CTkLabel(self, text=TR[Code],width=bw,font=('Helevtica',10, "italic"),text_color="grey",padx=5, height=24,anchor="w",bg_color=labelc)
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
        global xcode, ddays, edate, sdate, bw, tw
        super().__init__()
        self.title("StockSim")
        x = (self.winfo_screenwidth()-1280)//2
        y = (self.winfo_screenheight()-720)//2
        self.resizable(False, False)
        self.geometry('%dx%d+%d+%d' % (1280, 720, x, y))
        self.wm_attributes("-alpha","0.9")
    def home(self):
        global xcode, ddays, edate, sdate, bw, tw
        i = None
        self.btndict = {}
        self.lddict = {i:tradable(i,sdate,ddays,True).data for i in TR}
        
        def view(Tcode):
            global xcode, ddays, edate, sdate, bw, tw
            for i in self.btndict:
                if i == Tcode:
                    self.btndict[i].tradbutton.configure(state="disabled",text="O")
                else:
                    self.btndict[i].tradbutton.configure(state="normal", text="View")
            del xcode
            xcode = Tcode
            self.graphspace.upd(ncode=xcode, ndate=sdate, ndays=ddays)
            self.currd.configure(text="Curently Displaying: {} thru {}".format(sdate, edate))
            
        def go(date, ndays, isforward=True):
            global xcode, ddays, edate, sdate, bw, tw
            if date == "exit":
                self.destroy()
            ddays = ndays
            sdate = datetime.strptime(date, "%d/%m/%Y").date()
            ddays = int(ndays.strip().split(" ")[0])
            self.graphspace.upd(ndate=sdate, ndays=ddays, isforward=isforward)
            self.lddict = {i:tradable(i,sdate,ddays,True,isforward).data for i in TR}
            
            for i in self.btndict:
                self.btndict[i].upd(self.lddict[i]["Close"].round(1).values[0], self.lddict[i]["D%"].round(1).values[0])
            self.currd.configure(text="Curently Displaying: {} thru {}".format(sdate, edate))
            
        self.leftframe = ctk.CTkFrame(self, width=tw, height=720, corner_radius=0,fg_color="#23232d")
        self.tlable = ctk.CTkLabel(self.leftframe, text="Tokens",height=34, width=tw, font=("Arial", 20),bg_color="#2b2b2b").pack()
        
        for i in TR:
            self.btndict[i]= tab(self.leftframe, i, self.lddict[i]["Close"].round(1).values[0], self.lddict[i]["D%"].round(1).values[0])
        for i in self.btndict:
            self.btndict[i].pack(anchor="w", pady=(0,1))
        
        self.topbar = ctk.CTkFrame(self, width=1280-60-2*tw,height=48,fg_color="#0ff")
        for i in self.btndict:
            self.btndict[i].tradbutton.configure(command=partial(view, i))
        
        self.topbar = ctk.CTkFrame(self, width=1280-60-2*tw,height=48,fg_color="#0ff")
        
        self.graphspace = customcandlestick(self)
        
        self.calentry = ctk.CTkEntry(self, width=tw//2+2, height=6, placeholder_text="Enter Date DD/MM/YYYY", border_width=1, border_color="#000")
        self.ndaysentry = ctk.CTkEntry(self, width=tw//2+2, height=6, placeholder_text="Enter Number of Days", border_width=1, border_color="#000")
        self.ndaysentry.insert(0,str(ddays)+" Days")
        self.currd = ctk.CTkLabel(self,text="Curently Displaying: {} thru {}".format(sdate, edate), fg_color="#000", width=tw//2+2, height=6, anchor="w",padx=5)
        self.go = ctk.CTkButton(self,text="Go",height=48,width=48,command=lambda: go(self.calentry.get(), self.ndaysentry.get()))
        self.prev = ctk.CTkButton(self,text="<",font=("Helvetica",30,"bold"),width=28,height=34,corner_radius=1024, command= lambda: go(date = (sdate-timedelta(days=1)).strftime('%d/%m/%Y'), ndays = str(ddays)+" Days", isforward=False))
        self.next = ctk.CTkButton(self,text=">",font=("Helvetica",30,"bold"),width=28,height=34,corner_radius=1024, command= lambda: go(date = (sdate+timedelta(days=1)).strftime('%d/%m/%Y'), ndays = str(ddays)+" Days"))
        
        self.leftframe.place(x=0,y=0)
        self.calentry.place(x=20+tw,y=0)
        self.ndaysentry.place(x=20+tw,y=24)
        self.go.place(x=20+tw+tw//2+2,y=0)
        self.currd.place(x=20+tw,y=48)
        self.prev.place(x=1280-136,y=0)
        self.next.place(x=1280-80,y=0)
        self.graphspace.place(x=20+tw, y=48)
app = UI()
app.protocol("WM_DELETE_WINDOW", sys.exit)
app.home()
app.mainloop()