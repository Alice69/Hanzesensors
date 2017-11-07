from tkinter import *
import time, random

# Center function
def getCenterGeometry(width, height):
    return (width, height, int(tk.winfo_screenwidth() / 2) - int(width / 2), int(tk.winfo_screenheight() / 2) - int(height / 2))

class GridFrame(Frame):
    def __init__(self, master, width, height):
        Frame.__init__(self, master)
        self.master.title("zonneschermCentrale")
        self.master.geometry('%dx%d+%d+%d' % getCenterGeometry(width, height))  # w,h,x,y
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=2)
        self.master.rowconfigure(0, weight=1)

        self.subFrame = Frame(self.master, bg='#FAA')
        self.subFrame.grid(column=0, row=0, sticky=NSEW)
        self.subFrame.columnconfigure(0, weight=1)
        for i in range(6):
            self.subFrame.rowconfigure(i, weight=1)
        self.label = Label(self.subFrame, text="Zonneschermen:", bg='#FAA')
        self.label.grid(column=0, row=0, sticky=NSEW)

        self.subFrame2 = Frame(self.master, bg='#AAF')
        self.subFrame2.grid(column=1, row=0, sticky=NSEW)



tk = Tk()

mainFrame = GridFrame(tk, 640, 480)

tk.mainloop()