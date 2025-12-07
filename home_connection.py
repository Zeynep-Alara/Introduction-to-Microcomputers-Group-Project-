import serial
from air_conditioner import AirConditionerSystemConnection
from curtain_control import CurtainControlSystemConnection

class HomeAutomationSystemConnection:
    def __init__(self, port="COM9", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.air = AirConditionerSystemConnection(self)
        self.curtain = CurtainControlSystemConnection(self)


    def open(self):
        """Open the serial connection."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            return True
        except Exception as e:
            print("Error opening port:", e)
            return False

    def close(self):
        """Close the serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()

    def setComPort(self, port):
        self.port = port

    def setBaudRate(self, rate):
        self.baudrate = rate

    def sendByte(self, value):
        """Send a single byte (0-255)."""
        if self.ser and self.ser.is_open:
            self.ser.write(bytes([value]))

    def readByte(self):
        """Read a single byte. Returns integer."""
        if self.ser and self.ser.is_open:
            data = self.ser.read(1)
            if data:
                return int.from_bytes(data, "little")
            return None
        
    def update(self):
        self.air.update()
        self.curtain.update()