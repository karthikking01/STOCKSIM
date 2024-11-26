from bin.UI import *

if __name__ == "__main__":
    app = UI()
    app.protocol("WM_DELETE_WINDOW", save)
    app.mainloop()