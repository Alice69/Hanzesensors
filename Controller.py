from Protocol import *
from threading import Timer
import sys

protocol = Protocol()

class Controller:
    def myInit(self, mainFrame):
        self.mainFrame = mainFrame
        self.running = True
        self.t_update = None
        self.startUpdate()

    def stop(self):
        self.running = False
        self.t_update.cancel()
        #sys.exit(1)

    def startUpdate(self, timer=10):
        self.t_update = Timer(timer, protocol.update, [self.finnishUpdate])
        self.t_update.start()

    def finnishUpdate(self, devices, data, instellingen):
        #print("update", devices)
        self.mainFrame.updateGUI(devices, data, instellingen)
        if self.running:
            self.startUpdate()

    def startConnection(self, comInput):
        if str.strip(comInput) == "":
            return None
        print("start call")
        self.t_update.cancel()
        t_connection = Timer(0.5, protocol.connect, [self.finnishConnection, self.failedConnection, comInput])
        t_connection.start()

    def finnishConnection(self):
        print("Device connected!")
        self.startUpdate(0)

    def failedConnection(self):
        print("Connection failed!")
        self.startUpdate()


    '''--------------------
    --------Settings-------
    --------------------'''
    def startSaveSettings(self, name, uitrolstand, setTemp, setLicht):
        print("Saving..", (name, uitrolstand, setTemp, setLicht))
        self.t_update.cancel()
        t_save = Timer(0.5, protocol.saveSettings, [self.finnishSaveSettings, name, uitrolstand, setTemp, setLicht])
        t_save.start()

    def finnishSaveSettings(self):
        print("Settings are saved! :)")
        self.startUpdate(0)


    '''--------------------
    --------Actions--------
    --------------------'''
    # Zet automatisch
    def startSetAuto(self):
        print("Saving..")
        self.t_update.cancel()
        t_save = Timer(0.5, protocol.setAuto, [self.finnishSetAuto,self.failedSetAuto])
        t_save.start()

    def finnishSetAuto(self):
        print("Mode has changed")
        self.startUpdate(0)

    def failedSetAuto(self):
        self.startUpdate()

    # Oprollen
    def startRolOp(self):
        self.t_update.cancel()
        t_save = Timer(0.5, protocol.rolOp, [self.finnishRolOp, self.failedRolOp])
        t_save.start()

    def finnishRolOp(self):
        print("Het zonnescherm wordt op handmatig gezet en gaat oprollen.")
        self.startUpdate(0)

    def failedRolOp(self):
        self.startUpdate()

    # Uitrollen
    def startRolUit(self):
        self.t_update.cancel()
        t_save = Timer(0.5, protocol.rolUit, [self.finnishRolUit, self.failedRolUit])
        t_save.start()

    def finnishRolUit(self):
        print("Het zonnescherm wordt op handmatig gezet en gaat uitrollen.")
        self.startUpdate(0)

    def failedRolUit(self):
        self.startUpdate()