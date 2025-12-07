class CurtainControlSystemConnection:
    def __init__(self, connection):
        self.conn = connection
        self.curtainStatus = 0.0
        self.outdoorTemperature = 0.0
        self.outdoorPressure = 0.0
        self.lightIntensity = 0.0

    def _read_float(self, cmd_low, cmd_high):
        self.conn.sendByte(cmd_low)
        low = self.conn.readByte()

        self.conn.sendByte(cmd_high)
        high = self.conn.readByte()

        if low is None or high is None:
            return None

        return high + low / 10.0

    def update(self):
        """Refresh curtain, temperature, pressure, and light values."""
        # Desired curtain status is not needed for display — skip

        # Outdoor temperature
        self.outdoorTemperature = self._read_float(0b00000011, 0b00000100)

        # Outdoor pressure
        self.outdoorPressure = self._read_float(0b00000101, 0b00000110)

        # Light intensity
        self.lightIntensity = self._read_float(0b00000111, 0b00001000)

    def setCurtainStatus(self, value):
        """Set curtain openness (0–100%)."""
        integral = int(value)
        fractional = int((value - integral) * 10)

        # low byte
        self.conn.sendByte(0b10000000 | fractional)

        # high byte
        self.conn.sendByte(0b11000000 | integral)

    def getCurtainStatus(self):
        return self.curtainStatus
