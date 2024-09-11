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
import curses
from curses import wrapper

top = str("╔")+str("═"*118)+str("╗")
mid = str("║")+str(" "*118)+str("║")
bot = str("╚")+str("═"*118)+str("╝")



def homescreen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0,top)
    for i in range(1, 28):
        stdscr.addstr(i, 0, mid)
    stdscr.addstr(28, 0, bot)
    # dim = list(os.get_terminal_size())
    # lenx=dim[0]-2
    # leny=dim[1]-2
    stdscr.getch()

if __name__=="__main__":
    wrapper(homescreen)