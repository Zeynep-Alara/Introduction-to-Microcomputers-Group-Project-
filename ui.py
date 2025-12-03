import customtkinter as ctk
from home_connection import HomeAutomationSystemConnection
from air_conditioner import AirConditionerSystemConnection
from curtain_control import CurtainControlSystemConnection

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HomeAutomationUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Home Automation Panel")
        self.geometry("600x420")
        self.resizable(False, False)

        # MAIN FRAME
        self.main_frame = ctk.CTkFrame(self, fg_color="#1c1c1c")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Connection Section
        self.conn = HomeAutomationSystemConnection("COM10", 9600)

        conn_frame = ctk.CTkFrame(self.main_frame)
        conn_frame.pack(pady=10)

        self.connect_btn = ctk.CTkButton(conn_frame, text="Connect", width=120, command=self.connect)
        self.connect_btn.grid(row=0, column=0, padx=5)

        self.disconnect_btn = ctk.CTkButton(conn_frame, text="Disconnect", width=120, state="disabled", 
                                            fg_color="gray30", command=self.disconnect)
        self.disconnect_btn.grid(row=0, column=1, padx=5)

        # Tabs
        self.tabview = ctk.CTkTabview(self.main_frame, width=520, height=290)
        self.tabview.pack(pady=10)

        self.air_tab = self.tabview.add("Air Conditioner")
        self.curtain_tab = self.tabview.add("Curtain Control")

        # Build UIs
        self.build_air_ui()
        self.build_curtain_ui()

    # -------------------- CONNECTION ---------------------
    def connect(self):
        try:
            self.conn.open()
            self.connect_btn.configure(state="disabled")
            self.disconnect_btn.configure(state="normal")
        except Exception as e:
            print("Connection error:", e)

    def disconnect(self):
        try:
            self.conn.close()
            self.connect_btn.configure(state="normal")
            self.disconnect_btn.configure(state="disabled")
        except:
            pass

    # -------------------- AIR CONDITIONER ---------------------
    def build_air_ui(self):
        self.air = AirConditionerSystemConnection(self.conn)

        title = ctk.CTkLabel(self.air_tab, text="Air Conditioner Status", font=("Arial", 18))
        title.pack(pady=10)

        self.air_values = ctk.CTkFrame(self.air_tab)
        self.air_values.pack(pady=10)

        self.desired_lbl = self.create_value_row(self.air_values, "Desired Temp:")
        self.ambient_lbl = self.create_value_row(self.air_values, "Ambient Temp:")
        self.fan_lbl = self.create_value_row(self.air_values, "Fan Speed:")

        update_btn = ctk.CTkButton(self.air_tab, text="Update Values", width=150, command=self.update_air)
        update_btn.pack(pady=10)

    def update_air(self):
        self.air.update()
        self.desired_lbl.configure(text=str(self.air.desiredTemperature))
        self.ambient_lbl.configure(text=str(self.air.ambientTemperature))
        self.fan_lbl.configure(text=str(self.air.fanSpeed))

    # -------------------- CURTAIN CONTROL ---------------------
    def build_curtain_ui(self):
        self.curtain = CurtainControlSystemConnection(self.conn)

        title = ctk.CTkLabel(self.curtain_tab, text="Curtain Sensor Data", font=("Arial", 18))
        title.pack(pady=10)

        self.curtain_values = ctk.CTkFrame(self.curtain_tab)
        self.curtain_values.pack(pady=10)

        self.outdoor_temp_lbl = self.create_value_row(self.curtain_values, "Outdoor Temp:")
        self.outdoor_pressure_lbl = self.create_value_row(self.curtain_values, "Outdoor Pressure:")
        self.light_lbl = self.create_value_row(self.curtain_values, "Light Intensity:")

        update_btn = ctk.CTkButton(self.curtain_tab, text="Update Values", width=150, command=self.update_curtain)
        update_btn.pack(pady=10)

    def update_curtain(self):
        self.curtain.update()
        self.outdoor_temp_lbl.configure(text=str(self.curtain.outdoorTemperature))
        self.outdoor_pressure_lbl.configure(text=str(self.curtain.outdoorPressure))
        self.light_lbl.configure(text=str(self.curtain.lightIntensity))

    # -------------------- HELPER FUNCTION ---------------------
    def create_value_row(self, parent, label_text):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(anchor="w", pady=5)

        lbl = ctk.CTkLabel(row, width=200, text=label_text, anchor="w")
        lbl.pack(side="left")

        value_lbl = ctk.CTkLabel(row, text="-", anchor="w")
        value_lbl.pack(side="left", padx=10)

        return value_lbl


# -------------------- RUN WINDOW ---------------------
app = HomeAutomationUI()
app.mainloop()
