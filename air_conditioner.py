class AirConditionerSystemConnection:
    def __init__(self, connection):
        self.conn = connection
        self.desiredTemperature = 0.0
        self.ambientTemperature = 0.0
        self.fanSpeed = 0
    

    def _read_float(self, cmd_low, cmd_high):
        """Reads low byte + high byte, returns combined float."""
        self.conn.sendByte(cmd_low)
        low = self.conn.readByte()

        self.conn.sendByte(cmd_high)
        high = self.conn.readByte()

        if low is None or high is None:
            return None
        
        return high + low / 10.0

    def update(self):
        """Refresh all data from board #1 via UART."""
        # Desired temperature
        self.desiredTemperature = self._read_float(0b00000001, 0b00000010)

        # Ambient temperature
        self.ambientTemperature = self._read_float(0b00000011, 0b00000100)

        # Fan speed
        self.conn.sendByte(0b00000101)
        speed = self.conn.readByte()
        if speed is not None:
            self.fanSpeed = speed

    def setDesiredTemp(self, value):
        """Send new desired temperature to the board."""
        integral = int(value)
        fractional = int((value - integral) * 10)

        # Send low byte (fractional)
        self.conn.sendByte(0b10000000 | fractional)

        # Send high byte (integral)
        self.conn.sendByte(0b11000000 | integral)

    def getDesiredTemp(self):
         return self.desiredTemperature