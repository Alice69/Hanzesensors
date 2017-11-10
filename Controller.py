from Protocol import *
from threading import Timer

class Controller:
    def startConnection(self):
        print("start call")
        t = Timer(0.5, callTest)
        t.start()

    def finnishConnection(self):
        print("Device connected!")