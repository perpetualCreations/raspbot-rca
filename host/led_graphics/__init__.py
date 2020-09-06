"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1, revised for v1.2
led_graphics module, for controlling onboard LED matrix
Made by perpetualCreations

Host-only module.
"""

print("[INFO]: Initiating led_graphics module...")

from led_graphics import objects

config_parse_load = objects.configparser.ConfigParser()

try:
    config_parse_load.read("hardware.cfg")
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
    objects.basics.exit(1)
except KeyError as ke:
    print("[FAIL]: Failed to load configurations! Configuration file is corrupted or has been edited incorrectly.")
    print(ke)
    objects.basics.exit(1)
except FileNotFoundError as nf:
    print("[FAIL]: Failed to load configurations! Configuration file is missing.")
    objects.basics.exit(1)
pass

if objects.components[1][0] is True:
    import sense_hat
    objects.sense = sense_hat.SenseHat()
    objects.module_active = True
    from led_graphics import led_graphics, errors
else:
    led_graphics = None
    errors = None
pass

print("[INFO]: Initiation of led_graphics complete!")
