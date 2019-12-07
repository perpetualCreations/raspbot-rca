"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# science module (for collecting sensor data and saving it)
# creates GUI
# Made by Taian Chen (perpetualCreations)
"""

try:
    print("[INFO]: Starting imports...") # TODO test on actual raspberry pi
    import tkinter
    from sense_hat import SenseHat
    from time import gmtime
    from time import strftime
    import serial
    from time import sleep
except ImportError as e:
    tkinter = None
    gmtime = None
    strftime = None
    SenseHat = None
    serial = None
    sleep = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
    exit(1)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class science:
    """Creates a GUI interface for user to access scientific data collection."""
    def __init__(self):
        print("[INFO]: Science loaded!")
        print("[INFO]: Creating SenseHAT access interface...")
        self.sense = SenseHat()
        print("[INFO]: Loading graphics...")
        self.content = ""
        root = tkinter.Tk()
        root.title("Raspbot RCA-G: Science")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(400, 370))
        root.resizable(width=False, height=False)
        graphics_title = tkinter.Label(root, text = "Science", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 0, column = 0, padx = (0, 500))
        self.graphics_science = tkinter.Text(root, height = 15)
        self.graphics_science.configure(state = tkinter.DISABLED)
        self.graphics_science.grid(row = 1, column = 0, pady = (5, 14))
        graphics_science_frame_buttons = tkinter.Frame(root, bg = "#344561")
        graphics_science_button_reload = tkinter.Button(graphics_science_frame_buttons, text = "Refresh", fg = "white", bg = "#344561", width = 40, font = ("Calibri", 12), command = lambda: science.science_get(self))
        graphics_science_button_reload.pack(side = tkinter.TOP)
        graphics_science_button_save = tkinter.Button(graphics_science_frame_buttons, text = "Save", fg = "white", bg = "#344561", width = 40, font = ("Calibri", 12), command = lambda: science.science_save(self))
        graphics_science_button_save.pack(side = tkinter.BOTTOM)
        graphics_science_frame_buttons.grid(row = 2, column = 0, padx = (0, 250))
        root.mainloop()
    pass
    def science_get(self):
        """Calls SenseHAT Python integration package and Arduino PySerial for data inputs and collects output into self.content for displaying."""
        print("[INFO]: Refreshing science information...")
        print("[INFO]: Starting data collection...")
        print("[INFO]: Collecting data from sensors on SenseHAT...")
        temperature_data_raw = self.sense.get_temperature_from_humidity()
        temperature_data = round(temperature_data_raw, 2)
        pressure_data_raw = self.sense.get_pressure()
        pressure_data = round(pressure_data_raw, 2)
        humidity_data_raw = self.sense.get_humidity()
        humidity_data = round(humidity_data_raw, 2)
        self.sense.set_imu_config(True, True, True)
        orientation_raw = self.sense.get_orientation_degrees()
        compass_raw = self.sense.compass
        compass = round(compass_raw, 2)
        accelerometer_data = self.sense.get_accelerometer_raw()
        print("[INFO]: Collection completed.")
        temperature_str = str(temperature_data) + "C"
        pressure_str = str(pressure_data) + " Millibars"
        humidity_str = str(humidity_data) + "% Humidity"
        orientation_roll = str(round(orientation_raw["roll"], 2))
        orientation_pitch = str(round(orientation_raw["pitch"], 2))
        orientation_yaw = str(round(orientation_raw["yaw"], 2))
        orientation = "Orientation in Degrees, Roll: " + orientation_roll + ", Pitch: " + orientation_pitch + ", Yaw: " + orientation_yaw
        compass_str = str(compass) + " Degrees (0 being North)"
        accelerometer_x = str(round(accelerometer_data["x"], 2))
        accelerometer_y = str(round(accelerometer_data["y"], 2))
        accelerometer_z = str(round(accelerometer_data["z"], 2))
        accelerometer = "Acceleration in Gs, X: " + accelerometer_x + ", Y: " + accelerometer_y + ", Z: " + accelerometer_z
        print("[INFO]: Starting serial connection with Grove Arduino integration...")
        try:
            arduino = serial.Serial('/dev/ttyACM0', 9600)
        except serial.serialutil.SerialException:
            print("[FAIL]: Failed to create connection with Grove Arduino intergration!")
            return None
        pass
        sleep(5)
        print("[INFO]: Collecting data from serial.")
        arduino.write(b"D")
        grove_sensor_dust_lpo_data = arduino.read_until()
        dust_lpo = grove_sensor_dust_lpo_data.decode(encoding = "utf-8", errors = "replace")
        dust_lpo = dust_lpo.restrip("\n") + " (μs)"
        grove_sensor_dust_ratio_data = arduino.read_until()
        dust_ratio = grove_sensor_dust_ratio_data.decode(encoding = "utf-8", errors = "replace")
        dust_ratio = dust_ratio.rstrip("\n")
        grove_sensor_dust_concentration_data = arduino.read_until()
        dust_concentration = grove_sensor_dust_concentration_data.decode(encoding = "utf-8", errors = "replace")
        dust_concentration = dust_concentration.rstrip("\n") + " (pcs/L)"
        arduino.write(b"T")
        grove_sensor_distance_data = arduino.read_until()
        distance = grove_sensor_distance_data.decode(encoding = "utf-8", errors = "replace")
        distance = distance.rstrip("\n") + " (mm)"
        # NOTICE: Grove Light Sensor is not connected on official build, uncomment and configure in Arduino Instructions at your own will.
        # grove_sensor_light_data = arduino.read_until()
        # light = grove_sensor_light_data.decode(encoding = "utf-8", errors = "replace")
        # light = light.rstrip("\n")
        print("[INFO]: Generating timestamps...")
        timestamp = strftime("%b%d%Y%H%M%S"), gmtime()
        timestamp_output = timestamp[0]
        timestamp_str = str(timestamp_output)
        self.content = "Timestamp: " + timestamp_str + "\n" + "Temperature: " + temperature_str + "\n"\
                       + "Atm. Pressure: " + pressure_str + "\n" + "Atm. Humidity: " + humidity_str + "\n"\
                       + "Orientation: " + orientation + "\n" + "Compass: " + compass_str + "\n" + "Acceleration" \
                       + accelerometer + "\n" + "Dust LPO Time: " + dust_lpo + "\n" \
                       + "Dust LPO/Observation Time Ratio: " + dust_ratio + "\n" + "Dust Concentration: " \
                       + dust_concentration + "\n" + "ToF Distance: " + distance
        print("[INFO]: Done!")
        self.graphics_science.configure(state = tkinter.NORMAL)
        self.graphics_science.delete("1.0", tkinter.END)
        self.graphics_science.insert("1.0", self.content)
        self.graphics_science.configure(stat = tkinter.DISABLED)
    pass
    def science_save(self):
        """Collects self.content for saving to a text file."""
        if self.content == "":
            print("[FAIL]: No science data found, early exiting the function...")
            return None
        pass
        print("[INFO]: Generating timestamps...")
        timestamp = strftime("%b%d%Y%H%M%S"), gmtime()
        timestamp_output = timestamp[0]
        timestamp_str = str(timestamp_output)
        file_report_name = "science-report-" + timestamp_str + ".txt"
        print("[INFO]: Generating text file report...")
        file_report = open(file_report_name, "w+")
        file_report.write(self.content)
        file_report.close()
        print("[INFO]: Done!")
    pass
pass

vg = science()
