"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
telemetry module, for collecting telemetry information
Made by perpetualCreations
"""

print("[INFO]: Initiating telemetry module...")

try:
    from time import sleep
    from basics import basics, serial
except ImportError as ImportErrorMessage:
    print("[FAIL]: Imports failed! See below.")
    print(ImportErrorMessage)
    basics.exit(1)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(ImportWarningMessage)
    basics.exit(1)
pass

print("[INFO]: Initiation of telemetry complete!")

class telemetry:
    """
    Class for telemetry data collection.
    """
    def __init__(self):
        self.components = basics.load_hardware_config()
        if self.components[1][0] is True:
            import sense_hat
            self.sense = sense_hat.SenseHat()
        else: self.sense = None

    def get(self):
        """
        Calls SenseHAT Python integration package and Arduino PySerial for data inputs and returns formatted output.
        :return: str, multi-line
        """
        print("[INFO]: Starting data collection...")
        if self.components[1][0] is True:
            self.sense.set_imu_config(True, True, True)
            orientation_raw = self.sense.get_orientation_degrees()
            accelerometer_data = self.sense.get_accelerometer_raw()
            orientation = "Roll: " + str(round(orientation_raw["roll"], 2)) + ", Pitch: " + str(round(orientation_raw["pitch"], 2)) + ", Yaw: " + str(round(orientation_raw["yaw"], 2))
            compass = str(round(self.sense.compass, 2)) + " Degrees (0 being North)"
            accelerometer = "X: " + str(round(accelerometer_data["x"], 2)) + ", Y: " + str(round(accelerometer_data["y"], 2)) + ", Z: " + str(round(accelerometer_data["z"], 2))
        else:
            orientation = "No Data"
            compass = "No Data"
            accelerometer = "No Data"

        if self.components[1][1] is True:
            serial.serial(direction = "send", message = "T")
            self.sleep(0.1)
            distance = serial.serial().rstrip("\n") + " mm"
        else: distance = "No Data"

        if self.components[2][0] is True:
            serial.serial(direction = "send", message = "*")
            self.sleep(0.1)
            voltage = serial.serial().rstrip("\n") + " V"
        else: voltage = "No Data"

        timestamp = basics.make_timestamp()
        print("[INFO]: Done!")
        return "Telem. Timestamp: " + timestamp + "\nOrientation: " + orientation \
               + "\nCompass: " + compass + "\nAcceleration: " + accelerometer + "\nDistance Ahead: " + distance \
               + "\nBattery Voltage" + voltage
