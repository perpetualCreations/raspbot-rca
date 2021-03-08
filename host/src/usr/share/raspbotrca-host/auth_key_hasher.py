"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
# Authentication Key Hashing Tool, allows for users to hash a chosen auth key and automatically put the output into the host configuration.
# Made by perpetualCreations
"""

import configparser
from Cryptodome.Hash import SHA3_512

generation = SHA3_512.new(input("Please enter your chosen auth code: ").encode(encoding = "ascii", errors = "replace")).hexdigest()

config_parse = configparser.ConfigParser()
config_parse.read("comms/comms.cfg")
config_parse["ENCRYPT"]["auth"] = generation
with open("../../../comms/comms.cfg", "w") as config_write:
    config_parse.write(config_write)
pass
config_write.close()
print("[INFO]: Generated hash was: " + generation)
print("[INFO]: Done.")
