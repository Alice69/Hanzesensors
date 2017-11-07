import serial, time

class Protocol:
    def __init__(self):
        self.ser = None

    def request(self, command):
        try:
            self.ser.write((command + "\n").encode('ascii'))
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

    def handshake(self, comport):
        try:
            self.ser = serial.Serial(comport, 19200, timeout=4)
            time.sleep(2)
        except serial.SerialException:
            print("No device in " + comport)
            return False

        tries_left = 3
        while tries_left > 0:
            r = self.request("handshake")
            if r == ("OK", "pizza"):
                return True
            else:
                tries_left -= 1
                if (tries_left == 0):
                    return False



comport = input("COM Poort:")
protocol = Protocol()
if (protocol.handshake(comport)):
    print(comport + " connected! =D")

    while (1):
        if protocol.request("ping") != ("OK", "pong"):
            print(comport + " disconnected! :c")
        time.sleep(1)
else:
    print("Handshake failed!")