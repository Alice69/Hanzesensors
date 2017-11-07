from tkinter import *
import time, random

# Center function
def getCenterGeometry(width, height):
    return (width, height, int(tk.winfo_screenwidth() / 2) - int(width / 2), int(tk.winfo_screenheight() / 2) - int(height / 2))

class PackFrame(Frame):
    def __init__(self, master, width, height):
        Frame.__init__(self, master)
        self.master.title("zonneschermCentrale")
        self.master.geometry('%dx%d+%d+%d' % getCenterGeometry(width, height))  # w,h,x,y

        self.subFrame = Frame(self.master, width=width/3, bg='#FAA')
        self.subFrame.pack(side=LEFT, fill=BOTH, expand=True)
        self.label = Label(self.subFrame, text="Zonneschermen:")
        self.label.pack(side=TOP, fill=BOTH)

        self.subFrame2 = Frame(self.master, width=width/1, bg='#AAF').pack(side=RIGHT, fill=BOTH, expand=True)

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

#4mainFrame = PackFrame(tk, 640, 480)
mainFrame = GridFrame(tk, 640, 480)

tk.mainloop()







'''canvas = Canvas(tk, width=640, height=480, bg='#000')
canvas.pack()

rect = canvas.create_rectangle(0,0,100,100, fill="#FFF")


def GUI():
    x = random.randrange(640)
    y = random.randrange(480)
    canvas.coords(rect, x, y, x + 100, y + 100)

while(1):
    GUI()
    root.update_idletasks()
    root.update()
    time.sleep(0.025)'''