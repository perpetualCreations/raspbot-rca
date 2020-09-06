"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
science module, for collecting sensor data, made for RFP Enceladus Project with Raspbot
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through science.objects.
"""

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

components = [[None], [None, None, None], [None], [None, None]] # components list, overwritten by __init__

sense_hat = None # module placeholder, actually imported from __init__ instead so hardware check runs first
