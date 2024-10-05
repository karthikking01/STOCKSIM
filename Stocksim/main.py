"""
TODO:
CLI(Text and minimal visuals) based modern looking stock market simulator
working principal
1) will fetch week wise stock price over an year or so of about 10 tradables
2) assign random code to each stock (ADBE, TSLA)
3) at every 10 second update the price according to the data (ie simulate actual holding of stock but squeeze yearlong waiting period into a few minutes)
4) allow user to simulate the buying/selling stocks
5) show percentage loss/profit at end of each week
6) show the graph of the stock price
7) have a watchlist
8) have a portfolio

www.16colo.rs
"""
#120x30
from blessed import Terminal
term = Terminal()

pricetablet = 

def homescreen():
    with term.location(0,0), term.cbreak():
        h,w = term.height,term.width
        #print(h,w,term.number_of_colors)
        top = str("╔")+str("═"*(w-2))+str("╗")
        mid = str("║")+str(" "*(w-2))+str("║")
        bot = str("╚")+str("═"*(w-2))+str("╝")
        print(top)
        print(mid*(h-3))
        print(bot)
    with term.location(w//8, 0), term.cbreak():
        print(str("╦"))
        for i in range(h-3):
            with term.location(w//8, i+1):
                print(str("║"))
        with term.location(w//8, h-2):
            print(str("╩"))
    term.getch()
    
homescreen()