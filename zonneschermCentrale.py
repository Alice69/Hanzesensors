from tkinter import *
from threading import Timer
import serial, time

class Protocol:
    def __init__(self):
        self.com = ""
        self.ser = None

    def changeSer(self, com, ser):
        self.com = com
        self.ser = ser

    def request(self, command, data=None):
        if self.ser == None:
            print("Serial port connection is None")
            return None

        try:
            self.ser.write((command + "\n").encode('ascii'))
            if data:
                self.ser.write((data + "\n").encode('ascii'))
        except serial.SerialException:
            return None

        test = None
        info = None
        try:
            test = self.ser.readline().decode('ascii').strip()
        except:
            print("Can't read response from" + command)

        if test not in ["OK", "ERR"]:
            info = test
            test = self.ser.readline().decode('ascii').strip()
            if test not in ["OK", "ERR"]:
                test = None

        return (test, info)

    def handshake(self):
        tries_left = 3
        while tries_left > 0:
            r = self.request("handshake")
            if r == ("OK", "pizza"):
                return True
            else:
                tries_left -= 1
                if (tries_left == 0):
                    return False

    def ping(self):
        return (self.request("ping") == ("OK", "pong"))

    def getName(self):
        response = self.request("getName")
        if response[0] == "OK":
            return response[1]
        else:
            return "Naamloos " + self.com

    def setName(self, name):
        response = self.request("setName", name)
        return (response == ("OK", "Name is set"))



comList = {}
protocol = Protocol()

def update():
    labelText = ""
    for com in list(comList.keys()):
        protocol.changeSer(com, comList.get(com))
        if (protocol.ping()):
            name = protocol.getName()
            print(name)
            labelText += name + ", "
        else:
            comList.get(com).close()
            comList.pop(com)
            print(com + " disconnected! :c")
    label.config(text=labelText)
    t = Timer(0.5, update)
    t.start()

def changeName():
    newName = nameInput.get()

    if (protocol.setName(newName)):
        print("Updated name!")
    else:
        print("Something went wrong :C")


class Model:
    def connect(self):
        comport = comInput.get()
        print("try connect to " + comport)
        try:
            ser = serial.Serial(comport, 19200, timeout=4)
        except serial.SerialException:
            print("Can't connect " + comport)
            return None
        time.sleep(2)
        protocol.changeSer(comport, ser)
        if protocol.handshake():
            comList[comport] = ser
        else:
            print("Handshake failed!")


model = Model()
tk = Tk()
tk.geometry('%dx%d+%d+%d' % (480, 200, 100, 100))
tk.columnconfigure(0, weight=3)
tk.columnconfigure(1, weight=1)
tk.rowconfigure(0, weight=1)
tk.rowconfigure(1, weight=1)
tk.rowconfigure(2, weight=1)


label = Label(tk, text="Welcome")
label.grid(columnspan=2, row=0, sticky=NSEW)

nameInput = StringVar()
inputField = Entry(tk, textvariable=nameInput)
inputField.grid(column=0, row=1, sticky=NSEW)
connectBtn = Button(tk, text='Change Name', command=changeName)
connectBtn.grid(column=1, row=1, sticky=NSEW)

comInput = StringVar()
inputField = Entry(tk, textvariable=comInput)
inputField.grid(column=0, row=2, sticky=NSEW)
connectBtn = Button(tk, text='Connect', command=model.connect)
connectBtn.grid(column=1, row=2, sticky=NSEW)


update()
tk.mainloop()