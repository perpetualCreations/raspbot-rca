"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, contains functions for socket communications.
Made by perpetualCreations

Host version of comms module.

To setup the communications protocol for host, connect_accept must be invoked to start listening for connections.
"""

print("[INFO]: Initiating comms module...")

from comms import interface, acknowledge, objects, camera_capture, disconnect, telemetry

config_parse_load = objects.configparser.ConfigParser()
try:
    config_parse_load.read("comms/comms.cfg")
    objects.key = (objects.MD5.new((config_parse_load["ENCRYPT"]["key"]).encode(encoding = "ascii", errors = "replace")).hexdigest()).encode(encoding = "ascii", errors = "replace") # this was previously split into a multi-liner instead of an one-liner. why? i'm not sure why there's an extra encode either
    objects.hmac_key = config_parse_load["ENCRYPT"]["hmac_key"]
    objects.auth = (config_parse_load["ENCRYPT"]["auth"]).encode(encoding = "ascii", errors = "replace") # not sure why there's an extra encode here either, the auth message sent to host should be converted into a byte string anyways
    objects.port = int(config_parse_load["NET"]["port"])
    objects.cam_port = int(config_parse_load["NET"]["cam_port"])
    objects.telemetry_port = int(config_parse_load["NET"]["telemetry_port"])
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
    print(nf)
    objects.basics.exit(1)
pass

objects.components = objects.basics.load_hardware_config()

objects.host = objects.socket.gethostname() + ".local"

print("[INFO]: Initiation of comms complete!")
