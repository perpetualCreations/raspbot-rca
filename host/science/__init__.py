"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
science module, for collecting sensor data, made for RFP Enceladus Project with Raspbot
Made by perpetualCreations
"""

print("[INFO]: Initiating science module...")

from science import objects, science

config_parse_load.read("hardware.cfg")
objects.components[0][0] = objects.literal_eval(config_parse_load["HARDWARE"]["cam"])
objects.components[1][0] = objects.literal_eval(config_parse_load["HARDWARE"]["sensehat"])
objects.components[1][1] = objects.literal_eval(config_parse_load["HARDWARE"]["distance"])
objects.components[1][2] = objects.literal_eval(config_parse_load["HARDWARE"]["dust"])
objects.components[2][0] = objects.literal_eval(config_parse_load["HARDWARE"]["charger"])
objects.components[3][0] = objects.literal_eval(config_parse_load["HARDWARE"]["arm"])
objects.components[3][1] = objects.literal_eval(config_parse_load["HARDWARE"]["arm_cam"])

print("[INFO]: Initiation of science complete!")
