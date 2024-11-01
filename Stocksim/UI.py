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
from plot.data import TR, TRD, TRDX
from plot.data import tradable
import mplfinance as mpf
from functools import partial
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

code = "AAPL"
ddays = 21
edate = datetime(2023,2,1).date()
sdate = edate - timedelta(days=ddays)
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
        self.date = edate
        self.ndays = ddays
        self.trd = tradable(code,self.date,ddays)
        trd = self.trd
        self.configure(width=1280, height=720)
        
        self.startdate = trd.data.index[0].date()
        date = trd.data.index[-1].date()
        self.enddate = trd.data.index[-1].date()
        self.fig, self.ax = mpf.plot(trd.data, type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=1.4, panel_ratios=(3,1),tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        
        self.canvas.draw()
        self.canvas.get_tk_widget()
        self.canvas.get_tk_widget().grid(row=0,column=0)
        
    def upd(self, ncode=code, date=edate):
        plt.close()
        del self.fig, self.ax, self.canvas
        self.code = ncode
        trd = tradable(self.code,date, ddays)
        self.fig, self.ax = mpf.plot(trd.data, type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=1.4, panel_ratios=(3,1),tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget()
        self.canvas.get_tk_widget().grid(row=0,column=0)
        
        
class tab(ctk.CTkFrame):
    def __init__(self, parent, Code, Name, Curr, Dperc):
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

class UI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StockSim")
        x = (self.winfo_screenwidth()-1280)//2
        y = (self.winfo_screenheight()-720)//2
        # self.wm_attributes("-fullscreen", True)
        self.resizable(False, False)
        self.geometry('%dx%d+%d+%d' % (1280, 720, x, y))
        # self.wm_attributes("-alpha","0.9")
    def home(self):
        i = None
        self.btndict = {}
        self.lddict = {i:tradable(i,edate,ddays,True).data for i in TR}
        def View(Tcode):
            for i in self.btndict:
                if i == Tcode:
                    self.btndict[i].tradbutton.configure(state="disabled")
                    # print("hi")
                else:
                    self.btndict[i].tradbutton.configure(state="normal")
                    # print("bye")
            self.graphspace.upd(Tcode)
        # def buy():
        #     self.buy.configure(height=24,text="Confirm?", command=confirm)
        #     self.entry.grid(row=4,column=0,rowspan=1,columnspan=1)
        #     self.buy.grid_configure(row=5,column=0,rowspan=1,columnspan=1)
        #     self.sell.configure(text="Cancel",command=cancel)
        # def sell():
        #     self.sell.configure(height=24, text="Confirm?", command=confirm)
        #     self.entry.grid(row=4,column=1,rowspan=1,columnspan=1)
        #     self.sell.grid_configure(row=5,column=1,rowspan=1,columnspan=1)
        #     self.buy.configure(text="Cancel",command=cancel)
        # def confirm():
        #     self.buy.configure(text="Buy", command=buy,height=48)
        #     self.sell.configure(text="Sell", command=sell,height=48)
        #     self.entry.grid_forget()
        #     self.buy.grid_configure(row=4,column=0,rowspan=2,columnspan=1)
        #     self.sell.grid_configure(row=4,column=1,rowspan=2,columnspan=1)
        # def cancel():
        #     self.buy.configure(text="Buy", command=buy,height=48)
        #     self.sell.configure(text="Sell", command=sell,height=48)
        #     self.entry.grid_forget()
        #     self.buy.grid_configure(row=4,column=0,rowspan=2,columnspan=1)
        #     self.sell.grid_configure(row=4,column=1,rowspan=2,columnspan=1)
            
        self.leftframe = ctk.CTkFrame(self, width=tw, height=720, corner_radius=0,fg_color="#23232d")
        self.tlable = ctk.CTkLabel(self.leftframe, text="Tokens",height=34, width=tw, font=("Arial", 20),bg_color="#2b2b2b").pack()
        for i in TR:
            self.btndict[i]= tab(self.leftframe, i, TR[i], self.lddict[i]["Close"].round(1).values[0], self.lddict[i]["D%"].round(1).values[0])
        for i in self.btndict:
            self.btndict[i].pack(anchor="w", pady=(0,1))
        
        self.topbar = ctk.CTkFrame(self, width=1280-60-2*tw,height=48,fg_color="#0ff")
        for i in self.btndict:
            self.btndict[i].tradbutton.configure(command=partial(View, i))
        
        self.topbar = ctk.CTkFrame(self, width=1280-60-2*tw,height=48,fg_color="#0ff")
        # self.toprightframe = ctk.CTkFrame(self, width=tw, height=360, corner_radius=0, fg_color="#000",border_color="#000",border_width=5)
        # self.trf_name = ctk.CTkLabel(self.toprightframe, text="Name",width=tw, height=24,anchor="w", bg_color="#000",pady=10,padx=5)
        # self.trf_code = ctk.CTkLabel(self.toprightframe, font=("Helvetica",18),text="Code", width=tw ,height=24,anchor="w", bg_color="#000",pady=10, padx=5)
        # self.trf_curr = ctk.CTkLabel(self.toprightframe,text="Curr", font=("Helvetica",40,"bold"),width=tw//2 ,height=48,anchor="w", bg_color="#000",pady=10,padx=5)
        # self.trf_d = ctk.CTkLabel(self.toprightframe,text="D",width=tw//2 ,height=24,anchor="e", bg_color="#000",pady=10,padx=5)
        # self.trf_dperc = ctk.CTkLabel(self.toprightframe,text="D%",width=tw//2 ,height=24,anchor="e", bg_color="#000",pady=10,padx=5)
        # self.buy = ctk.CTkButton(self.toprightframe, text="Buy", width=tw//2, height=48, command=buy)
        # self.sell = ctk.CTkButton(self.toprightframe, text="Sell", width=tw//2, height=48, command=sell)
        # self.entry = ctk.CTkEntry(self.toprightframe, width=tw//2, height=24, placeholder_text="Enter Units")
        
        # self.aag = ctk.CTkLabel(self.toprightframe, text="At A Glance DD/MM/YYYY", fg_color="#000", width=tw, height=24)
        # self.lopen = ctk.CTkLabel(self.toprightframe, text="Open", fg_color="#000", width=tw//2, height=24, anchor="w", padx=5)
        # self.lopenv = ctk.CTkLabel(self.toprightframe, text="Open", fg_color="#000", width=tw//2, height=24, anchor="w")
        # self.lhigh = ctk.CTkLabel(self.toprightframe, text="High", fg_color="#000", width=tw//2, height=24, anchor="w",padx=5)
        # self.lhighv = ctk.CTkLabel(self.toprightframe, text="High", fg_color="#000", width=tw//2, height=24, anchor="w")
        # self.llow = ctk.CTkLabel(self.toprightframe, text="Low", fg_color="#000", width=tw//2, height=24, anchor="w",padx=5)
        # self.llowv = ctk.CTkLabel(self.toprightframe, text="Low", fg_color="#000", width=tw//2, height=24, anchor="w")
        # self.lclose = ctk.CTkLabel(self.toprightframe, text="Close", fg_color="#000", width=tw//2, height=24, anchor="w",padx=5)
        # self.lclosev = ctk.CTkLabel(self.toprightframe, text="Close", fg_color="#000", width=tw//2, height=24, anchor="w")
        # self.lshares = ctk.CTkLabel(self.toprightframe, text="Shares",justify="center", fg_color="#000", width=tw//2, height=24)
        # self.lnetval = ctk.CTkLabel(self.toprightframe, text="Net Value",justify="center", fg_color="#000", width=tw//2, height=24)
        # self.shares = ctk.CTkLabel(self.toprightframe, text="$Shares", fg_color="#000",justify="center", width=tw//2, height=48)
        # self.netval = ctk.CTkLabel(self.toprightframe, text="$Net Value", fg_color="#000",justify="center", width=tw//2, height=48)
        
        
        # self.botrightframe = ctk.CTkFrame(self, width=tw, height=360, corner_radius=0, fg_color="#fff",border_color="#000",border_width=5)
        # self.history = ctk.CTkLabel(self.botrightframe, text="History", fg_color="#fff", width=tw, height=12)
        
        # self.iconframe = ctk.CTkFrame(self,fg_color="gray", width=60, height=720, corner_radius=0)
        
        self.graphspace = customcandlestick(self)
        
        self.calentry = ctk.CTkEntry(self, width=tw//2+2, height=6, placeholder_text="Enter End Date DD/MM/YYYY", border_width=1, border_color="#000")
        self.ndaysentry = ctk.CTkEntry(self, width=tw//2+2, height=6, placeholder_text="Enter Number of Days", border_width=1, border_color="#000")
        self.ndaysentry.insert(0,ddays)
        self.currd = ctk.CTkLabel(self,text="Curently Displaying: {} thru {}".format(self.graphspace.startdate, self.graphspace.enddate), fg_color="#000", width=tw//2+2, height=6, anchor="w",padx=5)
        self.go = ctk.CTkButton(self,text="Go",height=48,width=48,command=lambda: go(self.calentry.get(), self.ndaysentry.get()))
        
        def go(date, ndays):
            global edate, ddays
            edate = datetime.strptime(date, "%d/%m/%Y").date()
            ddays = int(ndays)
        
        # print(self.btndict)
        # self.btndict["ASBL"].tradbutton.configure(state="disabled")
        # self.trf_name.grid(row=0,column=0, columnspan=2, rowspan=1)
        # self.trf_code.grid(row=1,column=0, columnspan=2, rowspan=1)
        # self.trf_curr.grid(row=2,column=0,columnspan=1, rowspan=2)
        # self.trf_d.grid(row=2,column=1,columnspan=1, rowspan=1)
        # self.trf_dperc.grid(row=3,column=1,columnspan=1, rowspan=1)
        # self.buy.grid(row=4,column=0,columnspan=1, rowspan=2)
        # self.sell.grid(row=4,column=1,columnspan=1, rowspan=2)
        # self.aag.grid(row=6,column=0,columnspan=2, rowspan=1)
        # self.lopen.grid(row=7,column=0,columnspan=1, rowspan=1)
        # self.lopenv.grid(row=7,column=1,columnspan=1, rowspan=1)
        # self.lhigh.grid(row=8,column=0,columnspan=1, rowspan=1)
        # self.lhighv.grid(row=8,column=1,columnspan=1, rowspan=1)
        # self.llow.grid(row=9,column=0,columnspan=1, rowspan=1)
        # self.llowv.grid(row=9,column=1,columnspan=1, rowspan=1)
        # self.lclose.grid(row=10,column=0,columnspan=1, rowspan=1)
        # self.lclosev.grid(row=10,column=1,columnspan=1, rowspan=1)
        # self.lshares.grid(row=11,column=0,columnspan=1, rowspan=1)
        # self.lnetval.grid(row=11,column=1,columnspan=1, rowspan=1)
        # self.shares.grid(row=12,column=0,columnspan=1, rowspan=2)
        # self.netval.grid(row=12,column=1,columnspan=1, rowspan=2)
        
        # self.history.grid(row=0,column=0, columnspan=2, rowspan=1)
        
        # self.iconframe.place(x=0,y=0)
        self.leftframe.place(x=0,y=0)
        self.calentry.place(x=20+tw,y=0)
        self.ndaysentry.place(x=20+tw,y=24)
        self.go.place(x=20+tw+tw//2+2,y=0)
        self.currd.place(x=20+tw,y=48)
        # self.topbar.place(x=60+tw,y=0)
        # self.toprightframe.place(x=1280-tw,y=0)
        # self.botrightframe.place(x=1280-tw,y=360)
        self.graphspace.place(x=20+tw, y=48)
app = UI()
app.home()
app.mainloop()