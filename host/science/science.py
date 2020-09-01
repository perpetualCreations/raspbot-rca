"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
science module, for collecting sensor data, made for RFP Enceladus Project with Raspbot
Made by perpetualCreations

Main module for collecting sensor data.
"""

from science import objects

def get():
    """
    Calls SenseHAT Python integration package and Arduino PySerial for data inputs and collects output into self.content for displaying.
    :return: formatted sensor data as: "Timestamp: " + timestamp_str + "\n" + "Temperature: " + temperature_str + "\n"\
                   + "Atm. Pressure: " + pressure_str + "\n" + "Atm. Humidity: " + humidity_str + "\n"\
                   + "Orientation: " + "\n" + orientation + "\n" + "Compass: " + compass_str + "\n" + "Acceleration: " \
                   + accelerometer + "\n" + "Dust LPO Time: " + dust_lpo + "\n" \
                   + "Dust LPO/Observation Time Ratio: " + dust_ratio + "\n" + "Dust Concentration: " \
                   + dust_concentration + "\n" + "ToF Distance: " + distance
    """
    print("[INFO]: Starting data collection...")
    print("[INFO]: Collecting data from sensors on SenseHAT...")
    temperature_data_raw = objects.sense.get_temperature_from_humidity()
    temperature_data = round(temperature_data_raw, 2)
    pressure_data_raw = objects.sense.get_pressure()
    pressure_data = round(pressure_data_raw, 2)
    humidity_data_raw = objects.sense.get_humidity()
    humidity_data = round(humidity_data_raw, 2)
    objects.sense.set_imu_config(True, True, True)
    orientation_raw = objects.sense.get_orientation_degrees()
    compass_raw = objects.sense.compass
    compass = round(compass_raw, 2)
    accelerometer_data = objects.sense.get_accelerometer_raw()
    print("[INFO]: Collection completed.")
    temperature_str = str(temperature_data) + "C"
    pressure_str = str(pressure_data) + " Millibars"
    humidity_str = str(humidity_data) + "% Humidity"
    orientation_roll = str(round(orientation_raw["roll"], 2))
    orientation_pitch = str(round(orientation_raw["pitch"], 2))
    orientation_yaw = str(round(orientation_raw["yaw"], 2))
    orientation = "Roll: " + orientation_roll + ", Pitch: " + orientation_pitch + ", Yaw: " + orientation_yaw
    compass_str = str(compass) + " Degrees (0 being North)"
    accelerometer_x = str(round(accelerometer_data["x"], 2))
    accelerometer_y = str(round(accelerometer_data["y"], 2))
    accelerometer_z = str(round(accelerometer_data["z"], 2))
    accelerometer = "X: " + accelerometer_x + ", Y: " + accelerometer_y + ", Z: " + accelerometer_z
    print("[INFO]: Starting serial connection with Grove Arduino integration...")
    try:
        arduino = objects.serial.Serial('/dev/ttyACM0', timeout = 5)
    except objects.serial.serialutil.SerialException as se:
        print("[FAIL]: Failed to create connection with Grove Arduino integration! See details below.")
        print(se)
        return None
    pass
    print("[INFO]: Collecting data from serial.")
    arduino.write(b"D")
    objects.sleep(0.1)
    grove_sensor_dust_lpo_data = arduino.readline()
    dust_lpo = grove_sensor_dust_lpo_data.decode(encoding = "utf-8", errors = "replace")
    dust_lpo = dust_lpo.rstrip("\n") + " (μs)"
    grove_sensor_dust_ratio_data = arduino.readline()
    dust_ratio = grove_sensor_dust_ratio_data.decode(encoding = "utf-8", errors = "replace")
    dust_ratio = dust_ratio.rstrip("\n")
    grove_sensor_dust_concentration_data = arduino.readline()
    dust_concentration = grove_sensor_dust_concentration_data.decode(encoding = "utf-8", errors = "replace")
    dust_concentration = dust_concentration.rstrip("\n") + " (pcs/L)"
    arduino.write(b"T")
    objects.sleep(0.1)
    grove_sensor_distance_data = arduino.readline()
    distance = grove_sensor_distance_data.decode(encoding = "utf-8", errors = "replace")
    distance = distance.rstrip("\n") + " (mm)"
    # NOTICE: Grove Light Sensor is not connected on official build, uncomment and configure in Arduino Instructions at your own will.
    # grove_sensor_light_data = arduino.readline()
    # light = grove_sensor_light_data.decode(encoding = "utf-8", errors = "replace")
    # light = light.rstrip("\n")
    print("[INFO]: Generating timestamps...")
    timestamp = objects.strftime("%b%d%Y%H%M%S"), objects.gmtime()
    timestamp_output = timestamp[0]
    timestamp_str = str(timestamp_output)
    print("[INFO]: Done!")
    return "Timestamp: " + timestamp_str + "\n" + "Temperature: " + temperature_str + "\n"\
                   + "Atm. Pressure: " + pressure_str + "\n" + "Atm. Humidity: " + humidity_str + "\n"\
                   + "Orientation: " + "\n" + orientation + "\n" + "Compass: " + compass_str + "\n" + "Acceleration: " \
                   + accelerometer + "\n" + "Dust LPO Time: " + dust_lpo + "\n" \
                   + "Dust LPO/Observation Time Ratio: " + dust_ratio + "\n" + "Dust Concentration: " \
                   + dust_concentration + "\n" + "ToF Distance: " + distance
pass
