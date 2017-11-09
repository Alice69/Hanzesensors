from tkinter import *
import serial, time


class Protocol:
    def __init__(self):
        self.ser = None

    def changeSer(self, ser):
        self.ser = ser

    def request(self, command, data=None):
        try:
            self.ser.write((command + "\n").encode('ascii'))
            if data:
                self.ser.write((data + "\n").encode('ascii'))
        except serial.SerialException:
            return None

        test = self.ser.readline().decode('ascii').strip()
        info = None
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



comList = {}
protocol = Protocol()
tk = Tk()
tk.columnconfigure(0, weight=3)
tk.columnconfigure(1, weight=1)
tk.rowconfigure(0, weight=1)
tk.rowconfigure(1, weight=1)
comInput = StringVar()
inputField = Entry(tk, textvariable=comInput)
inputField.grid(column=0, row=0, sticky=NSEW)

def update():
    for com in list(comList.keys()):
        protocol.changeSer(comList.get(com))
        if (protocol.request("ping") == ("OK", "pong")):
            print(protocol.request("getName"))
        else:
            comList.get(com).close()
            comList.pop(com)
            print(com + " disconnected! :c")
    tk.after(1000, update)
update()

def connect():
    comport = comInput.get()
    try:
        ser = serial.Serial(comport, 19200, timeout=4)
    except serial.SerialException:
        print("Can't connect " + comport)
        return None
    time.sleep(2)
    protocol.changeSer(ser)
    if protocol.handshake():
        comList[comport] = ser
    else:
        print("Handshake failed!")

connectBtn = Button(tk, text='Connect', command=connect)
connectBtn.grid(column=1, row=0, sticky=NSEW)



tk.mainloop()





'''comport = input("COM Poort:")
protocol = Protocol()
if (protocol.handshake(comport)):
    print(comport + " connected! =D")

    while (1):
        if protocol.request("ping") != ("OK", "pong"):
            print(comport + " disconnected! :c")

        print("Get existing name: ", protocol.request("getName"))
        time.sleep(4)
        print("Get existing min and max temperature: ", protocol.request("getMinMaxTemp"))
        time.sleep(4)

        newName = input("New name: ")
        print("Changing naam: ", protocol.request("setName", newName))
        time.sleep(2)
        print("Get new name: ", protocol.request("getName"))
        time.sleep(2)
        print("Set new min and max temperature: ", protocol.request("setMinMaxTemp"))
        time.sleep(2)
        print("Get new min and max temperature: ", protocol.request("getMinMaxTemp"))
        time.sleep(6)
else:
    print("Handshake failed!")'''