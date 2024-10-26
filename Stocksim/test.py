import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plot.data import tradable
from math import log10
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

asbl=tradable("ASBL","2023-08-01", 100)
como=tradable("COMO","2023-08-01", 100)

plt.rcParams['date.converter'] = 'concise'
plt.plot(asbl.data["D"])
plt.plot(como.data["D"])
plt.xticks(rotation=50)
plt.show()
class customcandlestick(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # asbl =  tradable("ASBL","2023-08-01", 100)
        self.configure(width=1280-60-2*268, height=672-2*48, fg_color="#fcf")

Tk = ctk.CTk()
Tk.geometry("1280x720")
Tk.title("Stocksim")
Tk.resizable(False, False)
Tk.configure(background="#1a1a1a")
candlestick = customcandlestick(Tk)
candlestick.pack()
# Tk.mainloop()