"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
nav.py module, contains navigation functions
Made by Taian Chen
"""

print("[INFO]: Initiating nav module...")

from nav import edit, gui, nav, objects

config_parse_load = objects.configparser.ConfigParser()

try:
    config_parse_load.read(objects.getcwd().strip("comms") + "hardware.cfg")
    objects.components[0][0] = objects.literal_eval(config_parse_load["HARDWARE"]["cam"])
    objects.components[1][0] = objects.literal_eval(config_parse_load["HARDWARE"]["sensehat"])
    objects.components[1][1] = objects.literal_eval(config_parse_load["HARDWARE"]["distance"])
    objects.components[1][2] = objects.literal_eval(config_parse_load["HARDWARE"]["dust"])
    objects.components[2][0] = objects.literal_eval(config_parse_load["HARDWARE"]["charger"])
    objects.components[3][0] = objects.literal_eval(config_parse_load["HARDWARE"]["arm"])
    objects.components[3][1] = objects.literal_eval(config_parse_load["HARDWARE"]["arm_cam"])
except objects.configparser.Error as ce:
    print("[FAIL]: Failed to load configurations! See below for details.")
    print(ce)
except KeyError as ke:
    print("[FAIL]: Failed to load configurations! Configuration file is corrupted or has been edited incorrectly.")
    print(ke)
except FileNotFoundError as nf:
    print("[FAIL]: Failed to load configurations! Configuration file is missing.")
pass

print("[INFO]: Initiating of nav module complete!")
