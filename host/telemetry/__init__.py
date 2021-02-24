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
    def __init__(self) -> None:
        self.components = basics.load_hardware_config()
        if self.components[1][0] is True:
            import sense_hat
            self.sense = sense_hat.SenseHat()
        else: self.sense = None

    def get(self, no_serial: bool = False) -> str:
        """
        Calls SenseHAT Python integration package and Arduino PySerial for data inputs and returns formatted output.
        :param no_serial: bool, if True no serial data will be collected
        :return: str, multi-line
        """
        if self.components[1][0] is True:
            self.sense.set_imu_config(True, True, True)
            orientation_raw = self.sense.get_orientation_degrees()
            accelerometer_data = self.sense.get_accelerometer_raw()
            roll_raw = round(orientation_raw["roll"], 2)
            if (roll_raw - 90) < 0: roll = 360 - abs(roll_raw - 90)
            else: roll = roll_raw - 90
            orientation = "Roll: " + str(roll) + ", Pitch: " + str(round(orientation_raw["pitch"], 2)) + ", Yaw: " + str(round(orientation_raw["yaw"], 2)) # subtract 90 deg from roll for mounting position offset
            compass = str(round(self.sense.compass, 2))
            accelerometer = "X: " + str(round(accelerometer_data["x"], 2)) + ", Y: " + str(round(accelerometer_data["y"], 2)) + ", Z: " + str(round(accelerometer_data["z"], 2))
        else:
            orientation = "No Data"
            compass = "No Data"
            accelerometer = "No Data"

        if self.components[1][1] is True and no_serial is False: distance = serial.serial(message = "T") + " mm"
        else: distance = "No Data"

        voltage_warn = ""

        if self.components[2][0] is True and no_serial is False:
            voltage = str(serial.voltage()) + " V"
            try:
                if float(voltage.rstrip(" V")) <= 9.5: voltage_warn = "WARNING - BATTERY VOLTAGE TOO LOW, DOCK AND CHARGE BATTERY"
            except ValueError:
                voltage_warn = "\nArduino isn't responding..."
                voltage = "NaN"
            pass
        else: voltage = "No Data"

        timestamp = basics.make_timestamp(log_suppress = True)
        return "Telem. Timestamp: " + timestamp + "\nOrientation: " + orientation \
               + "\nCompass: " + compass + "\nAcceleration: " + accelerometer + "\nDistance Ahead: " + distance \
               + "\nBattery Voltage: " + voltage + voltage_warn
