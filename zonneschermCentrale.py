from tkinter import *
from tkinter import ttk
from Controller import *


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
        self.emptyFrame = EmptyFrame(self.dataMenu)
        self.emptyFrame.tkraise()

    def getCenterGeometry(self, w, h):
        return (w, h, int(self.winfo_screenwidth() / 2) - int(w / 2), int(self.winfo_screenheight() / 2) - int(h / 2))

    def show_frame(self, frame):
        self.frames[frame].tkraise()

    def updateGUI(self, devices, data, instellingen):
        selectionReady = False
        for k, device in devices.items():
            if device['selected'] == 1:
                selectionReady = True

        if selectionReady:
            self.emptyFrame.hide()
            self.dataMenu.tab1.config(state=NORMAL)
            self.dataMenu.tab2.config(state=NORMAL)
            self.dataMenu.tab3.config(state=NORMAL)
            if device['status'] == "opgerold":
                self.dataMenu.progressBar.config(bg='#5bff6c', text="Opgerold")
            elif device['status'] == "uitgerold":
                self.dataMenu.progressBar.config(bg='#ff6b5b', text="Uitgerold")
            elif device['status'] == "oprollen":
                self.dataMenu.progressBar.config(bg='#ffd966', text="Bezig met oprollen..")
            elif device['status'] == "uitrollen":
                self.dataMenu.progressBar.config(bg='#ffd966', text="Bezig met uitrollen..")

            self.frames[InstellingenFrame].updateInstellingen(instellingen)
            self.frames[ZonneschermFrame].updateFrame(data)
        else:
            self.emptyFrame.show()
            self.dataMenu.tab1.config(state=DISABLED)
            self.dataMenu.tab2.config(state=DISABLED)
            self.dataMenu.tab3.config(state=DISABLED)
            self.dataMenu.progressBar.config(bg='#cccccc', text="")
        self.sideMenu.updateMenu(devices)


    def start_mainloop(self):
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.mainloop()

    def exit(self):
        self.destroy()
        controller.stop()


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

        self.mylist = Canvas(self, width=200, bg='#dddddd', height=300)
        self.mylist.grid(columnspan=2, row=1, sticky=NSEW)

        comInput = StringVar()
        self.inputField = Entry(self, bd=0, textvariable=comInput)
        self.inputField.grid(column=0, row=2, sticky=NSEW)
        self.button = Button(self, text="Connect", command=lambda: controller.startConnection(comInput.get()))
        self.button.grid(columnspan=2, column=1, row=2, sticky=NSEW)

    def updateMenu(self, devices):
        itemHeight = 60
        itemWidth = self.mylist.winfo_width()-(self.scrollbar.winfo_width()/2)
        dotSize = 16
        statusColor = {'0':'#ff6b5b', '1':'#5bff6c'}
        selectColor = [('#FFF', '#000'), ('#2b78e4', '#FFF')]

        self.mylist.delete("all")
        for i, item in enumerate(devices.items()):
            com, data = item[0], item[1]
            y = (i * itemHeight)
            self.mylist.create_rectangle(0,y, itemWidth, y + itemHeight, tags="btn-{}".format(i), fill=selectColor[data['selected']][0])
            self.mylist.tag_bind("btn-{}".format(i), '<ButtonPress-1>', lambda event, idx=i, com=com: controller.startConnection(com))
            self.mylist.create_oval(10, y+(itemHeight/2)-(dotSize/2), 10+dotSize, y+(itemHeight/2)+(dotSize/2), fill=statusColor[data['status']])
            self.mylist.create_text(itemWidth/2, (i * itemHeight) + (itemHeight/2), text=data['naam'], fill=selectColor[data['selected']][1], font=("Helvetica", 10, "bold"))
        self.scrollbar.config(command=self.mylist.yview)
        self.mylist.config(yscrollcommand=self.scrollbar.set, scrollregion=(0,0,0,len(devices)*itemHeight))


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
        self.tab1= Button(self, text="Zonnescherm", bd=1, relief='solid', bg=self.tabSelectColor, fg='#fff', font=self.tabFont, state=DISABLED, command=self.changeTabZonnescherm)
        self.tab1.grid(column=0, row=0, sticky=NSEW)
        self.tab2 = Button(self, text="Metingen", bd=1, relief='solid', bg=self.tabColor, font=self.tabFont, state=DISABLED, command=self.changeTabMetingen)
        self.tab2.grid(column=1, row=0, sticky=NSEW)
        self.tab3 = Button(self, text="Instellingen", bd=1, relief='solid', bg=self.tabColor, font=self.tabFont, state=DISABLED, command=self.changeTabInstellingen)
        self.tab3.grid(column=2, row=0, sticky=NSEW)

        self.progressBar = Label(self, bg='#cccccc', font=("Helvetica", 10, "bold"), border=0)
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



class EmptyFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.config(bg='#EEE')
        self.show()

    def show(self):
        self.grid(columnspan=3, row=1, sticky=NSEW)
        self.tkraise()

    def hide(self):
        self.grid_forget()

class DataFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.config(bg='#FFF')
        self.grid(columnspan=3, row=1, padx=16, pady=16, sticky=NSEW)


class ZonneschermFrame(DataFrame):
    def __init__(self, master):
        DataFrame.__init__(self, master)
        self.handmatig = False

        for i in range(12):
            self.columnconfigure(i, weight=1)

        for i in range(12):
            self.rowconfigure(i, weight=1)

        self.modusLabel = Label(self, text="Modus: ", font=("Helvetica", 8, "bold"))
        self.modusLabel.grid(column=9, row=0, sticky=NSEW)

        self.btnMode_1 = Button(self, text = "Automatisch", bd=2, relief='solid', font=("Helvetica", 6, "bold"), command=self.setAuto)
        self.btnMode_1.grid(column=10, row=0, sticky = NSEW)
        self.btnMode_2 = Button(self, text = "Handmatig", bd=2, relief='solid', font=("Helvetica", 6, "bold"), command=self.setHandmatig)
        self.btnMode_2.grid(column=11, row=0, sticky = NSEW)

        self.button = Button(self, text = "Oprollen", bg = '#5bff6c', bd=2, relief='solid', font=("Helvetica", 10, "bold"), command=controller.startRolOp)
        self.button1 = Button(self, text = "Uitrollen", bg = '#ff6b5b', bd=2, relief='solid', font=("Helvetica", 10, "bold"), command=controller.startRolUit)

    def updateFrame(self, data):
        if data and self.handmatig == False:
            modus = int(data['getModus'])
        else:
            modus = 1
        if modus == 0:
            self.btnMode_1.config(bg='#674ea7', fg='#FFF')
            self.btnMode_2.config(bg='#cccccc', fg='#000')
            self.button.grid_forget()
            self.button1.grid_forget()
        if modus == 1:
            self.btnMode_1.config(bg='#cccccc', fg='#000')
            self.btnMode_2.config(bg='#674ea7', fg='#FFF')
            self.button.grid(column=2, columnspan=4, row=5, rowspan=2, sticky=NSEW)
            self.button1.grid(column=8, columnspan=3, row=5, rowspan=2, sticky=NSEW)

    def setHandmatig(self):
        self.handmatig = True
        self.updateFrame(None)

    def setAuto(self):
        self.handmatig = False
        controller.startSetAuto()


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

        self.entry1 =  Entry(self, highlightthickness=2, highlightbackground="black", width=50, font=8)
        self.entry1.grid(column=2, row=0, sticky=W)

        self.scale1 = Scale(self, from_= 1, to=10, orient=HORIZONTAL,troughcolor="black",bg = "#FFF", highlightbackground="#FFF",length=300,relief=FLAT,sliderrelief=FLAT, width=8, font=8)
        self.scale1.grid(column=2, row=1,sticky=W)
        self.scale2 = Scale(self, from_= 1, to=10, orient=HORIZONTAL,troughcolor="black",bg = "#FFF", highlightbackground="#FFF",length=300,relief=FLAT,sliderrelief=FLAT, width=8, font=8)
        self.scale2.grid(column=2, row=2,sticky=W)

        self.spinbox1 = Spinbox(self, from_= 0, to=50, justify=CENTER,width=5, font=8)
        self.spinbox1.grid(column=2, row=5,sticky=W)
        self.spinbox2 = Spinbox(self, from_= 1, to=10, justify=CENTER, width=5,font=8)
        self.spinbox2.grid(column=2, row=6,sticky=W)
        self.spinbox3 = Spinbox(self, from_= 0, to=50, justify=CENTER, width=5,font=8)
        self.spinbox3.grid(column=2, row=9,sticky=W)
        self.spinbox4 = Spinbox(self, from_= 1, to=10, justify=CENTER, width=5,font=8)
        self.spinbox4.grid(column=2, row=10,sticky=W)

        self.button_opslaan = Button(self,text="Opslaan",font=8, command=self.save)
        self.button_opslaan.grid(columnspan=3,row=11)

    def save(self):
        controller.startSaveSettings(
            self.entry1.get(),
            (self.scale1.get(), self.scale2.get()),
            (self.spinbox1.get(), self.spinbox3.get()),
            (self.spinbox2.get(), self.spinbox4.get())
        )

    def updateInstellingen(self, instellingen):
        if instellingen != {}:
            self.entry1.delete(0, "end")
            self.entry1.insert(0, instellingen['naam'])

            self.scale1.set(instellingen["getUitrolstand"][0])
            self.scale2.set(instellingen["getUitrolstand"][1])

            self.spinbox1.delete(0, "end")
            self.spinbox1.insert(0, instellingen["getSettingsTemp"][0])
            self.spinbox3.delete(0, "end")
            self.spinbox3.insert(0, instellingen["getSettingsTemp"][1])

            self.spinbox2.delete(0, "end")
            self.spinbox2.insert(0, instellingen["getSettingsLicht"][0])
            self.spinbox4.delete(0, "end")
            self.spinbox4.insert(0, instellingen["getSettingsLicht"][1])


controller = Controller()
mainFrame = MainFrame(1024, 600)
controller.myInit(mainFrame)

mainFrame.start_mainloop()