"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
science module, for collecting sensor data, made for RFP Enceladus Project with Raspbot
Made by perpetualCreations
"""

print("[INFO]: Initiating science module...")

try:
    import tkinter, serial, configparser
    from time import gmtime, strftime, sleep
    from basics import basics
    from ast import literal_eval
except ImportError as e:
    print("[FAIL]: Imports failed! See below.")
    print(e)
    basics.exit(1)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
    basics.exit(1)
pass

components = [[None], [None, None, None], [None], [None, None]]

sense_hat = None

config_parse_load = configparser.ConfigParser()

try:
    config_parse_load.read("hardware.cfg")
    components[0][0] = literal_eval(config_parse_load["HARDWARE"]["cam"])
    components[1][0] = literal_eval(config_parse_load["HARDWARE"]["sensehat"])
    components[1][1] = literal_eval(config_parse_load["HARDWARE"]["distance"])
    components[1][2] = literal_eval(config_parse_load["HARDWARE"]["dust"])
    components[2][0] = literal_eval(config_parse_load["HARDWARE"]["charger"])
    components[3][0] = literal_eval(config_parse_load["HARDWARE"]["arm"])
    components[3][1] = literal_eval(config_parse_load["HARDWARE"]["arm_cam"])
except objects.configparser.Error as ce:
    print("[FAIL]: Failed to load configurations! See below for details.")
    print(ce)
    objects.basics.exit(1)
except KeyError as ke:
    print("[FAIL]: Failed to load configurations! Configuration file is corrupted or has been edited incorrectly.")
    print(ke)
    objects.basics.exit(1)
except FileNotFoundError:
    print("[FAIL]: Failed to load configurations! Configuration file is missing.")
    objects.basics.exit(1)
pass

if objects.components[1][0] is True:
    import sense_hat
    sense = sense_hat.SenseHat()
pass

print("[INFO]: Initiation of science complete!")

def get():
    """
    Calls SenseHAT Python integration package and Arduino PySerial for data inputs and collects output into self.content for displaying.
    :return: formatted sensor data as: "Timestamp: " + timestamp + "\n" + "Temperature: " + temperature + "\n"\
                   + "Atm. Pressure: " + pressure + "\n" + "Atm. Humidity: " + humidity + "\n"\
                   + "Orientation: " + "\n" + orientation + "\n" + "Compass: " + compass_str + "\n" + "Acceleration: " \
                   + accelerometer + "\n" + "Dust LPO Time: " + dust_lpo + "\n" \
                   + "Dust LPO/Observation Time Ratio: " + dust_ratio + "\n" + "Dust Concentration: " \
                   + dust_concentration + "\n" + "ToF Distance: " + distance
    """
    print("[INFO]: Starting data collection...")
    if objects.components[1][0] is True:
        print("[INFO]: Collecting data from sensors on SenseHAT...")
        objects.sense.set_imu_config(True, True, True)
        orientation_raw = objects.sense.get_orientation_degrees()
        compass = round(objects.sense.compass, 2)
        accelerometer_data = objects.sense.get_accelerometer_raw()
        print("[INFO]: Collection completed.")
        temperature = str(round(objects.sense.get_temperature_from_humidity(), 2)) + "C"
        pressure = str(round(objects.sense.get_pressure(), 2)) + " Millibars"
        humidity = str(round(objects.sense.get_humidity(), 2)) + "% Humidity"
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
    print("[INFO]: Starting serial connection with Arduino...")
    try:
        arduino = objects.serial.Serial('/dev/ttyACM0', timeout = 5)
    except objects.serial.serialutil.SerialException as se:
        print("[FAIL]: Failed to create connection with Arduino! See details below.")
        print(se)
        return None
    pass
    print("[INFO]: Collecting data from serial...")
    if objects.components[1][2] is True:
        arduino.write(b"D")
        objects.sleep(0.1)
        dust_lpo = arduino.readline().decode(encoding = "utf-8", errors = "replace").rstrip("\n") + " (μs)"
        dust_ratio = arduino.readline().decode(encoding = "utf-8", errors = "replace").rstrip("\n")
        dust_concentration = arduino.readline().decode(encoding = "utf-8", errors = "replace").rstrip("\n") + " (pcs/L)"
    else:
        print("[INFO]: No data for dust sensor.")
        dust_lpo = "No Data"
        dust_ratio = "No Data"
        dust_concentration = "No Data"
    pass
    if objects.components[1][1] is True:
        arduino.write(b"T")
        objects.sleep(0.1)
        grove_sensor_distance_data = arduino.readline()
        distance = grove_sensor_distance_data.decode(encoding = "utf-8", errors = "replace")
        distance = distance.rstrip("\n") + " (mm)"
    else:
        print("[INFO]: No data for ToF sensor.")
        distance = "No Data"
    pass
    print("[INFO]: Generating timestamps...")
    timestamp = str((objects.strftime("%b%d%Y%H%M%S"), objects.gmtime())[0])
    print("[INFO]: Done!")
    return "Timestamp: " + timestamp + "\n" + "Temperature: " + temperature + "\n"\
                   + "Atm. Pressure: " + pressure + "\n" + "Atm. Humidity: " + humidity + "\n"\
                   + "Orientation: " + "\n" + orientation + "\n" + "Compass: " + compass_str + "\n" + "Acceleration: " \
                   + accelerometer + "\n" + "Dust LPO Time: " + dust_lpo + "\n" \
                   + "Dust LPO/Observation Time Ratio: " + dust_ratio + "\n" + "Dust Concentration: " \
                   + dust_concentration + "\n" + "ToF Distance: " + distance
pass
