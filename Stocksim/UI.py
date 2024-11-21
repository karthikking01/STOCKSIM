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
from plot.data import *
import mplfinance as mpf
from functools import partial
import customtkinter as ctk
from math import *
from PIL import Image
import tkinter.messagebox as mb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import sys

xledger = ledger("Stocksim/plot/data/ledger.csv")
xcode = "COMO"
ddays = 21
sdate = datetime(2000,1,3).date()
print(sdate)
edate = None
itertime = 5000
bw = 110
tw = (bw*2)+48
vw = 1180-2*tw
rfw = tw+40
usr = "admin"
pwd = "admin"
liq = None
play = True
tasv = 0
tval = None

images = {"home":ctk.CTkImage(light_image=Image.open("Stocksim/plot/data/images/home.png"),dark_image=Image.open("Stocksim/plot/data/images/home.png"),size=(25,25)), "pf":ctk.CTkImage(dark_image=Image.open("Stocksim/plot/data/images/pf.png"),size=(25,25))}
def save():
    xledger.save_to_csv()
    with open("Stocksim/plot/data/userdata.csv","a") as file:
        file.write("{},{},{},{},{},{},{}\n".format(usr,pwd,sdate,edate,ddays,itertime,liq))
    sys.exit()
class customcandlestick(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        global xcode, ddays, edate, sdate, bw, tw
        self.date = sdate
        self.ndays = ddays
        self.trd = tradable(xcode,self.date,ddays)
        self.configure(width=1280, height=720)
        
        sdate = self.trd.index[0].date()
        edate = self.trd.index[-1].date()
        self.fig, self.ax = mpf.plot(self.trd,title=TRDX[xcode], type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=0.8, panel_ratios=(3,1),tight_layout=False)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,column=0)
    

    def upd(self, ndate=sdate, ndays=ddays):
        global xcode, ddays, edate, sdate, bw, tw
        print(xcode)
        plt.close()
        del self.fig, self.ax, self.canvas, self.trd
        self.code = xcode
        self.trd = tradable(self.code,ndate,ndays,False)
        sdate = self.trd.index[0].date()
        edate = self.trd.index[-1].date()
        print(sdate,edate)
        self.fig, self.ax = mpf.plot(self.trd, title=TRDX[xcode], type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=0.8, panel_ratios=(3,1),tight_layout=False)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        
        self.canvas.get_tk_widget().grid(row=0,column=0)
        
    def show_history(self,UI):
        global play
        def on_exit():
            global play
            play = True
            UI.movedays(date=sdate)
            UI.histwin.destroy()
            
        
        play = False
        UI.histwin = ctk.CTkToplevel(UI)
        UI.histwin.title("History")
        UI.histwin.geometry("1280x720")
        
        data = loadhistory(xcode,edate)
        _fig, ax = mpf.plot(data, type="line",title=TRDX[xcode],datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=2, panel_ratios=(3,1),tight_layout=False)

        print(ax)
        
        canvas = FigureCanvasTkAgg(_fig, master=UI.histwin)

        canvas.draw()
        canvas.get_tk_widget().pack()
        
        UI.histwin.protocol("WM_DELETE_WINDOW", on_exit)
        
        # play = False
        # data = loadhistory(xcode,edate)
        # mpf.plot(data, type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",show_nontrading=False,figscale=2, panel_ratios=(3,1),tight_layout=False)
        # play = True
    
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
        self.configure(fg_color="#0b1015")
        x = (self.winfo_screenwidth()-1280)//2
        y = (self.winfo_screenheight()-720)//2
        self.resizable(False, False)
        self.geometry('%dx%d+%d+%d' % (1280, 730, x, y))
        
        self.login()
        self.iconframe = ctk.CTkFrame(self,fg_color="#151928", width=60, height=720, corner_radius=0)
        self.homeicon = ctk.CTkButton(self.iconframe, text=None,image=images["home"],height=60,width=60,command=self.home)
        self.portficon = ctk.CTkButton(self.iconframe,text=None,image=images["pf"],height=60,width=60,command=self.portf)
        # self.wm_attributes("-alpha","0.9")
        
    def botrightfill(self):
        rbw = tw+20
        for widget in self.botrightscrollable.winfo_children():
            widget.destroy()

        none = ctk.CTkLabel(self.botrightscrollable, text="Initiate a trade", fg_color="#151928", width=rbw, height=15)
        
        row1 = []
        for i in ["Date","Code","Price","Units","Amt","Action"]:
            row1.append(ctk.CTkLabel(self.botrightscrollable, text=i, fg_color="#151928", width=rbw//6, height=15))
        for i in row1:
            i.grid(row=0,column=row1.index(i))
            
        tokenledgerlist = {}

        for i in list(self.tokenledger.index):
            date_label = ctk.CTkLabel(self.botrightscrollable, text=self.tokenledger.loc[i, 'date'], font=("font77", 10), width=rbw//6, padx=5,fg_color="#000022")
            token_label = ctk.CTkLabel(self.botrightscrollable, text=self.tokenledger.loc[i, 'token'], font=("font77", 10), width=rbw//6,fg_color="#000033")
            price_label = ctk.CTkLabel(self.botrightscrollable, text=self.tokenledger.loc[i, 'price'].round(2), font=("font77", 11), width=rbw//6,fg_color="#000044")
            qty_label = ctk.CTkLabel(self.botrightscrollable, text=abs(self.tokenledger.loc[i, 'qty'].round(2)), font=("font77", 11), width=rbw//6,fg_color="#000055")
            amt_label = ctk.CTkLabel(self.botrightscrollable, text=self.tokenledger.loc[i, 'amt'].round(2), font=("font77", 11), width=rbw//6,fg_color="#000066")
            buy_sell_label = ctk.CTkLabel(self.botrightscrollable,text="$buysell", font=("font77", 11), width=rbw//6,fg_color="#000077")
            if self.tokenledger.loc[i, 'qty'] > 0:
                buy_sell_label.configure(text="Buy", text_color="#3dc985")
            else:
                buy_sell_label.configure(text="Sell", text_color="#ef4f60")
            
            rown=[date_label, token_label, price_label, qty_label, amt_label, buy_sell_label]
            
            for j in rown:
                if self.tokenledger.loc[i, 'qty'] > 0:
                    j.configure(text_color="#3dc985")
                else:
                    j.configure(text_color="#ef4f60")
            
            tokenledgerlist[i]=rown
        
        # self.tokenledgerlist = {i:(ctk.CTkLabel(self.botrightscrollable,text=self.tokenledger.loc[i,'date'],font=("font77",10),width=rbw//6,padx=5),ctk.CTkLabel(self.botrightscrollable,text=self.tokenledger.loc[i,'token'],font=("font77",10),width=rbw//6),ctk.CTkLabel(self.botrightscrollable,text=self.tokenledger.loc[i,'price'].round(2),font=("font77",11),width=rbw//6),ctk.CTkLabel(self.botrightscrollable,text=abs(self.tokenledger.loc[i,'qty'].round(2)),font=("font77",11),width=rbw//6),ctk.CTkLabel(self.botrightscrollable,text=self.tokenledger.loc[i,'amt'].round(2), font=("font77",11),width=rbw//6),ctk.CTkLabel(self.botrightscrollable,text="Buy" if self.tokenledger.loc[i,'qty'] > 0 else "Sell",font=("font77",11),width=rbw//6)) for i in list(self.tokenledger.index)}
        if self.tokenledger.empty:
            none.grid(row=1,column=0,rowspan=3,columnspan=6)
            return
        else:
            revkeys = sorted(list(tokenledgerlist.keys()),reverse=True)
            none.grid_forget()
            for c,i in enumerate(revkeys):
                for j in range(6):
                    tokenledgerlist[i][j].grid(row=c+1,column=j)
                    
    def toprightfill(self):
        self.trf_name.configure(text=TRDX[xcode])
        self.trf_code.configure(text=xcode)
        self.trf_curr.configure(text="$ "+str(self.lddict[xcode]["Close"].iloc[0].round(3)))
        self.trf_d.configure(text=str(self.lddict[xcode]["D"].iloc[0].round(3))+" USD")
        self.trf_dperc.configure(text=str(self.lddict[xcode]["D%"].iloc[0].round(3))+"%")   
        self.shares.configure(text=self.tokenledger["qty"].sum().round(2))
        self.netval.configure(text=str(round(self.lddict[xcode]["Close"].iloc[0]*self.userledger[self.userledger["token"]==xcode]["qty"].sum(),2))+"USD")
        self.lopenv.configure(text=self.lddict[xcode]["Open"].iloc[0].round(3))
        self.lhighv.configure(text=self.lddict[xcode]["High"].iloc[0].round(3))
        self.llowv.configure(text=self.lddict[xcode]["Low"].iloc[0].round(3))
        self.lclosev.configure(text=self.lddict[xcode]["Close"].iloc[0].round(3))

    def movedays(self,date, ndays=21, isforward=True):
        
        global xcode, ddays, edate, sdate, bw, tw,play
        if play:
            if date == "exit":
                self.destroy()

            ddays = ndays
            sdate = date
            
            self.graphspace.upd(ndate=sdate, ndays=ddays)
            self.lddict = {i:tradable(i,sdate,ddays,True) for i in TRDX}
            
            tasv=0
            for i in self.lddict:
                tasv += self.lddict[i]["Close"].iloc[0]*self.userledger[self.userledger["token"]==i]["qty"].sum()
            tasv = round(tasv,2)
            tval = tasv + liq
            tval = round(tval,2)
            
            self.topbar_children_dynamic["Liquid Assets"].configure(text=liq)
            self.topbar_children_dynamic["Assets Value"].configure(text=tasv)
            self.topbar_children_dynamic["Total Value"].configure(text=tval)
            
            for i in self.btndict:
                self.btndict[i].upd(self.lddict[i]["Close"].iloc[0].round(1), self.lddict[i]["D%"].iloc[0].round(1))
            self.toprightfill()
            self.currd.configure(text="Curently Displaying: {} thru {}".format(sdate, edate))
            self.after(itertime,partial(self.movedays,sdate+timedelta(days=1)))
            print(sdate,edate, itertime)
    
    
    def login(self):
        global xcode, ddays, edate, sdate, bw, tw, usr, pwd, liq
        self.loginw = ctk.CTkToplevel(self)
        self.loginw.title("Login")
        self.loginw.geometry("200x200")
        # self.loginw.resizable(False, False)
        self.loginw.wm_attributes("-alpha","0.9","-topmost","True")
        self.loginw.protocol("WM_DELETE_WINDOW",sys.exit)

        def loginx(event): # Event for bind 
            global xcode, ddays, edate, sdate, bw, tw, usr, pwd, liq, tasv, tval, itertime
            usr = self.usren.get()
            pwd = self.pwden.get()
            print(usr)
            print(pwd)
            
            config = get_config(usr,pwd)
            
            match config[0]: # fancy if-elif
                case 200:
                    sdate = config[1].date()
                    edate = config[2].date()
                    ddays = config[3]
                    itertime = config[4]
                    liq = round(config[5],2)
                    self.loginw.destroy()
                    self.home()
                    self.iconframe.place(x=0,y=0)
                    self.homeicon.place(x=0,y=0)
                    self.portficon.place(x=0,y=60)
                case 401:
                    mb.showerror(title="Error", message="Check your password".format(usr), icon="info", type=mb.OK)
                case 400:
                    msg = mb.showerror(title="Error", message="No user named {}, Do you want to create one?".format(usr), icon="info", type=mb.YESNO)
                    
                    if msg == "yes" and len(pwd)>5:
                        self.loginw.destroy()
                        with open("Stocksim/plot/data/userdata.csv","a") as file:
                            file.write("{},{},{},{},\n".format(usr,edate,pwd,10000))
                        self.login()
                    else:
                        mb.showerror(title="Error", message="Create a stronger password!".format(usr), icon="info", type=mb.OK)
                    
                        
                    
        self.usren = ctk.CTkEntry(self.loginw, width=200, height=32, placeholder_text="Username")
        self.pwden = ctk.CTkEntry(self.loginw, width=200, height=32, placeholder_text="Password", show="*")
        self.loginbtn = ctk.CTkButton(self.loginw, text="Login", width=100, height=32, command=partial(loginx,None))

        self.pwden.bind("<Return>", command=loginx)
        
        self.usren.grid(row=0,column=0,pady=10)
        self.pwden.grid(row=1,column=0,pady=10)
        self.loginbtn.grid(row=2,column=0,pady=10)
        
    def home(self):
        try:
            self.portfupperframe.destroy()
            self.portflowerframe.destroy()
        except:
            pass
        
        self.homeicon.configure(state="disabled")
        self.portficon.configure(state="normal")
        print(usr,pwd)
        global xcode, ddays, edate, sdate, bw, tw, tasv, play
        play = True
        i = None
        self.btndict = {}
        self.txnlist = []
        self.lddict = {i:tradable(i,sdate,ddays,True) for i in TRD}
        self.tokenledger = xledger.fetch_token_data(usr,xcode)
        self.userledger = xledger.fetch_user_data(usr)
        
        print(self.userledger)
        print(self.tokenledger)
        
        tasv=0
        for i in self.lddict:
            tasv += self.lddict[i]["Close"].iloc[0]*self.userledger[self.userledger["token"]==i]["qty"].sum()
        tasv = round(tasv,2)
        tval = round(tasv + liq,2)            
        print(self.tokenledger)
        def Trade(Tcode):
            global xcode, ddays, edate, sdate, bw, tw
            del xcode
            xcode = Tcode
            print(xcode)
            self.tokenledger = xledger.fetch_token_data(usr,xcode)
            self.userledger = xledger.fetch_user_data(usr)
            self.toprightfill()
            self.botrightfill()
            
            for i in self.btndict:
                if i == Tcode:
                    self.btndict[i].tradbutton.configure(state="disabled")
                else:
                    self.btndict[i].tradbutton.configure(state="normal")

            self.graphspace.upd(ndate=sdate, ndays=ddays)
            self.currd.configure(text="Curently Displaying: {} thru {}".format(sdate, edate))

        def buy():
            self.buy.configure(height=24,text="Confirm?",font=("Helvetica",15,"bold"), command=partial(confirm, "buy"))
            self.entry.grid(row=4,column=0,rowspan=1,columnspan=1)
            self.buy.grid_configure(row=5,column=0,rowspan=1,columnspan=1)
            self.sell.configure(text="Cancel",command=cancel)
        def sell():
            self.sell.configure(height=24, text="Confirm?",font=("Helvetica",15,"bold"), command=partial(confirm, "sell"))
            self.entry.grid(row=4,column=1,rowspan=1,columnspan=1)
            self.sell.grid_configure(row=5,column=1,rowspan=1,columnspan=1)
            self.buy.configure(text="Cancel",command=cancel)
        def confirm(what):
            self.buy.configure(text="Buy",font=("Helvetica",25,"bold"), command=buy,height=48)
            self.sell.configure(text="Sell",font=("Helvetica",25,"bold"), command=sell,height=48)
            self.entry.grid_forget()
            self.buy.grid_configure(row=4,column=0,rowspan=2,columnspan=1)
            self.sell.grid_configure(row=4,column=1,rowspan=2,columnspan=1)
            nstock = self.entry.get()
            
            try: 
                float(nstock)
            except: 
                mb.showerror(title="Error", message="Enter a valid quantity", icon="info", type=mb.OK)
                return
            
            if float(nstock)>0:
                if what == "buy":
                    if float(nstock)*self.lddict[xcode]["Open"].iloc[0] > float(liq):
                        mb.showerror(title="Error", message="Not enough Liquidity", icon="info", type=mb.OK)
                    else:
                        sell_buy_update(self.lddict[xcode]["Open"].iloc[0], float(nstock))
                elif what == "sell":
                    if float(nstock) > float(self.tokenledger["qty"].sum()):
                        mb.showerror(title="Error", message="Not enough Shares to sell", icon="info", type=mb.OK)
                    else:
                        sell_buy_update(self.lddict[xcode]["Close"].iloc[0], -float(nstock))
            elif float(nstock)==0:
                mb.showerror(title="Good thinking!!", message="Try that in real world", icon="info", type=mb.OK)
            else:
                mb.showerror(title="Error", message="Enter a valid quantity", icon="info", type=mb.OK)
            del nstock
        def cancel():
            self.buy.configure(text="Buy",font=("Helvetica",25,"bold"), command=buy,height=48)
            self.sell.configure(text="Sell",font=("Helvetica",25,"bold"), command=sell,height=48)
            self.entry.grid_forget()
            self.buy.grid_configure(row=4,column=0,rowspan=2,columnspan=1)
            self.sell.grid_configure(row=4,column=1,rowspan=2,columnspan=1)

            
        def sell_buy_update(price,units):
            global liq, tasv, tval
            xledger.txn(edate,usr,xcode,price,units)
            self.tokenledger = xledger.fetch_token_data(usr,xcode)
            self.userledger = xledger.fetch_user_data(usr)
            liq -= units*price
            liq = round(liq,2)
            tasv += units*price
            tasv = round(tasv,2)
            tval = liq + tasv
            tval = round(tval,2)
            self.topbar_children_dynamic["Liquid Assets"].configure(text=liq)
            self.topbar_children_dynamic["Assets Value"].configure(text=tasv)
            self.topbar_children_dynamic["Total Value"].configure(text=tval)
            self.entry.delete(0,len(self.entry.get()))
            self.configure(text=self.tokenledger["qty"].sum())
            self.configure(text=self.tokenledger["amt"].sum())
            
            self.shares.configure(text=self.tokenledger["qty"].sum().round(2))
            self.netval.configure(text=str(round(self.lddict[xcode]["Close"].iloc[0]*self.userledger[self.userledger["token"]==xcode]["qty"].sum(),2))+"USD")
            
            self.botrightfill()
            
            
        self.leftframe = ctk.CTkScrollableFrame(self, width=tw, height=720, corner_radius=0,fg_color="#2d303e")
        self.tlable = ctk.CTkLabel(self.leftframe, text="Tradables",height=48, width=tw+2, font=("Arial", 20),bg_color="#2b2b2b").pack()
        for i in TRDX:
            self.btndict[i]= tab(self.leftframe, i, self.lddict[i]["Close"].iloc[0].round(3), self.lddict[i]["D%"].iloc[0].round(1))
        for i in self.btndict:
            self.btndict[i].tradbutton.configure(command=partial(Trade, i))
            self.btndict[i].pack(anchor="w",pady=(0,1))
        
        self.graphspace = customcandlestick(self)
        
        self.topbar = ctk.CTkFrame(self, width=vw,height=48,fg_color="#000")
        # self.usrname = ctk.CTkLabel(self.topbar, text="User: {}".format(usr), width=tw, height=24, padx=10, fg_color="#000")
        self.topbar_children_static = {"Total Value":ctk.CTkLabel(self.topbar, text="Total Value", width=vw//2, height=10, fg_color="#000"),"Liquid Assets":ctk.CTkLabel(self.topbar, text="Liquid Assets", width=vw//4, height=10, fg_color="#000"),"Assets Value":ctk.CTkLabel(self.topbar, text="Assets Value", width=vw//4, height=10,  fg_color="#000")}
        self.topbar_children_dynamic = {"Total Value": ctk.CTkLabel(self.topbar, text=tval, width=vw//2, height=36, fg_color="#000"),"Liquid Assets": ctk.CTkLabel(self.topbar, text=liq, width=vw//4, height=36, fg_color="#000"),"Assets Value":ctk.CTkLabel(self.topbar, text=tasv, width=vw//4, height=36,  fg_color="#000")}
        
        for count, i in enumerate(self.topbar_children_static):
            self.topbar_children_static[i].grid(row=0,column=count)
            self.topbar_children_dynamic[i].grid(row=1,column=count)
        # self.usrname.pack()
        
        self.currd = ctk.CTkLabel(self,text="Curently Displaying: {} thru {}".format(sdate, edate), fg_color="#000", width=rfw//2+2, height=6, anchor="w",padx=5)
        
        self.toprightframe = ctk.CTkFrame(self, width=rfw, height=360, corner_radius=0,fg_color="#2d303e")
        self.trf_name = ctk.CTkLabel(self.toprightframe, text=TRDX[xcode],width=rfw, height=24,anchor="w", bg_color="#0d1016",pady=10,padx=5)
        self.trf_code = ctk.CTkLabel(self.toprightframe, font=("Helvetica",15),text=xcode, width=rfw ,height=24,anchor="w", bg_color="#151928",pady=10, padx=5)
        self.trf_curr = ctk.CTkLabel(self.toprightframe,text="$ "+str(self.lddict[xcode]["Close"].iloc[0].round(3)), font=("Helvetica",30,"bold"),width=rfw//2 ,height=48,anchor="w", bg_color="#212533",pady=18,padx=5)
        self.trf_d = ctk.CTkLabel(self.toprightframe,text=str(self.lddict[xcode]["D"].iloc[0].round(3))+" USD",width=rfw//2 ,height=24,anchor="e", bg_color="#212533",pady=10,padx=5)
        self.trf_dperc = ctk.CTkLabel(self.toprightframe,text=str(self.lddict[xcode]["D%"].iloc[0].round(3))+"%",width=rfw//2 ,height=24,anchor="e", bg_color="#212533",pady=10,padx=5)
        self.buy = ctk.CTkButton(self.toprightframe, text="Buy",font=("Helvetica",35,"bold"), width=rfw//2,fg_color="#1f9358", height=48, command=buy)
        self.sell = ctk.CTkButton(self.toprightframe, text="Sell",font=("Helvetica",35,"bold"), width=rfw//2,fg_color="#e04d5c", height=48, command=sell)
        self.entry = ctk.CTkEntry(self.toprightframe, width=rfw//2, height=24, placeholder_text="Enter Units")
        
        if self.lddict[xcode]["D"].iloc[0] > 0:
            self.trf_dperc.configure(text_color="#1f9358")
            self.trf_d.configure(text_color="#1f9358")
        else:
            self.trf_dperc.configure(text_color="#e04d5c")
            self.trf_d.configure(text_color="#e04d5c")

        self.aag = ctk.CTkLabel(self.toprightframe, text="At A Glance {}".format(edate), fg_color="#0d1017", width=rfw, height=24)
        self.lopen = ctk.CTkLabel(self.toprightframe, text="Open", fg_color="#1d2950", width=rfw//2, height=24, padx=5)
        self.lhigh = ctk.CTkLabel(self.toprightframe, text="High", fg_color="#161929", width=rfw//2, height=24,padx=5)
        self.llow = ctk.CTkLabel(self.toprightframe, text="Low", fg_color="#1d2950", width=rfw//2, height=24,padx=5)
        self.lclose = ctk.CTkLabel(self.toprightframe, text="Close", fg_color="#161929", width=rfw//2, height=24,padx=5)
        self.lshares = ctk.CTkLabel(self.toprightframe, text="Shares",justify="center", fg_color="#1c2951", width=rfw//2, height=24)
        self.lnetval = ctk.CTkLabel(self.toprightframe, text="Net Value",justify="center", fg_color="#142e61", width=rfw//2, height=24)
        
        self.lopenv = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["Open"].iloc[0].round(3), fg_color="#000", width=rfw//2, height=24)
        self.lhighv = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["High"].iloc[0].round(3), fg_color="#000", width=rfw//2, height=24)
        self.llowv = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["Low"].iloc[0].round(3), fg_color="#000", width=rfw//2, height=24)
        self.lclosev = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["Close"].iloc[0].round(3), fg_color="#000", width=rfw//2, height=24)
    
    
        self.shares = ctk.CTkLabel(self.toprightframe, text="$Shares", fg_color="#1c2951",justify="center", width=rfw//2, height=48)
        self.netval = ctk.CTkLabel(self.toprightframe, text="$Net Value", fg_color="#142e61",justify="center", width=rfw//2, height=48)
        
        self.shares.configure(text=str(self.tokenledger["qty"].sum()))
        self.netval.configure(text=str(round(self.lddict[xcode]["Close"].iloc[0]*self.userledger[self.userledger["token"]==xcode]["qty"].sum(),2))+"USD")
        
        self.toprightframe.place(x=1240-tw,y=0)
        
        # self.prev = ctk.CTkButton(self,text="<",font=("Helvetica",30,"bold"),width=28,height=34,corner_radius=1024, command= lambda: go(date = (sdate-timedelta(days=1)).strftime('%d/%m/%Y'), ndays = str(ddays)+" Days", isforward=False))
        # self.next = ctk.CTkButton(self,text=">",font=("Helvetica",30,"bold"),width=28,height=34,corner_radius=1024, command= lambda: go(date = (sdate+timedelta(days=1)).strftime('%d/%m/%Y'), ndays = str(ddays)+" Days"))
        
        rbw = tw+20
        self.botrightframe = ctk.CTkFrame(self, width=rbw, height=300, corner_radius=0, fg_color="#151928",border_color="#fff",border_width=1)
        self.botrightscrollable = ctk.CTkScrollableFrame(self.botrightframe, width=rbw, height=360, corner_radius=0, fg_color="#151928")        
        self.botrightfill()
        self.botrightscrollable.pack()
        self.botrightframe.place(x=1280-tw-40,y=400)
        
        self.histbtn = ctk.CTkButton(self, text="Show History", font=("Helvetica", 20, "bold"), width=rfw//2, height=48, corner_radius=0, fg_color="#1c2951", command=partial(self.graphspace.show_history,self))
        self.histbtn.place(x=1240-tw*2.5,y=555)

        
        self.btndict["COMO"].tradbutton.configure(state="disabled")
        self.trf_name.grid(row=0,column=0, columnspan=2, rowspan=1)
        self.trf_code.grid(row=1,column=0, columnspan=2, rowspan=1)
        self.trf_curr.grid(row=2,column=0,columnspan=1, rowspan=2, padx=(0,1))
        self.trf_d.grid(row=2,column=1,columnspan=1, rowspan=1, pady=(0,1))
        self.trf_dperc.grid(row=3,column=1,columnspan=1, rowspan=1)
        self.buy.grid(row=4,column=0,columnspan=1, rowspan=2, pady=(5,0))
        self.sell.grid(row=4,column=1,columnspan=1, rowspan=2,pady=(5,0))
        self.aag.grid(row=6,column=0,columnspan=2, rowspan=1, pady=(10,1))
        self.lopen.grid(row=7,column=0,columnspan=1, rowspan=1, pady=(0,1))
        self.lopenv.grid(row=7,column=1,columnspan=1, rowspan=1, pady=(0,1))
        self.lhigh.grid(row=8,column=0,columnspan=1, rowspan=1, pady=(0,1))
        self.lhighv.grid(row=8,column=1,columnspan=1, rowspan=1, pady=(0,1))
        self.llow.grid(row=9,column=0,columnspan=1, rowspan=1, pady=(0,1))
        self.llowv.grid(row=9,column=1,columnspan=1, rowspan=1, pady=(0,1))
        self.lclose.grid(row=10,column=0,columnspan=1, rowspan=1, pady=(0,1))
        self.lclosev.grid(row=10,column=1,columnspan=1, rowspan=1, pady=(0,1))
        self.lshares.grid(row=11,column=0,columnspan=1, rowspan=1, pady=(5,1))
        self.lnetval.grid(row=11,column=1,columnspan=1, rowspan=1, pady=(5,1))
        self.shares.grid(row=12,column=0,columnspan=1, rowspan=2)
        self.netval.grid(row=12,column=1,columnspan=1, rowspan=2)
        
        self.graphspace.place(x=60+tw, y=48+48)
        self.currd.place(x=20+tw,y=48)
        self.leftframe.place(x=60,y=0)
        self.topbar.place(x=60+tw,y=0)
        # self.prev.place(x=1280-500,y=0)
        # self.next.place(x=1280-80-500,y=0)
        self.movedays(date=sdate)
        
    def portf(self):
        
        global sdate, edate, play
        play = False
        self.homeicon.configure(state="normal")
        self.portficon.configure(state="disabled")

        try:
            self.leftframe.destroy()
            self.botrightframe.destroy()
            self.toprightframe.destroy()
            self.graphspace.destroy()
            self.currd.destroy()
            self.topbar.destroy()
        except:
            pass
        upw = 1220//6
        lpw = 1220//8
        

        self.portfupperframe = ctk.CTkFrame(self, width=1220, height=360, corner_radius=50, fg_color="#151928",border_color="#fff",border_width=1)
        self.pfuscroll = ctk.CTkScrollableFrame(self.portfupperframe, width=1220-20, height=360, corner_radius=0, fg_color="#151928")
        self.pfuscroll.pack()
        urow1 = []
        for i in ["Code","Name","Units","Value","Profitability"]:
            if i == "Name":
                urow1.append(ctk.CTkLabel(self.pfuscroll, text=i, width=upw*2))
            else:
                urow1.append(ctk.CTkLabel(self.pfuscroll, text=i, width=upw))
                
        for c,i in enumerate(urow1):
            i.grid(row=0,column=c)
        
        del urow1
        
        self.tradabluserdata = []
        
        for code in TRDX:
            code_label = ctk.CTkLabel(self.pfuscroll, text=code,fg_color="#000022", width=upw)
            trdx_label = ctk.CTkLabel(self.pfuscroll, text=TRDX[code],fg_color="#000044", width=upw*2)
            qty_label = ctk.CTkLabel(self.pfuscroll, text=self.userledger[self.userledger["token"] == code]["qty"].sum(),fg_color="#000066", width=upw)
            value_label = ctk.CTkLabel(self.pfuscroll, text=round(self.userledger[self.userledger["token"] == code]["qty"].sum() * self.lddict[code]["Close"].iloc[0], 3),fg_color="#000088", width=upw)
            pl_label = ctk.CTkLabel(self.pfuscroll, text=round(self.userledger[self.userledger["token"] == code]["qty"].sum() * self.lddict[code]["Close"].iloc[0] - self.userledger[self.userledger["token"] == code]["amt"].sum(), 3),fg_color="#0000aa", width=upw)
            
            self.tradabluserdata.append((code_label, trdx_label, qty_label, value_label, pl_label))
            
        for i in range(len(self.tradabluserdata)):
            for j in range(5):
                self.tradabluserdata[i][j].grid(row=i+1,column=j)
                
        del code_label, trdx_label, qty_label, value_label, pl_label
                
        self.portflowerframe = ctk.CTkFrame(self, width=1220, height=350, corner_radius=0, fg_color="#fff")
        self.pflscroll = ctk.CTkScrollableFrame(self.portflowerframe, width=1220-30, height=360, corner_radius=0, fg_color="#151928")
        self.pflscroll.pack()
        
        urow2 = []

        for i in ["TXN id.","Date","User","Code","Units","Price","Action","Liq Change"]:
            urow2.append(ctk.CTkLabel(self.pflscroll, text=i, width=lpw,padx=2))
            
        for c,i in enumerate(urow2):
            i.grid(row=0,column=c)
            
        self.txndata = []
        
        for i in xledger.data[xledger.data["user"] == usr].index:
            txn_id_label = ctk.CTkLabel(self.pflscroll, text=i,fg_color="#000012",width=lpw)
            date_label = ctk.CTkLabel(self.pflscroll, text=xledger.data['date'].iloc[i],fg_color="#000024",width=lpw)
            user_label = ctk.CTkLabel(self.pflscroll, text=xledger.data['user'].iloc[i],fg_color="#000036",width=lpw)
            code_label = ctk.CTkLabel(self.pflscroll, text=xledger.data['token'].iloc[i],fg_color="#000048",width=lpw)
            units_label = ctk.CTkLabel(self.pflscroll, text=abs(xledger.data['qty'].iloc[i]),fg_color="#000060",width=lpw)
            price_label = ctk.CTkLabel(self.pflscroll, text=xledger.data['price'].iloc[i].round(3),fg_color="#000072",width=lpw)
            action_label = ctk.CTkLabel(self.pflscroll, text="$BuySell",fg_color="#000084", width=lpw)
            liqchange_label = ctk.CTkLabel(self.pflscroll, text= (-xledger.data["amt"].iloc[i].round(3)),fg_color="#000096",width=lpw)
            
            
            if xledger.data['qty'].iloc[i]>0:
                action_label.configure(text="Buy")
            else:
                action_label.configure(text="Sell")
                
            rown = [txn_id_label, date_label, user_label, code_label, units_label, price_label, action_label, liqchange_label]
                
            for j in rown:
                if xledger.data['qty'].iloc[i]>0:
                    j.configure(text_color="#3dc985")
                else:
                    j.configure(text_color="##ef4f60")
            
            self.txndata.append(rown)

        for i in range(len(self.txndata)):
            for j in range(8):
                self.txndata[i][j].grid(row=i+1,column=j)
        
        self.portfupperframe.place(x=60,y=0)
        self.portflowerframe.place(x=60,y=370)

        del txn_id_label, date_label, user_label, code_label, units_label, price_label, action_label, liqchange_label, rown

if __name__ == "__main__":
    app = UI()
    app.protocol("WM_DELETE_WINDOW", save)
    app.mainloop()