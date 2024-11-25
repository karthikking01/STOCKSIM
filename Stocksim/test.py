#simple customtkinter program
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

from numpy import add
from UI import images
from plot.data import *
bw = 110
curr = 69
usr = "admin"

def add_tickers(usr, ticker):
    tickername = str(yf.Ticker(ticker).info["longName"]).replace("Limited","Ltd.")
    with open("Stocksim/plot/data/tickers.csv", "a") as f:
        f.write("{},{},{}".format(usr,ticker,tickername))
    TRDX = get_tickers("admin")
    trd[ticker] = tradable(ticker,date(2000,1,3),21)
    

TRDX = get_tickers("admin")
trd = {i:tradable(i,date(2000,1,3),21) for i in TRDX.index}

def addx():
    add_btn.grid_forget()
    addentry.grid(row=0,column=0,padx=5,columnspan=2)
    addcnf.grid(row=1,column=0,padx=5)
    addcanc.grid(row=1,column=1,padx=5)

def add_cnf():
    add_btn.grid(row=0,column=0,padx=5,columnspan=2)
    tname = addentry.get()
    txr = yf.Ticker(tname)
    if tname in trd.keys():
        print("already added")
    elif txr.info["quoteType"] == "NONE":
        print("invalid name")
    elif txr.info["financialCurrency"] != "INR":
        print("not indian stock")
    else:
        add_tickers(usr,tname)
        addentry.delete(0,tk.END)
        print("SUCCESSFUL")
    
    # addentry.delete(0,tk.END)

    addentry.grid_forget()
    addcnf.grid_forget()
    addcanc.grid_forget()

def add_canc():
    add_btn.grid(row=0,column=0,padx=5,columnspan=2)
    addentry.grid_forget()
    addcnf.grid_forget()
    addcanc.grid_forget()

root =ctk.CTk()
catcher = ctk.CTkScrollableFrame(master=root, width=3*bw,height=48*5)
frame = ctk.CTkFrame(master=catcher, width=3*bw,height=48)
add_btn = ctk.CTkButton(frame, text=None,image=images["add"], width=2*bw+48, height=48, corner_radius=10, fg_color="#202020", command=addx)
addentry = ctk.CTkEntry(frame, width=2*bw+48-1, height=24, placeholder_text="Enter <STOCK>.NS or <STOCK>.BO", fg_color="#202020")
addcnf = ctk.CTkButton(frame, text="Add",width=bw, height=24, command=add_cnf)
addcanc = ctk.CTkButton(frame, text="Cancel",width=bw, height=24, command=add_canc)

add_btn.grid(row=0,column=0,padx=5,columnspan=2)
# addcnf.grid(row=1,column=0,padx=5)
# addcanc.grid(row=1,column=1,padx=5)

frame.pack()

    
catcher.pack()


def upd(root,Curr,Dperc):
    curr.configure(text=str(Curr)+" USD")
    Dperc.configure(text=str(Dperc)+"%")
    if Dperc > 0:
        Dperc.configure(text_color="#3dc985")
    else:
        Dperc.configure(text_color="#ef4f60")

root.mainloop()