from Protocol import *
from threading import Timer

connection = Connection()
# Misschien de lijst met compoorten toch maar hierin?

class Controller:
    def __init__(self):
        self.update()

    def update(self):
        # check voor connecties, sturen van ping, getname etc.
        print( connection.protocol.getName() )
        t = Timer(0.5, self.update)
        t.start()

    def startConnection(self, comInput):
        if str.strip(comInput) == "":
            return None
        print("start call")
        t = Timer(0.5, connection.connect, [self.finnishConnection, comInput])
        t.start()

    def finnishConnection(self):
        print("Device connected!")