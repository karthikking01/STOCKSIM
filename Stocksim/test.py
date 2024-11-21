#simple customtkinter program
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

from numpy import add
from UI import images
bw = 110

root =ctk.CTk()
catcher = ctk.CTkScrollableFrame(master=root, width=3*bw,height=48*5)
for i in range(5):
    frame = ctk.CTkFrame(master=catcher, width=3*bw,height=48)
    code = ctk.CTkLabel(frame, text="Code",font=("Arial", 12, "bold"),padx=5,width=bw, height=24,anchor="w",bg_color="#000")
    name = ctk.CTkLabel(frame, text="TRDX[Code]",width=bw,font=('Helevtica',10, "italic"),text_color="grey",padx=5, height=24,anchor="w",bg_color="#000")
    curr = ctk.CTkLabel(frame, text="str(Curr)"+" USD",width=bw, height=24,anchor="e",bg_color="#000")
    Dperc = ctk.CTkLabel(frame, text='str(Dperc)'+"%",width=bw, height=24,anchor="e",bg_color="#000")
    tradbutton = ctk.CTkButton(frame, text="View", width=48, height=48, corner_radius=10, fg_color="#202020",anchor="c")
    code.grid(row=0,column=0)
    name.grid(row=1,column=0)
    curr.grid(row=0,column=1)
    Dperc.grid(row=1,column=1)
    tradbutton.grid(row=0,column=2,rowspan=2)
    frame.pack()

    
catcher.pack()

add_btn = ctk.CTkButton(master=catcher, text=None,image=images["add"], width=3*bw, height=48, corner_radius=10, fg_color="#202020",anchor="c")
add_btn.pack()



def upd(root,Curr,Dperc):
    curr.configure(text=str(Curr)+" USD")
    Dperc.configure(text=str(Dperc)+"%")
    if Dperc > 0:
        Dperc.configure(text_color="#3dc985")
    else:
        Dperc.configure(text_color="#ef4f60")

root.mainloop()