"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
science module, for collecting sensor data
Made by perpetualCreations
"""

print("[INFO]: Initiating science module...")

try:
    from time import sleep
    from basics import basics, serial
except ImportError as e:
    print("[FAIL]: Imports failed! See below.")
    print(e)
    basics.exit(1)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
    basics.exit(1)
pass

print("[INFO]: Initiation of science complete!")

class science:
    """
    Class for sensor data collection.
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
        :return: formatted sensor data as: "Timestamp: " + timestamp + "\n" + "Temperature: " + temperature + "\n"\
                       + "Atm. Pressure: " + pressure + "\n" + "Atm. Humidity: " + humidity + "\n"\
                       + "Orientation: " + "\n" + orientation + "\n" + "Compass: " + compass_str + "\n" + "Acceleration: " \
                       + accelerometer + "\n" + "Dust LPO Time: " + dust_lpo + "\n" \
                       + "Dust LPO/Observation Time Ratio: " + dust_ratio + "\n" + "Dust Concentration: " \
                       + dust_concentration + "\n" + "ToF Distance: " + distance
        """
        print("[INFO]: Starting data collection...")
        if self.components[1][0] is True:
            print("[INFO]: Collecting data from sensors on SenseHAT...")
            self.sense.set_imu_config(True, True, True)
            orientation_raw = self.sense.get_orientation_degrees()
            compass = round(self.sense.compass, 2)
            accelerometer_data = self.sense.get_accelerometer_raw()
            print("[INFO]: Collection completed.")
            temperature = str(round(self.sense.get_temperature(), 2)) + "C"
            pressure = str(round(self.sense.get_pressure(), 2)) + " Millibars"
            humidity = str(round(self.sense.get_humidity(), 2)) + "% Humidity"
            orientation = "Roll: " + str(round(orientation_raw["roll"], 2)) + ", Pitch: " + str(round(orientation_raw["pitch"], 2)) + ", Yaw: " + str(round(orientation_raw["yaw"], 2))
            compass_str = str(compass) + " Degrees (0 being North)"
            accelerometer = "X: " + str(round(accelerometer_data["x"], 2)) + ", Y: " + str(round(accelerometer_data["y"], 2)) + ", Z: " + str(round(accelerometer_data["z"], 2))
        else:
            temperature = "No Data"
            pressure = "No Data"
            humidity = "No Data"
            orientation = "No Data"
            compass_str = "No Data"
            accelerometer = "No Data"

        print("[INFO]: Collecting data from serial...")
        if self.components[1][2] is True:
            serial.serial(direction = "send", message = "D")
            self.sleep(0.1)
            dust_lpo = serial.serial().rstrip("\n") + " (μs)"
            dust_ratio = serial.serial().rstrip("\n")
            dust_concentration = serial.serial().rstrip("\n") + " (pcs/L)"
        else:
            print("[INFO]: No data for dust sensor.")
            dust_lpo = "No Data"
            dust_ratio = "No Data"
            dust_concentration = "No Data"

        timestamp = basics.make_timestamp()
        print("[INFO]: Done!")
        return "Timestamp: " + timestamp + "\nTemperature: " + temperature + "\nAtm. Pressure: " + pressure \
               + "\nAtm. Humidity: " + humidity + "\nOrientation: " + "\n" + orientation + \
               "\nCompass: " + compass_str + "\nAcceleration: " + accelerometer + "\nDust LPO Time: " \
               + dust_lpo + "\nDust LPO/Observation Time Ratio: " + dust_ratio + "\nDust Concentration: " \
               + dust_concentration
