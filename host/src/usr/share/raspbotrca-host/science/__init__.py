"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
science module, for collecting sensor data
Made by perpetualCreations
"""

print("[INFO]: Initiating science module...")

try:
    from time import sleep
    from basics import basics, serial, restart_shutdown
    from gpiozero import CPUTemperature
except ImportError as ImportErrorMessage:
    print("[FAIL]: Imports failed! See below.")
    print(ImportErrorMessage)
    basics.exit(1)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(ImportWarningMessage)
    basics.exit(1)
pass

print("[INFO]: Initiation of science complete!")

class science:
    """
    Class for sensor data collection.
    """
    def __init__(self) -> None:
        self.components = basics.load_hardware_config()
        if self.components[0][0] is True:
            import sense_hat
            self.sense = sense_hat.SenseHat()
        else: self.sense = None

    def get(self) -> str:
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
        if self.components[0][0] is True:
            print("[INFO]: Collecting data from sensors on SenseHAT...")
            self.sense.set_imu_config(True, True, True)
            orientation_raw = self.sense.get_orientation_degrees()
            compass = round(self.sense.compass, 2)
            accelerometer_data = self.sense.get_accelerometer_raw()
            print("[INFO]: Collection completed.")
            temperature_raw = self.sense.get_temperature()
            temperature = str(round(temperature_raw - ((CPUTemperature() - temperature_raw)/5.466), 2)) + "C" # calibration ref, https://github.com/initialstate/wunderground-sensehat/wiki/Part-3.-Sense-HAT-Temperature-Correction
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
        if self.components[0][2] is True:
            dust_lpo = serial.serial(message = "DUST LPO") + " (μs)"
            dust_ratio = serial.serial(message = "DUST RATIO")
            dust_concentration = serial.serial(message = "DUST CONC") + " (pcs/L)"
        else:
            print("[INFO]: No data for dust sensor.")
            dust_lpo = "No Data"
            dust_ratio = "No Data"
            dust_concentration = "No Data"

        print("[INFO]: Done!")
        return "Timestamp: " + basics.make_timestamp() + "\nTemperature: " + temperature + "\nAtm. Pressure: " + pressure \
               + "\nAtm. Humidity: " + humidity + "\nOrientation: " + "\n" + orientation + \
               "\nCompass: " + compass_str + "\nAcceleration: " + accelerometer + "\nDust LPO Time: " \
               + dust_lpo + "\nDust LPO/Observation Time Ratio: " + dust_ratio + "\nDust Concentration: " \
               + dust_concentration
