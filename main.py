from home_connection import HomeAutomationSystemConnection
from air_conditioner import AirConditionerSystemConnection
from curtain_control import CurtainControlSystemConnection

conn = HomeAutomationSystemConnection("COM9", 9600)
conn.open()

air = AirConditionerSystemConnection(conn)
curtain = CurtainControlSystemConnection(conn)

while True:
    print("\nMAIN MENU")
    print("1. Air Conditioner")
    print("2. Curtain Control")
    print("3. Exit")

    choice = input("Select: ")

    if choice == "1":
        air.update()
        print("Desired Temp:", air.desiredTemperature)
        print("Ambient Temp:", air.ambientTemperature)
        print("Fan Speed:", air.fanSpeed)

    elif choice == "2":
        curtain.update()
        print("Outdoor Temp:", curtain.outdoorTemperature)
        print("Outdoor Pressure:", curtain.outdoorPressure)
        print("Light Intensity:", curtain.lightIntensity)

    elif choice == "3":
        conn.close()
        break
