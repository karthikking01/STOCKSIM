from bin.plot.data import *                                     # importing data-related classes and functions
import mplfinance as mpf                                        # importing mplfinance for candlestick plot
from functools import partial                                   # importing partial for assigning functions to button
import customtkinter as ctk                                     # importing customtkinter for GUI widgets
from PIL import Image                                           # importing PIL for image processing
import tkinter.messagebox as mb                                 # importing messagebox for displaying messages and error
import matplotlib.pyplot as plt                                 # importing matplotlib for plotting 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # importing FigureCanvasTkAgg for embedding matplotlib plots in tkinter
from datetime import datetime, timedelta                        # importing datetime for date and time related calculations, conversions and comparisions
import sys                                                      # importing sys for exiting the program

#loading list of trading days excluding holidays as list of dates
datelist = pd.read_csv("bin/plot/data/datelist.csv", header=None, parse_dates=[0])
datelist[0] = pd.to_datetime(datelist[0], format="%d/%m/%y").dt.date
datelist = datelist[0].tolist()

#loading all previous transactions
xledger = ledger("bin/plot/data/ledger.csv")

#declaring global variables for later use
TRDX = None                                         
xcode = None
ddays = 21
sdate = datetime(2000,1,3).date()
edate = None
itertime = 5000
bw = 110
tw = (bw*2)+48
vw = 1180-2*tw
rfw = tw+40
usr = None
pwd = None
liq = None
play = True
tasv = 0
tval = None
loopid = None
images = {"home":ctk.CTkImage(light_image=Image.open("bin/plot/data/images/home.png"),dark_image=Image.open("bin/plot/data/images/home.png"),size=(25,25)), "pf":ctk.CTkImage(dark_image=Image.open("bin/plot/data/images/pf.png"),size=(25,25)),"add":ctk.CTkImage(dark_image=Image.open("bin/plot/data/images/add.png"),size=(25,25))}


#defining an exit function
def save():
    if usr is not None:
        xledger.save_to_csv()
        with open("bin/plot/data/userdata.csv","a") as file:
            file.write("{},{},{},{},{},{},{}\n".format(usr,pwd,sdate,edate,ddays,itertime,liq))
        sys.exit()

#creating a class for candlestick chart which supports on-demand update
class customcandlestick(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        global xcode, ddays, edate, sdate, bw, tw
        self.ndays = ddays
        self.trd = tradable(xcode,sdate,ddays)
        self.configure(width=1280, height=720)
        
        sdate = self.trd.index[0].date()
        edate = self.trd.index[-1].date()
        self.fig, self.ax = mpf.plot(self.trd,title=TRDX.loc[xcode,"name"], type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=0.8, panel_ratios=(3,1),tight_layout=False)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,column=0)
    

    def upd(self, ndate=sdate, ndays=ddays):
        global xcode, ddays, edate, sdate, bw, tw
        plt.close()
        del self.fig, self.ax, self.canvas, self.trd
        self.code = xcode
        self.trd = tradable(self.code,ndate,ndays,False)
        sdate = self.trd.index[0].date()
        edate = self.trd.index[-1].date()
        self.fig, self.ax = mpf.plot(self.trd, title=TRDX.loc[xcode,"name"], type="candle",datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=0.8, panel_ratios=(3,1),tight_layout=False)
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
        _fig, ax = mpf.plot(data, type="line",title=TRDX.loc[xcode,"name"],datetime_format='%d/%m/%y',style=binance_dark,volume=True, ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False,figscale=2, panel_ratios=(3,1),tight_layout=False)
        
        canvas = FigureCanvasTkAgg(_fig, master=UI.histwin)

        canvas.draw()
        canvas.get_tk_widget().pack()
        
        UI.histwin.protocol("WM_DELETE_WINDOW", on_exit)
    
#creating a tab class for selecting which stock to choose which supports on-demand update
class tab(ctk.CTkFrame):
    def __init__(self, parent, Code, Curr, Dperc):
        global xcode, ddays, edate, sdate, bw, tw
        super().__init__(parent)
        labelc="#000"
        self.Tcode = Code
        self.text = TRDX.loc[Code,"name"]
        
        if len(self.text) > 15:
            self.text = self.text[:15]+".."
        
        self.code = ctk.CTkLabel(self, text=Code,font=("Arial", 12, "bold"),padx=5,width=bw, height=24,anchor="w",bg_color=labelc)
        self.name = ctk.CTkLabel(self, text=self.text,width=bw,font=('Helevtica',10, "italic"),text_color="grey",padx=5, height=24,anchor="w",bg_color=labelc)
        self.curr = ctk.CTkLabel(self, text=str(Curr)+" INR",width=bw, height=24,anchor="e",bg_color=labelc)
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
        self.curr.configure(text=str(Curr)+" INR")
        self.Dperc.configure(text=str(Dperc)+"%")
        if Dperc > 0:
            self.Dperc.configure(text_color="#3dc985")
        else:
            self.Dperc.configure(text_color="#ef4f60")


#GUI
class UI(ctk.CTk):
    def __init__(self):
        global xcode, ddays, edate, sdate, bw, tw, tasv
    
        super().__init__()                                  #self refers to the GUI window
        self.title("StockSim")                              #set title to StockSim
        self.configure(fg_color="#0b1015")                  #set background color to #0b1015       
        x = (self.winfo_screenwidth()-1280)//2              #calculate midpoint of screen width
        y = (self.winfo_screenheight()-720)//2              #calculate midpoint of screen height
        self.resizable(False, False)                        #disable window resize
        self.geometry('%dx%d+%d+%d' % (1280, 730, x, y))    #set window size and position
        self.wm_attributes("-alpha","0.9")                  #set window transparency
        
        self.login()                                        #show login screen
        self.iconframe = ctk.CTkFrame(self,fg_color="#151928", width=60, height=720, corner_radius=0)                       #create frame(holder) for icons
        self.homeicon = ctk.CTkButton(self.iconframe, text=None,image=images["home"],height=60,width=60,command=self.home)  #create home button inside frame
        self.portficon = ctk.CTkButton(self.iconframe,text=None,image=images["pf"],height=60,width=60,command=self.portf)   #create porfolio button inside frame
        

#defining a function that updates the transaction history for a specific ticker
    def botrightfill(self):
        rbw = tw+20                                                 #calculate width for each cell
        for widget in self.botrightscrollable.winfo_children():     #clear previous table incase of updation
            widget.destroy()

        none = ctk.CTkLabel(self.botrightscrollable, text="Initiate a trade", fg_color="#151928", width=rbw, height=15)     #label for if no trade has taken place yet
        
        row1 = []
        for i in ["Date","Code","Price","Units","Amt","Action"]:                                                            #create column labels
            row1.append(ctk.CTkLabel(self.botrightscrollable, text=i, fg_color="#151928", width=rbw//6, height=15))
        for i in row1:                                                                                                      #display column labels
            i.grid(row=0,column=row1.index(i))                                                                              
            
        tokenledgerlist = {}
        
        #load transaction history of current token line by line
        
        for i in list(self.tokenledger.index):
            date_label = ctk.CTkLabel(self.botrightscrollable, text=self.tokenledger.loc[i, 'date'], font=("font77", 10), width=rbw//6, padx=5,fg_color="#000022")
            token_label = ctk.CTkLabel(self.botrightscrollable, text=self.tokenledger.loc[i, 'token'], font=("font77", 7), width=rbw//6,fg_color="#000033")
            price_label = ctk.CTkLabel(self.botrightscrollable, text=self.tokenledger.loc[i, 'price'].round(2), font=("font77", 10), width=rbw//6,fg_color="#000044")
            qty_label = ctk.CTkLabel(self.botrightscrollable, text=abs(self.tokenledger.loc[i, 'qty'].round(2)), font=("font77", 10), width=rbw//6,fg_color="#000055")
            amt_label = ctk.CTkLabel(self.botrightscrollable, text=self.tokenledger.loc[i, 'amt'].round(2), font=("font77", 10), width=rbw//6,fg_color="#000066")
            buy_sell_label = ctk.CTkLabel(self.botrightscrollable,text="₹buysell", font=("font77", 11), width=rbw//6,fg_color="#000077")
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
        
        #if no trade has taken place, then show text "Initiate a trade"
        if self.tokenledger.empty:
            none.grid(row=1,column=0,rowspan=3,columnspan=6)
            return
        #insert values into the table in descending order of transaction date
        else:
            revkeys = sorted(list(tokenledgerlist.keys()),reverse=True)
            none.grid_forget()
            for c,i in enumerate(revkeys):
                for j in range(6):
                    tokenledgerlist[i][j].grid(row=c+1,column=j)
#defining a function to update the top right frame with the current token's data when user changes what token they are trading
    def toprightfill(self):
        self.trf_name.configure(text=TRDX.loc[xcode,"name"])                                  #update name being shown
        self.trf_code.configure(text=xcode)                                                   #update code being shown
        self.trf_curr.configure(text="₹ "+str(self.lddict[xcode]["Close"].iloc[0].round(3)))  #update current price being shown rounded off to nearest 3 decimal places
        self.trf_d.configure(text=str(self.lddict[xcode]["D"].iloc[0].round(3))+" INR")       #update change in price being shown rounded off to nearest 3 decimal places
        self.trf_dperc.configure(text=str(self.lddict[xcode]["D%"].iloc[0].round(3))+"%")     #update change in price percentage being shown rounded off to nearest 3 decimal places
        self.shares.configure(text=self.tokenledger["qty"].sum().round(2))                    #update number of shares owned by the user
        self.netval.configure(text=str(round(self.lddict[xcode]["Close"].iloc[0]*self.userledger[self.userledger["token"]==xcode]["qty"].sum(),2))+"INR")    #update net value of the shares owned by the user
        self.lopenv.configure(text=self.lddict[xcode]["Open"].iloc[0].round(3))                                                                              #update open value being shown rounded off to nearest 3 decimal places
        self.lhighv.configure(text=self.lddict[xcode]["High"].iloc[0].round(3))                                                                              #update high value being shown rounded off to nearest 3 decimal places                                                     
        self.llowv.configure(text=self.lddict[xcode]["Low"].iloc[0].round(3))                                                                                #update low value being shown rounded off to nearest 3 decimal places
        self.lclosev.configure(text=self.lddict[xcode]["Close"].iloc[0].round(3))                                                                            #update close value being shown rounded off to nearest 3 decimal places

        if self.lddict[xcode]["D"].iloc[0] > 0:             #change color of text according to profit or loss
            self.trf_dperc.configure(text_color="#1f9358")
            self.trf_d.configure(text_color="#1f9358")
        else:
            self.trf_dperc.configure(text_color="#e04d5c")
            self.trf_d.configure(text_color="#e04d5c")

    def movedays(self,date:datetime.date, ndays=21):        #function to move the data to certain date and/or change the number of days displayed
        
        
        global xcode, ddays, edate, sdate, bw, tw,play, loopid

        if date > datelist[-1] or date < datelist[0]-timedelta(5):    #if date is out of range, show error message
            
            mb.showerror(title="Date out of range", message="Date Must be Greater than 2010-01-01 and Less than Today")
            return

        if play: #check if in hometab
            ddays = ndays   #set new number of days
            sdate = date    #set new sdate
            
            self.graphspace.upd(ndate=sdate, ndays=ddays)   #update graph
            self.lddict = {i:tradable(i,sdate,ddays,True) for i in TRDX.index} #update ticker data
            
            tasv=0
            for i in self.lddict:
                tasv += self.lddict[i]["Close"].iloc[0]*self.userledger[self.userledger["token"]==i]["qty"].sum() #recalculate total assets value
            tasv = round(tasv,2)
            tval = tasv + liq
            tval = round(tval,2)
            
            self.topbar_children_dynamic["Liquid Assets"].configure(text=liq)   #update topbar
            self.topbar_children_dynamic["Assets Value"].configure(text=tasv)
            self.topbar_children_dynamic["Total Value"].configure(text=tval)
            
            for i in self.btndict:
                self.btndict[i].upd(self.lddict[i]["Close"].iloc[0].round(1), self.lddict[i]["D%"].iloc[0].round(1)) #update tabs
            self.toprightfill()                                                                                      #update stock data
            self.currd.configure(text="Curently Displaying: {} thru {}".format(sdate, edate))

            try:
                self.after_cancel(loopid)                                                                            
            except:
                pass

            loopid = self.after(itertime,partial(self.movedays,datelist[(datelist.index(sdate))+1],ndays))        #This is to keep updating the interface by 1 day after set time(default 5s)
    
    
    def login(self):
        global xcode, ddays, edate, sdate, bw, tw, usr, pwd, liq

        self.login_form = ctk.CTkFrame(self, width=300)                                                           #frame containing login interface
        self.usren = ctk.CTkEntry(self.login_form, width=150, height=32, placeholder_text="Username")             #entry widget to get username
        self.pwden = ctk.CTkEntry(self.login_form, width=150, height=32, placeholder_text="Password", show="*")   #entry widget to get password 
        self.title1 = ctk.CTkLabel(self.login_form, text="Welcome To",text_color="#4c4c4c", font=("Roboto", 10))  #label widget to display welcome message
        self.title2 = ctk.CTkLabel(self.login_form, text="STOCKSIM", font=("Roboto", 30))                         #label widget to display STOCKSIM                      
        self.title3 = ctk.CTkLabel(self.login_form, text="Login to continue", font=("Roboto", 15))                #label widget to display login message
        self.loginbtn = ctk.CTkButton(self.login_form, text="Login", width=100, height=32)                        #button widget to login

        self.title1.grid(row=0,column=0)                                                                          #placing all elements
        self.title2.grid(row=1,column=0, padx=10,pady=(0,20))
        self.title3.grid(row=2,column=0)
        self.usren.grid(row=3,column=0)
        self.pwden.grid(row=4,column=0)
        self.loginbtn.grid(row=5,column=0)
        
        
        #login function
        def loginx(event): # Event argument is required for "bind: fucntionality (pressing enter to submit form) 
            global xcode, ddays, edate, sdate, bw, tw, usr, pwd, liq, tasv, tval, itertime, TRDX
            usr = self.usren.get()          #get user entry
            pwd = self.pwden.get()
            
            config = get_config(usr,pwd)    #get user information from database
            
            match config[0]: # fancy if-elif
                case 200:   #if user is in database
                    TRDX = get_tickers(usr)                         #load the tickers user had previously traded thru this app
                    sdate = config[1].date()                        #get last start date on graph
                    edate = config[2].date()                        #get last end date on graph
                    ddays = config[3]                               #get number of days being displayed in previous session
                    xcode = get_tickers(usr).index.tolist()[-1]     #get last ticker displayed in previous session
                    itertime = config[4]                           
                    liq = round(config[5],2)                        #get total credits before leaving previous session
                    self.home()
                    
                    self.iconframe.place(x=0,y=0)                   #begin loading homescreen
                    self.homeicon.place(x=0,y=0)
                    self.portficon.place(x=0,y=60)
                case 401:
                    mb.showerror(title="Error", message="Check your password".format(usr), icon="info", type=mb.OK)                                     #if password is wrong but user exists show error
                case 400:
                    msg = mb.showerror(title="Error", message="No user named {}, Do you want to create one?".format(usr), icon="info", type=mb.YESNO)   #if user doesn't exist ask to create one
                    
                    if msg == "yes" and len(pwd)>5:                                                                                                     #if user wants to create a session and password is longer than 5 characters
                        with open("bin/plot/data/userdata.csv","a") as file:                                                                            #add user to database
                            file.write("{},{},{},{},{},{},{}\n".format(usr,pwd,"2010-01-04",None,21,5000,10000))
                        with open("bin/plot/data/tickers.csv","a") as file:
                            file.write("{},{},{}".format(usr,"SBIN.NS","State Bank of India"))
                        self.login()                                                                                                                    #revert back to login screen
                    else:
                        mb.showerror(title="Error", message="Create a stronger password!".format(usr), icon="info", type=mb.OK)                         #if weak password show error
                        
                        
                    
        self.pwden.bind("<Return>", command=loginx)                 #set enter key to submit login form
        self.loginbtn.configure(command=partial(loginx,None))       #set login button to submit login form
        self.login_form.place(relx=0.5,rely=0.5,anchor="center")    #place login form in center of screen
        
#homescreen
    def home(self):
        global xcode, ddays, edate, sdate, bw, tw, tasv, play
        try:                                                    #try clearing screen
            for i in self.login_form.winfo_children():          
                i.destroy()
            self.login_form.destroy()
        except:
            pass
        
        try:
            self.portfupperframe.destroy()
            self.portflowerframe.destroy()
        except:
            pass
        
        self.homeicon.configure(state="disabled")
        self.portficon.configure(state="normal")
        play = True
        i = None
        self.btndict = {}
        self.txnlist = []
        self.lddict = {i:tradable(i,sdate,ddays,True) for i in TRDX.index}      #load all tradable tokens
        self.tokenledger = xledger.fetch_token_data(usr,xcode)                  #load data of token currently on screen
        self.userledger = xledger.fetch_user_data(usr)                          #load user transaction data
        
        tasv=0                                                                  #load user's total asset value
        for i in self.lddict:
            tasv += self.lddict[i]["Close"].iloc[0]*self.userledger[self.userledger["token"]==i]["qty"].sum()
        tasv = round(tasv,2)
        tval = round(tasv + liq,2)   
                 
        def Trade(Tcode):
            global xcode, ddays, edate, sdate, bw, tw
            del xcode
            xcode = Tcode
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
        def addx():
            self.add_btn.grid_forget()
            self.addentry.grid(row=0,column=0,padx=5,columnspan=2)
            self.addcnf.grid(row=1,column=0,padx=5)
            self.addcanc.grid(row=1,column=1,padx=5)

        def add_cnf():
            global TRDX
            self.add_btn.grid(row=0,column=0,padx=5,columnspan=2)
            tname = self.addentry.get()
            txr = yf.Ticker(tname)

            if tname in TRDX.keys():
                mb.showinfo(title="Already added", message="Ticker is already added")
            elif txr.info["quoteType"] == "NONE":
                mb.showerror(title="Invalid Trade Symbol", message="Please check the symbol or refer to https://finance.yahoo.com/lookup/ for valid BSE/NSE symbols")
            elif txr.info["financialCurrency"] != "INR":
                mb.showerror(title="Invalid Currency", message="Please check the symbol or refer to https://finance.yahoo.com/lookup/ for valid BSE/NSE symbols trading in INR")
            else:
                add_tickers(usr,sdate,ddays,tname)
                self.addentry.delete(0,200)
                TRDX = get_tickers(usr)
                self.lddict[tname] = tradable(tname,sdate,ddays,True)
                self.btndict[tname]= tab(self.leftscroller, tname, self.lddict[tname]["Close"].iloc[0].round(3), self.lddict[tname]["D%"].iloc[0].round(1))
                self.btndict[tname].tradbutton.configure(command=partial(Trade, tname))
                self.btndict[tname].pack(anchor="w",pady=(0,1))

            self.addentry.grid_forget()
            self.addcnf.grid_forget()
            self.addcanc.grid_forget()

        def add_canc():
            self.add_btn.grid(row=0,column=0,padx=5,columnspan=2)
            self.addentry.grid_forget()
            self.addcnf.grid_forget()
            self.addcanc.grid_forget()

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
                    elif not(self.userledger[self.userledger["token"]==xcode].empty) and sdate < self.userledger[self.userledger["token"]==xcode]["date"].iloc[0]:
                        mb.showerror(title="Error", message="You can't sell before buying", icon="info", type=mb.OK)
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
            self.netval.configure(text=str(round(self.lddict[xcode]["Close"].iloc[0]*self.userledger[self.userledger["token"]==xcode]["qty"].sum(),2))+"INR")
            
            self.botrightfill()
            
        self.leftframe = ctk.CTkFrame(self, width=tw, height=720, corner_radius=0,fg_color="#2d303e")
        self.leftscroller = ctk.CTkScrollableFrame(self.leftframe, width=tw, height=720, corner_radius=0,fg_color="#2d303e")
        self.leftscroller.pack()
        self.tlable = ctk.CTkLabel(self.leftscroller, text="Tradables",height=48, width=tw+2, font=("Arial", 20),bg_color="#2b2b2b").pack()
        

        self.add_frame = ctk.CTkFrame(master=self.leftscroller, width=3*bw,height=48)
        self.add_btn = ctk.CTkButton(self.add_frame, text=None,image=images["add"], width=2*bw+48, height=48, corner_radius=10, fg_color="#242424", command=addx)
        self.addentry = ctk.CTkEntry(self.add_frame, width=2*bw+48-1, height=24, placeholder_text="Enter <STOCK>.NS or <STOCK>.BO", fg_color="#202020")
        self.addcnf = ctk.CTkButton(self.add_frame, text="Add",width=bw, height=24, command=add_cnf)
        self.addcanc = ctk.CTkButton(self.add_frame, text="Cancel",width=bw, height=24, command=add_canc)
        self.add_btn.grid(row=0,column=0,padx=5,columnspan=2)
        self.add_frame.pack()
        
        for i in TRDX.index:
            self.btndict[i]= tab(self.leftscroller, i, self.lddict[i]["Close"].iloc[0].round(3), self.lddict[i]["D%"].iloc[0].round(1))
        for i in self.btndict:
            self.btndict[i].tradbutton.configure(command=partial(Trade, i))
            self.btndict[i].pack(anchor="w",pady=(0,1))
        
        self.graphspace = customcandlestick(self)
        
        self.topbar = ctk.CTkFrame(self, width=vw,height=48,fg_color="#000")
        self.topbar_children_static = {"Total Value":ctk.CTkLabel(self.topbar, text="Total Value", width=vw//2, height=10, fg_color="#000"),"Liquid Assets":ctk.CTkLabel(self.topbar, text="Liquid Assets", width=vw//4, height=10, fg_color="#000"),"Assets Value":ctk.CTkLabel(self.topbar, text="Assets Value", width=vw//4, height=10,  fg_color="#000")}
        self.topbar_children_dynamic = {"Total Value": ctk.CTkLabel(self.topbar, text=tval, width=vw//2, height=36, fg_color="#000"),"Liquid Assets": ctk.CTkLabel(self.topbar, text=liq, width=vw//4, height=36, fg_color="#000"),"Assets Value":ctk.CTkLabel(self.topbar, text=tasv, width=vw//4, height=36,  fg_color="#000")}
        
        for count, i in enumerate(self.topbar_children_static):
            self.topbar_children_static[i].grid(row=0,column=count)
            self.topbar_children_dynamic[i].grid(row=1,column=count)
            
        self.currd = ctk.CTkLabel(self,text="Curently Displaying: {} thru {}".format(sdate, edate), fg_color="#000", width=rfw//2+2, height=6, anchor="w",padx=5)
        
        self.toprightframe = ctk.CTkFrame(self, width=rfw, height=360, corner_radius=0,fg_color="#2d303e")
        self.trf_name = ctk.CTkLabel(self.toprightframe, text=TRDX.loc[xcode,"name"],width=rfw, height=24,anchor="w", bg_color="#0d1016",pady=10,padx=5)
        self.trf_code = ctk.CTkLabel(self.toprightframe, font=("Helvetica",15),text=xcode, width=rfw ,height=24,anchor="w", bg_color="#151928",pady=10, padx=5)
        self.trf_curr = ctk.CTkLabel(self.toprightframe,text="₹ "+str(self.lddict[xcode]["Close"].iloc[0].round(3)), font=("Helvetica",30,"bold"),width=rfw//2 ,height=48,anchor="w", bg_color="#212533",pady=18,padx=5)
        self.trf_d = ctk.CTkLabel(self.toprightframe,text=str(self.lddict[xcode]["D"].iloc[0].round(3))+" INR",width=rfw//2 ,height=24,anchor="e", bg_color="#212533",pady=10,padx=5)
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
        self.lnetval = ctk.CTkLabel(self.toprightframe, text="Net Value",justify="center", fg_color="#1c2951", width=rfw//2, height=24)
        
        self.lopenv = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["Open"].iloc[0].round(3), fg_color="#000", width=rfw//2, height=24)
        self.lhighv = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["High"].iloc[0].round(3), fg_color="#000", width=rfw//2, height=24)
        self.llowv = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["Low"].iloc[0].round(3), fg_color="#000", width=rfw//2, height=24)
        self.lclosev = ctk.CTkLabel(self.toprightframe, text=self.lddict[xcode]["Close"].iloc[0].round(3), fg_color="#000", width=rfw//2, height=24)
    
    
        self.shares = ctk.CTkLabel(self.toprightframe, text="₹Shares", fg_color="#1c2971",justify="center", width=rfw//2, height=48)
        self.netval = ctk.CTkLabel(self.toprightframe, text="₹Net Value", fg_color="#1c2971",justify="center", width=rfw//2, height=48)
        
        self.shares.configure(text=str(self.tokenledger["qty"].sum()))
        self.netval.configure(text=str(round(self.lddict[xcode]["Close"].iloc[0]*self.userledger[self.userledger["token"]==xcode]["qty"].sum(),2))+"INR")
        
        self.toprightframe.place(x=1240-tw,y=0)
        
        rbw = tw+20
        self.botrightframe = ctk.CTkFrame(self, width=rbw, height=300, corner_radius=0, fg_color="#151928",border_color="#fff",border_width=1)
        self.botrightscrollable = ctk.CTkScrollableFrame(self.botrightframe, width=rbw, height=360, corner_radius=0, fg_color="#151928")        

        self.botrightfill()
        self.botrightscrollable.pack()
        self.botrightframe.place(x=1280-tw-40,y=400)

        self.timecontrolframe = ctk.CTkFrame(self, width=tw+96, height=48, corner_radius=0, fg_color="#151928",border_color="#fff")
        self.timecontrolable = ctk.CTkLabel(self.timecontrolframe, width=tw+96, height=6,text="Time Controls", fg_color="#151928", font=("Helvetica", 20, "bold"))
        self.calentry = ctk.CTkEntry(self.timecontrolframe, width=tw//2, height=6, placeholder_text="Enter Date DD/MM/YYYY")
        self.ndaysentry = ctk.CTkEntry(self.timecontrolframe, width=tw//2, height=6, placeholder_text="Enter Number of Days")
        self.ndaysentry.insert(0,str(ddays)+" Days")
        self.go = ctk.CTkButton(self.timecontrolframe,text="Go",height=48,width=48,command=lambda: self.movedays(datetime.strptime(self.calentry.get(),"%d/%m/%Y").date(), self.ndaysentry.get().split(" ")[0]))
        self.histbtn = ctk.CTkButton(self.timecontrolframe, text="Show History", width=tw//2, height=48, fg_color="#1c2951", command=partial(self.graphspace.show_history,self))

        self.timecontrolable.grid(row=0,column=0, columnspan=3, rowspan=1)
        self.calentry.grid(row=1,column=0, columnspan=1, rowspan=1)
        self.ndaysentry.grid(row=2,column=0, columnspan=1, rowspan=1)
        self.go.grid(row=1,column=1, columnspan=1, rowspan=2)
        self.histbtn.grid(row=1,column=2, columnspan=1, rowspan=3,padx=(20,0))
        self.timecontrolframe.place(x=500,y=650)


        
        self.btndict[xcode].tradbutton.configure(state="disabled")
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
        self.movedays(date=sdate)
        
    def portf(self):
        
        global sdate, edate, play
        play = False
        self.homeicon.configure(state="normal")
        self.portficon.configure(state="disabled")

        try:
            self.leftframe.destroy()
            self.timecontrolframe.destroy()
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
        
        for code in TRDX.index:
            code_label = ctk.CTkLabel(self.pfuscroll, text=code,fg_color="#000022", width=upw)
            trdx_label = ctk.CTkLabel(self.pfuscroll, text=TRDX.loc[code,"name"],fg_color="#000044", width=upw*2)
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
        
        for i in xledger.data[xledger.data["user"] == usr].index.sort_values(ascending=False):
            txn_id_label = ctk.CTkLabel(self.pflscroll, text=i,fg_color="#000012",width=lpw)
            date_label = ctk.CTkLabel(self.pflscroll, text=xledger.data['date'].iloc[i],fg_color="#000024",width=lpw)
            user_label = ctk.CTkLabel(self.pflscroll, text=xledger.data['user'].iloc[i],fg_color="#000036",width=lpw)
            code_label = ctk.CTkLabel(self.pflscroll, text=xledger.data['token'].iloc[i],fg_color="#000048",width=lpw)
            units_label = ctk.CTkLabel(self.pflscroll, text=abs(xledger.data['qty'].iloc[i]),fg_color="#000060",width=lpw)
            price_label = ctk.CTkLabel(self.pflscroll, text=xledger.data['price'].iloc[i].round(3),fg_color="#000072",width=lpw)
            action_label = ctk.CTkLabel(self.pflscroll, text="₹BuySell",fg_color="#000084", width=lpw)
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
                    j.configure(text_color="#ef4f60")
            
            self.txndata.append(rown)

        for i in xledger.data[xledger.data["user"] == usr].index.sort_values():
            for j in range(8):
                self.txndata[i][j].grid(row=i+1,column=j)
        
        self.portfupperframe.place(x=60,y=0)
        self.portflowerframe.place(x=60,y=370)

        del txn_id_label, date_label, user_label, code_label, units_label, price_label, action_label, liqchange_label, rown