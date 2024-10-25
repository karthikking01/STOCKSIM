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
#120x30
from plot.data import TRD
from blessed import Terminal
import os
term = Terminal()
h,w = term.height,term.width
bw = w-2 #empty width
fbw = (w//8)-1 #full tab width
hbw = (w//16)-2 #half tab width
mbw = (w//8)-12 #middle tab width

def tabletplot(startl, code, price, change):
    with term.location(0,startl), term.cbreak():
        tabtop = ("╠"+"═"*fbw+"╣")
        tabl1 = ("║"+" "*hbw+code+" "*hbw)
        tabe   = ("║"+" "*fbw+"║")
        tabl2 = ("║"+price+" "*mbw+change)
        tablbot = ("╠"+"═"*fbw+"╣")
        print(tabtop)
        print(tabl1)
        print(tabe)
        print(tabl2)
        print(tabe)
        print(tablbot)
def homescreen():
    global ftop, fst, fbot
    ftop = ("╔"+"═"*(bw)+"╗")
    fst= "║"
    fbot = ("╚"+"═"*(bw)+"╝")
    with term.location(0,0), term.cbreak():
        print(ftop)
    for i in range(1,h-2):
        with term.location(0,i), term.cbreak():
            print(fst)
        with term.location(w,i), term.cbreak():
            print(fst)
    with term.location(0,h-2), term.cbreak():
        print(fbot)
        
    with term.location(0,1), term.cbreak():
       print("║"+" "*hbw+"v0.0"+" "*hbw)
        
    with term.location(w//8, 0), term.cbreak():
        print(str("╦"))
        for i in range(h-3):
            with term.location(w//8, i+1):
                print(str("║"))
        with term.location(w//8, h-2):
            print(str("╩"))
    with term.location(w//8*2, 0), term.cbreak():
        print(TRD)
def endwin():            
    print(term.clear + term.home)
    os.system("cls")
    
k=3
tabletplot(k, "ADBE", "100.00", "+0.01")
tabletplot(k+5*1, "ADBE", "100.00", "+0.01")
tabletplot(k+5*2, "ADBE", "100.00", "+0.01")
tabletplot(k+5*3, "ADBE", "100.00", "+0.01")
tabletplot(k+5*4, "ADBE", "100.00", "+0.01")
tabletplot(k+5*5, "ADBE", "100.00", "+0.01")
tabletplot(k+5*6, "ADBE", "100.00", "+0.01")
tabletplot(k+5*7, "ADBE", "100.00", "+0.01")

homescreen()
term.getch()
endwin()