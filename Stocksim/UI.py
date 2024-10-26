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
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

bw = 110
tw = (bw*2)+48

class customcandlestick(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(width=1280-60-2*tw, height=672-2*48, fg_color="#fcf")
        # self.canvas = 

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
        self.tradbutton = ctk.CTkButton(self, text="Trade", width=48, height=48, corner_radius=0, fg_color="#2b2b2b",anchor="c")
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