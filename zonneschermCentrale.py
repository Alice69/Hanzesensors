from tkinter import *
from tkinter import ttk, font


class MainFrame(Frame):
    def __init__(self, master, width, height):
        Frame.__init__(self, master)
        self.master.title("zonneschermCentrale")
        self.master.geometry('%dx%d+%d+%d' % self.getCenterGeometry(width, height))  # w,h,x,y
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=3)
        self.master.rowconfigure(0, weight=1)

        self.sideMenu = SideMenu(master)
        self.dataMenu = DataMenu(master, self)

        self.frames = {}
        for F in (ZonneschermFrame, MetingenFrame, InstellingenFrame):
            self.frames[F] = F(self.dataMenu)

        self.show_frame(ZonneschermFrame)

    def getCenterGeometry(self, w, h):
        return (w, h, int(tk.winfo_screenwidth() / 2) - int(w / 2), int(tk.winfo_screenheight() / 2) - int(h / 2))

    def show_frame(self, frame):
        self.frames[frame].tkraise()


class SideMenu(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master)
        self.config(bg='#dddddd')
        self.grid(column=0, row=0, sticky=NSEW)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.rowconfigure(2, weight=1)

        self.label = Label(self, text="Zonneschermen:", fg='#666666', bg='#dddddd', font=("Helvetica", 12, "bold italic"))
        self.label.grid(columnspan=3, row=0, sticky=NSEW)

        #scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        self.scrollbar.grid(row=1, column=2, sticky=NS)
        #self.config(yscrollcommand = self.scrollbar.set)

        self.mylist = Listbox(self, width=0, bd=1, bg='#dddddd', relief='flat', yscrollcommand=self.scrollbar.set)
        self.mylist.grid(columnspan=2, row=1, sticky=NSEW)
        for line in range(40):
            self.mylist.insert(END, "Naamloos COM" + str(line))
        self.scrollbar.config(command=self.mylist.yview)

        self.comport = StringVar()
        self.inputField = Entry(self, width=0, textvariable=self.comport)
        self.inputField.grid(column=0, row=2, sticky=NSEW)
        self.button = Button(self, text="Connect", command=lambda: print(self.comport.get()))
        self.button.grid(columnspan=2, column=1, row=2, sticky=NSEW)


class DataMenu(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.config(bg='#FFF')
        self.grid(column=1, row=0, sticky=NSEW)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.rowconfigure(2, weight=1)

        # buttons op frame
        self.button = Button(self, text="Zonnescherm", command=lambda: controller.show_frame(ZonneschermFrame))
        self.button.grid(column=0, row=0, sticky=NSEW)
        self.button1 = Button(self, text="Metingen", command=lambda: controller.show_frame(MetingenFrame))
        self.button1.grid(column=1, row=0, sticky=NSEW)
        self.button2 = Button(self, text="Instellingen", command=lambda: controller.show_frame(InstellingenFrame))
        self.button2.grid(column=2, row=0, sticky=NSEW)

        self.progressBar = Label(self, bg='#5bff6c')
        self.progressBar.grid(columnspan=3, row=2, sticky=NSEW)


class DataFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.config(bg='#FFF')
        self.grid(columnspan=3, row=1, sticky=NSEW)

class ZonneschermFrame(DataFrame):
    def __init__(self, master):
        DataFrame.__init__(self, master)

        for col in range(5):
            self.columnconfigure(col, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=2)
        self.rowconfigure(4, weight=1)

        self.button = Button(self, text = "Oprollen", bg = '#5bff6c', border=1, relief='flat', font=("Helvetica", 10, "bold"))
        self.button.grid(column=1, row=2, sticky = NSEW)
        self.button1 = Button(self, text = "Uitrollen", bg = '#ff6b5b', border=1, relief='flat', font=("Helvetica", 10, "bold"))
        self.button1.grid(column=3, row=2, sticky=NSEW)

class MetingenFrame(DataFrame):
    def __init__(self, master):
        DataFrame.__init__(self, master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.label = Label(self, text="Grafiek1")
        self.label.grid(column=0, row=0, sticky=NSEW)
        self.label1 = Label(self, text="Grafiek2")
        self.label1.grid(column=1, row=0, sticky=NSEW)
        self.tabel = Label(self, text="Tabel")
        self.tabel.grid(column=0, row=1, sticky=NSEW)

class InstellingenFrame(DataFrame):
    def __init__(self, master):
        DataFrame.__init__(self, master)

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=10)
        self.columnconfigure(3, weight=5)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)

        self.label = Label(self, text="Naam:", bg = "#FFF", font=("Comic Sans MS", 13))
        self.label.grid(column=1, row=0, sticky=W)
        self.label2 = Label(self, text="Minimale oprolstand:", bg="#FFF", font=("Comic Sans MS", 13))
        self.label2.grid(column=1, row=1, sticky=W)
        self.label3 = Label(self, text="Maximale oprolstand:", bg="#FFF", font=("Comic Sans MS", 13))
        self.label3.grid(column=1, row=2, sticky=W)
        self.label4 = Label(self, text="Uitrollen bij:", bg="#FFF", font=("Comic Sans MS", 13))
        self.label4.grid(column=1, row=4, sticky=W)
        self.label5 = Label(self, text="-Een temperatuur boven de:", bg="#FFF", font=("Comic Sans MS", 11))
        self.label5.grid(column=1, row=5, sticky=W)
        self.label6 = Label(self, text="-Een lichtsterkte boven de:", bg="#FFF", font=("Comic Sans MS", 11))
        self.label6.grid(column=1, row=6, sticky=W)
        self.label7 = Label(self, text="Oprollen bij:", bg="#FFF", font=("Comic Sans MS", 13))
        self.label7.grid(column=1, row=8, sticky=W)
        self.label8 = Label(self, text="-Een temperatuur onder de:", bg="#FFF", font=("Comic Sans MS", 11))
        self.label8.grid(column=1, row=9, sticky=W)
        self.label9 = Label(self, text="-Een lichtsterkte onder de:", bg="#FFF", font=("Comic Sans MS", 11))
        self.label9.grid(column=1, row=10, sticky=W)
        #self.label10 = Label(self, text="ºC", bg="#FFF")
        #self.label10.grid(columnspan=2, row=5, sticky=E)

        self.entry1 =  Entry(self, highlightthickness=2, highlightbackground="black", width=50, font=8)
        self.entry1.grid(column=2, row=0, sticky=W)

        self.scale1 = Scale(self, orient=HORIZONTAL,troughcolor="black",bg = "#FFF", highlightbackground="#FFF",length=300,relief=FLAT,sliderrelief=FLAT, width=8, font=8)
        self.scale1.grid(column=2, row=1,sticky=W)
        self.scale2 = Scale(self, orient=HORIZONTAL,troughcolor="black",bg = "#FFF", highlightbackground="#FFF",length=300,relief=FLAT,sliderrelief=FLAT, width=8, font=8)
        self.scale2.grid(column=2, row=2,sticky=W)

        self.spinbox1 = Spinbox(self, from_= 0, to=100, justify=CENTER,width=5, font=8)
        self.spinbox1.grid(column=2, row=5,sticky=W)
        self.spinbox1 = Spinbox(self, from_= 0, to=100, justify=CENTER, width=5,font=8)
        self.spinbox1.grid(column=2, row=6,sticky=W)
        self.spinbox1 = Spinbox(self, from_= 0, to=100, justify=CENTER, width=5,font=8)
        self.spinbox1.grid(column=2, row=9,sticky=W)
        self.spinbox1 = Spinbox(self, from_= 0, to=100, justify=CENTER, width=5,font=8)
        self.spinbox1.grid(column=2, row=10,sticky=W)

        self.button_opslaan = Button(self,text="Opslaan",font=8)
        self.button_opslaan.grid(columnspan=3,row=11)
tk = Tk()
mainFrame = MainFrame(tk, 1024, 600)
tk.mainloop()