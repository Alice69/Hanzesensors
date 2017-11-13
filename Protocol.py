import serial, time

class Connection:
    def __init__(self, com, ser):
        self.com = com
        self.ser = ser

class Protocol:
    def __init__(self):
        self.comList = {}

        self.connection = ("", None)#Connection("", None)
        self.selectConn = ("", None)#Connection("COM4", None)


    '''------------------------
    -------Connection----------
    ------------------------'''
    def changeSer(self, com, ser):
        self.connection = (com, ser)

    def selectSer(self, com):
        self.selectConn = (com, self.comList.get(com))

    def connect(self, callback, comport):
        print("try connect to " + comport)
        try:
            self.connection = (comport, serial.Serial(comport, 19200, timeout=4))
        except serial.SerialException:
            print("Can't connect " + comport)
            return None
        time.sleep(2)
        if self.handshake():
            self.comList[comport] = self.connection[1]
            callback()
        else:
            print("Handshake failed!")


    '''------------------------
    ---------Request-----------
    ------------------------'''
    def request(self, command, data=None):
        if self.connection[1] == None:
            #print("Serial port connection is None")
            return None

        print("command: {} to {}".format(command, self.connection[0]))

        try:
            self.connection[1].write((command + "\n").encode('ascii'))
            if data:
                self.connection[1].write((data + "\n").encode('ascii'))
        except serial.SerialException:
            return None

        test = None
        info = None
        try:
            test = self.connection[1].readline().decode('ascii').strip()
        except:
            print("Can't read response from" + command)

        if test not in ["OK", "ERR"]:
            info = test
            test = self.connection[1].readline().decode('ascii').strip()
            if test not in ["OK", "ERR"]:
                test = None

        return (test, info)


    '''------------------------
    --------Protocol-----------
    ------------------------'''
    # Connection and Update:
    def handshake(self):
        tries_left = 3
        while tries_left > 0:
            r = self.request("handshake")
            if r == ("OK", "handshake"):
                return True
            else:
                tries_left -= 1
                if (tries_left == 0):
                    return False

    def update(self, callback):
        devices = {}
        for com in list(self.comList.keys()):
            self.changeSer(com, self.comList.get(com))
            if self.ping():
                devices[com] = {
                    "naam": self.getNaam(),
                    "tempSettings": self.getSettingsTemp(),
                    "lichtSettings": self.getSettingsLicht(),
                    "uitrolSettings": self.getUitrolstand(),
                    "temperatuur": self.getSensorTemp(),
                    "lichtsterkte": self.getSensorLicht(),
                    "getAfstand": self.getAfstand(),
                    "getModus": self.getModus()
                }
            else:
                self.comList.pop(com)
        callback(devices)

    def ping(self):
        return (self.request("ping") == ("OK", "pong"))


    # Get:
    def getNaam(self):
        response = self.request("getNaam")
        if response[0] == "OK":
            if response[1] == "":
                return "Naamloos " + self.connection[0]
            else:
                return response[1]
        else:
            return None

    def getSettingsTemp(self):
        response = self.request("getSettingsTemp")
        if response[0] == "OK":
            settings = response[1].split(',')
            return (settings[0], settings[1])
        else:
            return (None, None)

    def getSettingsLicht(self):
        response = self.request("getSettingsLicht")
        if response[0] == "OK":
            settings = response[1].split(',')
            return (settings[0], settings[1])
        else:
            return (None, None)

    def getUitrolstand(self):
        response = self.request("getUitrolstand")
        if response[0] == "OK":
            settings = response[1].split(',')
            return (settings[0], settings[1])
        else:
            return (None, None)

    def getSensorTemp(self):
        response = self.request("getSensorTemp")
        if response[0] == "OK":
            return response[1]
        else:
            return None

    def getSensorLicht(self):
        response = self.request("getSensorLicht")
        if response[0] == "OK":
            return response[1]
        else:
            return None

    def getAfstand(self):
        response = self.request("getAfstand")
        if response[0] == "OK":
            return response[1]
        else:
            return None

    def getModus(self):
        response = self.request("getModus")
        if response[0] == "OK":
            return response[1]
        else:
            return None


    # Set:
    def saveSettings(self, callback, name):
        self.selectSer("COM5")
        self.connection = self.selectConn
        self.setNaam(name)
        callback()

    def setNaam(self, name):
        response = self.request("setNaam", name)
        return (response[0] == "OK")

    def setTemp(self, min, max):
        # Dubbele data verzenden
        response = self.request("setTemp")
        return (response[0] == "OK")

    def setLicht(self, min, max):
        # Dubbele data verzenden
        response = self.request("setLicht")
        return (response[0] == "OK")

    def setUitrolstand(self, min, max):
        # Dubbele data verzenden
        response = self.request("setUitrolstand")
        return (response[0] == "OK")


    # Actie:
    def rolOp(self):
        response = self.request("rolOp")
        return (response[0] == "OK")

    def rolUit(self):
        response = self.request("rolUit")
        return (response[0] == "OK")

    def setAuto(self):
        response = self.request("setAuto")
        return (response[0] == "OK")