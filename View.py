from tkinter import *
from tkinter import ttk
from Controller import *

controller = Controller()

class MainFrame(Tk):
    def __init__(self, width, height):
        Tk.__init__(self)
        self.title("zonneschermCentrale")
        self.geometry('%dx%d+%d+%d' % self.getCenterGeometry(width, height))  # w,h,x,y
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        self.sideMenu = SideMenu(self)
        self.dataMenu = DataMenu(self, self)

        self.frames = {}
        for F in (ZonneschermFrame, MetingenFrame, InstellingenFrame):
            self.frames[F] = F(self.dataMenu)

        self.show_frame(ZonneschermFrame)

    def getCenterGeometry(self, w, h):
        return (w, h, int(self.winfo_screenwidth() / 2) - int(w / 2), int(self.winfo_screenheight() / 2) - int(h / 2))

    def show_frame(self, frame):
        self.frames[frame].tkraise()

    def start_mainloop(self):
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.mainloop()

    def exit(self):
        controller.stop()
        self.destroy()


class SideMenu(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master)
        self.config(bg='#dddddd')
        self.grid(column=0, row=0, sticky=NSEW)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=16)
        self.rowconfigure(2, weight=1)

        self.label = Label(self, text="Zonneschermen:", fg='#666666', bg='#dddddd', font=("Helvetica", 12, "bold italic"))
        self.label.grid(columnspan=3, row=0, sticky=NSEW)

        #scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        self.scrollbar.grid(row=1, column=2, sticky=NS)
        #self.config(yscrollcommand = self.scrollbar.set)

        #self.mylist = Listbox(self, width=0, bd=1, bg='#dddddd', relief='flat', yscrollcommand=self.scrollbar.set)
        self.mylist = Canvas(self, width=200, bg='#dddddd', yscrollcommand=self.scrollbar.set)
        self.mylist.grid(columnspan=2, row=1, sticky=NSEW)
        '''for line in range(40):
            self.mylist.insert(END, "Naamloos COM" + str(line))'''
        self.scrollbar.config(command=self.mylist.yview)

        comInput = StringVar()
        self.inputField = Entry(self, bd=0, textvariable=comInput)
        self.inputField.grid(column=0, row=2, sticky=NSEW)
        self.button = Button(self, text="Connect", command=lambda: controller.startConnection(comInput.get()))
        self.button.grid(columnspan=2, column=1, row=2, sticky=NSEW)


class DataMenu(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.config(bg='#FFF')
        self.grid(column=1, row=0, sticky=NSEW)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=16)
        self.rowconfigure(2, weight=2)

        self.controller = controller
        self.tabColor = '#FFF'
        self.tabSelectColor = '#2b78e4'
        self.tabFont = ("Helvetica", 12, "bold")

        # tabs op frame
        self.tab1= Button(self, text="Zonnescherm", bd=1, relief='solid', bg=self.tabSelectColor, fg='#FFF', font=self.tabFont, command=self.changeTabZonnescherm)
        self.tab1.grid(column=0, row=0, sticky=NSEW)
        self.tab2 = Button(self, text="Metingen", bd=1, relief='solid', bg=self.tabColor, font=self.tabFont, command=self.changeTabMetingen)
        self.tab2.grid(column=1, row=0, sticky=NSEW)
        self.tab3 = Button(self, text="Instellingen", bd=1, relief='solid', bg=self.tabColor, font=self.tabFont, command=self.changeTabInstellingen)
        self.tab3.grid(column=2, row=0, sticky=NSEW)

        self.progressBar = Label(self, bg='#5bff6c', bd=1, relief='solid')
        self.progressBar.grid(columnspan=3, row=2, sticky=NSEW)

    def changeTabZonnescherm(self):
        self.controller.show_frame(ZonneschermFrame)
        self.tab1.config(bg=self.tabSelectColor, fg='#FFF')
        self.tab2.config(bg=self.tabColor, fg='#000')
        self.tab3.config(bg=self.tabColor, fg='#000')

    def changeTabMetingen(self):
        self.controller.show_frame(MetingenFrame)
        self.tab1.config(bg=self.tabColor, fg='#000')
        self.tab2.config(bg=self.tabSelectColor, fg='#FFF')
        self.tab3.config(bg=self.tabColor, fg='#000')

    def changeTabInstellingen(self):
        self.controller.show_frame(InstellingenFrame)
        self.tab1.config(bg=self.tabColor, fg='#000')
        self.tab2.config(bg=self.tabColor, fg='#000')
        self.tab3.config(bg=self.tabSelectColor, fg='#FFF')


class DataFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.config(bg='#FFF')
        self.grid(columnspan=3, row=1, padx=16, pady=16, sticky=NSEW)

class ZonneschermFrame(DataFrame):
    def __init__(self, master):
        DataFrame.__init__(self, master)

        for i in range(12):
            self.columnconfigure(i, weight=1)

        for i in range(12):
            self.rowconfigure(i, weight=1)

        self.modusLabel = Label(self, text="Modus: ", font=("Helvetica", 8, "bold"))
        self.modusLabel.grid(column=9, row=0, sticky=NSEW)

        self.btnMode_1 = Button(self, text = "Automatisch", bg = '#cccccc', bd=2, relief='solid', font=("Helvetica", 6, "bold"))
        self.btnMode_1.grid(column=10, row=0, sticky = NSEW)
        self.btnMode_2 = Button(self, text = "Handmatig", bg = '#674ea7', fg='#FFF', bd=2, relief='solid', font=("Helvetica", 6, "bold"))
        self.btnMode_2.grid(column=11, row=0, sticky = NSEW)

        self.button = Button(self, text = "Oprollen", bg = '#5bff6c', bd=2, relief='solid', font=("Helvetica", 10, "bold"))
        self.button.grid(column=2, columnspan=4, row=5, rowspan=2, sticky = NSEW)
        self.button1 = Button(self, text = "Uitrollen", bg = '#ff6b5b', bd=2, relief='solid', font=("Helvetica", 10, "bold"))
        self.button1.grid(column=8, columnspan=3, row=5, rowspan=2, sticky=NSEW)

class MetingenFrame(DataFrame):
    def __init__(self, master):
        DataFrame.__init__(self, master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.label = Label(self, text="Grafiek1")
        self.label.grid(column=0, row=0, padx=8, pady=8, sticky=NSEW)
        self.label1 = Label(self, text="Grafiek2")
        self.label1.grid(column=1, row=0, padx=8, pady=8, sticky=NSEW)
        self.tabel = Label(self, text="Tabel")
        self.tabel.grid(column=0, row=1, padx=8, pady=8, sticky=NSEW)

class InstellingenFrame(DataFrame):
    def __init__(self, master):
        DataFrame.__init__(self, master)

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=10)
        self.columnconfigure(3, weight=5)
        for i in range(12):
            self.rowconfigure(i, weight=1)

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

        name = StringVar()
        self.entry1 =  Entry(self, highlightthickness=2, highlightbackground="black", width=50, font=8, textvariable=name)
        self.entry1.grid(column=2, row=0, sticky=W)

        self.scale1 = Scale(self, orient=HORIZONTAL,troughcolor="black",bg = "#FFF", highlightbackground="#FFF",length=300,relief=FLAT,sliderrelief=FLAT, width=8, font=8)
        self.scale1.grid(column=2, row=1,sticky=W)
        self.scale2 = Scale(self, orient=HORIZONTAL,troughcolor="black",bg = "#FFF", highlightbackground="#FFF",length=300,relief=FLAT,sliderrelief=FLAT, width=8, font=8)
        self.scale2.grid(column=2, row=2,sticky=W)

        self.spinbox1 = Spinbox(self, from_= 0, to=10, justify=CENTER,width=5, font=8)
        self.spinbox1.grid(column=2, row=5,sticky=W)
        self.spinbox1 = Spinbox(self, from_= 0, to=10, justify=CENTER, width=5,font=8)
        self.spinbox1.grid(column=2, row=6,sticky=W)
        self.spinbox1 = Spinbox(self, from_= 0, to=10, justify=CENTER, width=5,font=8)
        self.spinbox1.grid(column=2, row=9,sticky=W)
        self.spinbox1 = Spinbox(self, from_= 0, to=10, justify=CENTER, width=5,font=8)
        self.spinbox1.grid(column=2, row=10,sticky=W)

        self.button_opslaan = Button(self,text="Opslaan",font=8, command=lambda: controller.startSaveSettings(name.get(), self.scale1.get(), self.scale2.get()))
        self.button_opslaan.grid(columnspan=3,row=11)