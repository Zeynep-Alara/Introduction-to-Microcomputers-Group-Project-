import serial

ser = serial.Serial("COM10", 9600, timeout=1)

print("Fake PIC running on COM10...")

while True:
    data = ser.read(1)
    if data:
        print("Received:", data)
        
        # Respond with a simple fake value
        # e.g. always return 25.3 degrees or fan speed=100
        cmd = data[0]

        if cmd == 0b00000001:  # desired temp fractional
            ser.write(bytes([3]))  # 0.3
        elif cmd == 0b00000010:  # desired temp integral
            ser.write(bytes([25])) # 25
        elif cmd == 0b00000011:  # ambient temp fractional
            ser.write(bytes([8]))
        elif cmd == 0b00000100:  # ambient temp integral
            ser.write(bytes([22]))
        elif cmd == 0b00000101:  # fan speed
            ser.write(bytes([90]))
