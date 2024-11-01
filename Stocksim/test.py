import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf
from plot.data import tradable
from math import log10

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
        "alpha": 1,
    },
    "mavcolors": ("#ad7739", "#a63ab2", "#62b8ba"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
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

# class tab(ctk.CTkFrame):
#     def __init__(self,parent):
#         super().__init__(parent)
#         self.configure(width=300, height=100)    
# class UI(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("800x720")
#         self.title("Stocksim")
#         self.resizable(False, False)
#         self.configure(background="#1a1a1a")
#         x = tab(self)
#         x.pack()
        
#         self.mainloop()

# app = UI()

#candlestick

# asbl=tradable("ASBL","2023-08-01", 100)
# como=tradable("COMO","2023-08-01", 100)
# mpf.plot(asbl.data, type="candle", style="charles", volume=True, title="ASBL", ylabel="Price", ylabel_lower="Shares Traded", show_nontrading=True, figscale=1.5, panel_ratios=(3,1))
# class customcandlestick(ctk.CTkFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         asbl =  tradable("ASBL","2023-08-01", 50)
#         self.configure(width=1280-60-2*268, height=672-2*48, fg_color="#fcf")


#         self.fig, self.ax = mpf.plot(asbl.data, type="candle", style=binance_dark, volume=True, title="ASBL", ylabel="Price", ylabel_lower="Shares Traded",returnfig=True,show_nontrading=False, figscale=1.5, panel_ratios=(3,1))
#         self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        
#         self.canvas.draw()
#         self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        
# Tk = ctk.CTk()
# Tk.geometry("1280x720")
# Tk.title("Stocksim")
# Tk.resizable(False, False)
# Tk.configure(background="#1a1a1a")
# candlestick = customcandlestick(Tk)
# candlestick.pack()
# Tk.mainloop()