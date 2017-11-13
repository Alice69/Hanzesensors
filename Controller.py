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

    def startUpdate(self):
        self.t_update = Timer(10, protocol.update, [self.finnishUpdate])
        self.t_update.start()

    def finnishUpdate(self, devices):
        print("update", devices)
        self.mainFrame.updateInstellingen(devices)
        if self.running:
            self.startUpdate()

    def startConnection(self, comInput):
        if str.strip(comInput) == "" and len(str.strip(comInput)) > 19:
            return None
        print("start call")
        t_connection = Timer(0.5, protocol.connect, [self.finnishConnection, comInput])
        t_connection.start()

    def finnishConnection(self):
        print("Device connected!")

    def startSaveSettings(self, name):
        print("Saving..")
        t_save = Timer(0.5, protocol.saveSettings, [self.finnishSaveSettings, name])
        t_save.start()

    def finnishSaveSettings(self):
        print("Settings are saved! :)")