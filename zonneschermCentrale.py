from tkinter import *
from tkinter import ttk

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


        #maken van het canvas, gekozen voor canvas anders kun je niet scrollen

        self.canvas = Canvas(self.master, bg='#c9cacc')
        self.canvas.grid(column=0, row=0, sticky=NSEW)
        self.canvas.columnconfigure(0, weight=1)

        #scrollbar

        self.scrollbar = ttk.Scrollbar(self.canvas, orient=VERTICAL, command = self.canvas.yview)
        self.scrollbar.grid(rowspan=6, column=1, sticky=NS)
        self.canvas.config(yscrollcommand = self.scrollbar.set)


        #canvas wordt in 6 rijen verdeeld

        for i in range(6):
            self.canvas.rowconfigure(i, weight=1)
        self.label = Label(self.canvas, text="Zonneschermen:", bg='#c9cacc')
        self.label.grid(column=0, row=0, sticky=NSEW)

        #frame naast canvas, opgedeeld in drie kolommen en 3 rijen waarvan
        #de ene rij 20/22 deel inneemt.

        self.subFrame = Frame(self.master, bg='#FFF')
        self.subFrame.grid(column=1, row=0, sticky=NSEW)
        self.subFrame.columnconfigure(0, weight=1)
        self.subFrame.columnconfigure(1, weight=1)
        self.subFrame.columnconfigure(2, weight=1)
        self.subFrame.rowconfigure(0, weight=1)
        self.subFrame.rowconfigure(1, weight=20)
        self.subFrame.rowconfigure(2, weight=1)

        #buttons op frame

        self.button = Button(self.subFrame,text = "Zonnescherm")
        self.button.grid(column=0, row=0, sticky=NSEW)
        self.button = Button(self.subFrame, text="Metingen")
        self.button.grid(column=1, row=0, sticky=NSEW)
        self.button = Button(self.subFrame, text="Instellingen")
        self.button.grid(column=2, row=0, sticky=NSEW)

        #canvas op frame

        self.cframe = Canvas(self.subFrame, bg='#FFF')
        self.cframe.grid(columnspan=3, row=1, sticky=NSEW)
        self.cframe.columnconfigure(0,weight=1)
        self.cframe.columnconfigure(1, weight=1)
        self.cframe.columnconfigure(2, weight=1)
        self.cframe.columnconfigure(3, weight=1)
        self.cframe.columnconfigure(4, weight=1)
        self.cframe.rowconfigure(0, weight=1)
        self.cframe.rowconfigure(1, weight=2)
        self.cframe.rowconfigure(2, weight=1)
        self.cframe.rowconfigure(3, weight=2)
        self.cframe.rowconfigure(4, weight=1)

        #buttons op cframe = canvas

        self.cbutton = Button(self.cframe, text = "Oprollen", bg = '#32e82c')
        self.cbutton.grid(column=1, row=2, sticky = NSEW)
        self.cbutton = Button(self.cframe, text="Uitrollen", bg = '#ff1500')
        self.cbutton.grid(column=3, row=2, sticky=NSEW)




tk = Tk()
mainFrame = GridFrame(tk, 640, 480)

tk.mainloop()