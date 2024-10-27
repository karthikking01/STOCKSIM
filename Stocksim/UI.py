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
from plot.data import tradable
import mplfinance as mpf
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

bw = 110
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
        trd =  tradable("ASBL","2023-12-01", 100)
        self.configure(width=1280-60-2*268, height=672-48)

        self.fig, self.ax = mpf.plot(trd.data, type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, title="ASBL", ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False, panel_ratios=(3,1),tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        
class tab(ctk.CTkFrame):
    def __init__(self, parent, Code, Name, Curr, Dperc):
        super().__init__(parent)
        labelc="#000"
        self.configure(corner_radius=5)
        self.configure(width=tw, height=48)
        # bxn = ctk.CTkButton(self, text=str(Code), width=300, height=48, corner_radius=0, fg_color="#2b2b2b",anchor="nw")
        self.code = ctk.CTkLabel(self, text=Code,width=bw, height=24,anchor="w",bg_color=labelc)
        self.name = ctk.CTkLabel(self, text=TRDX[Code],width=bw, height=24,anchor="w",bg_color=labelc)
        self.curr = ctk.CTkLabel(self, text=Curr,width=bw, height=24,anchor="e",bg_color=labelc)
        self.Dperc = ctk.CTkLabel(self, text=Dperc,width=bw, height=24,anchor="e",bg_color=labelc)
        self.tradbutton = ctk.CTkButton(self, text="Trade", width=48, height=48, corner_radius=0, fg_color="#2b2b2b",anchor="c",command=self.chg)
        self.code.grid(row=0,column=0)
        self.name.grid(row=1,column=0)
        self.curr.grid(row=0,column=1)
        self.Dperc.grid(row=1,column=1)
        self.tradbutton.grid(row=0,column=2,rowspan=2)
    def chg(self):
        print("hi")
        self.tradbutton.configure(state="disabled")
        self.curr.configure(text="0")
        self.Dperc.configure(text="0")

class UI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StockSim")
        x = (self.winfo_screenwidth()-1280)//2
        y = (self.winfo_screenheight()-720)//2
        # self.wm_attributes("-fullscreen", True)
        self.resizable(False, False)
        self.geometry('%dx%d+%d+%d' % (1280, 720, x, y))
        self.wm_attributes("-alpha","0.9")
    def home(self):
        self.leftframe = ctk.CTkFrame(self, width=tw, height=720, corner_radius=0,fg_color="#000")
        self.topbar = ctk.CTkFrame(self, width=1280-60-2*tw,height=48,fg_color="#0ff")
        self.toprightframe = ctk.CTkFrame(self, width=tw, height=360, corner_radius=0, fg_color="#fff",border_color="#000",border_width=5)
        self.botrightframe = ctk.CTkFrame(self, width=tw, height=360, corner_radius=0, fg_color="#fff",border_color="#000",border_width=5)
        self.iconframe = ctk.CTkFrame(self,fg_color="gray", width=60, height=720, corner_radius=0)
        self.graphspace = customcandlestick(self).place(x=60+tw, y=48+48)
        self.tlable = ctk.CTkLabel(self.leftframe, text="Tradables",height=48, width=tw, font=("Arial", 20),bg_color="#2b2b2b").pack()
        self.btndict = {}
        for i in TRD:
            self.btndict[i]= tab(self.leftframe, i, TRD[i][0], "curr", "Dperc")
        for i in self.btndict:
            self.btndict[i].pack(anchor="w")
        # print(self.btndict)
        
        #matplotlib!
        
        self.btndict["ASBL"].tradbutton.configure(state="disabled")
        self.iconframe.place(x=0,y=0)
        self.leftframe.place(x=60,y=0)
        self.topbar.place(x=60+tw,y=0)
        self.toprightframe.place(x=1280-tw,y=0)
        self.botrightframe.place(x=1280-tw,y=360)
app = UI()
app.home()
app.mainloop()