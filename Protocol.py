import serial, time

class Connection:
    def __init__(self, com, ser):
        self.com = com
        self.ser = ser

class Protocol:
    def __init__(self):
        self.comList = {}

        self.connection = ("", None)
        self.selectConn = ("", None)


    '''------------------------
    -------Connection----------
    ------------------------'''
    def changeSer(self, com, ser):
        self.connection = (com, ser)

    def selectSer(self, com):
        self.selectConn = (com, self.comList.get(com))
        print(self.selectConn)

    def connect(self, success, fail, comport):
        if comport in self.comList.keys():
            self.selectSer(comport)
            success()
            return

        print("try connect to " + comport)
        try:
            self.connection = (comport, serial.Serial(comport, 19200, timeout=4))
        except serial.SerialException:
            print("Can't connect " + comport)
            fail()
            return
        time.sleep(2)
        if self.handshake():
            self.comList[comport] = self.connection[1]
            success()
        else:
            print("Handshake failed!")
            fail()


    '''------------------------
    ---------Request-----------
    ------------------------'''
    def request(self, command, data=None, data2=None):
        if self.connection[1] == None:
            #print("Serial port connection is None")
            return
        # print("command: {} to {}".format(command, self.connection[0]))

        try:
            self.connection[1].write((command + "\n").encode('ascii'))
            if data:
                    self.connection[1].write((str(data) + "\n").encode('ascii'))
            if data2:
                self.connection[1].write((str(data2) + "\n").encode('ascii'))
        except serial.SerialException:
            return

        test = None
        info = None
        while(test == None):
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
        selectedDevice = None
        for com in list(self.comList.keys()):
            self.changeSer(com, self.comList.get(com))
            if self.ping():
                naam = self.getNaam()
                if com == self.selectConn[0]:
                    selectedDevice = com
                    devices[com] = {
                        "naam": naam,
                        "status": self.getStatus(),
                        "getSensorTemp": self.getSensorTemp(),
                        "getSensorLicht": self.getSensorLicht(),
                        "getModus": self.getModus(),
                        "getSettingsTemp": self.getSettingsTemp(),
                        "getSettingsLicht": self.getSettingsLicht()
                    }
                else:
                    devices[com] = {
                        "naam": naam,
                        "status": self.getStatus()
                    }
            else:
                self.comList.pop(com)
        callback(devices, selectedDevice)

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

    def getStatus(self):
        response = self.request("getStatus")
        if response[0] == "OK":
            return response[1]
        else:
            return "0"

    def getModus(self):
        response = self.request("getModus")
        if response[0] == "OK":
            return response[1]
        else:
            return "1"


    # Set:
    def saveSettings(self, callback, name, uitrolstand, setTemp, setLicht):
        self.connection = self.selectConn
        self.setNaam(name)
        #self.setUitrolstand(uitrolstand[0], uitrolstand[1])
        self.setTemp(setTemp[0], setTemp[1])
        self.setLicht(setLicht[0], setLicht[1])
        callback()

    def setNaam(self, name):
        response = self.request("setNaam", name)
        return (response[0] == "OK")

    def setTemp(self, min, max):
        # Dubbele data verzenden
        response = self.request("setTemp", min)
        return (response[0] == "OK")

    def setLicht(self, min, max):
        # Dubbele data verzenden
        response = self.request("setLicht", min)
        return (response[0] == "OK")

    def setUitrolstand(self, min, max):
        # Dubbele data verzenden
        response = self.request("setUitrolstand", min, max)
        return (response[0] == "OK")


    # Actie:
    def rolOp(self, success, failed):
        response = self.request("rolOp")
        if (response[0] == "OK"):
            success()
        else:
            failed()

    def rolUit(self, success, failed):
        response = self.request("rolUit")
        if (response[0] == "OK"):
            success()
        else:
            failed()

    def setAuto(self, success, failed):
        response = self.request("setAuto")
        if (response[0] == "OK"):
            success()
        else:
            failed()