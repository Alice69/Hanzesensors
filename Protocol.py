import serial, time


def callTest():
    time.sleep(1000)
    # Misschien toegang naar controller ofzow? send callback << function


class Connection:
    def __init__(self):
        self.comList = {}
        self.protocol = Protocol()

    def connect(self, comp):
        comport = "COM4" #comInput.get()
        print("try connect to " + comport)
        try:
            ser = serial.Serial(comport, 19200, timeout=4)
        except serial.SerialException:
            print("Can't connect " + comport)
            return None
        time.sleep(2)
        self.protocol.changeSer(comport, ser)
        if self.protocol.handshake():
            self.comList[comport] = ser
        else:
            print("Handshake failed!")

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