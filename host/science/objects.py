"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
science module, for collecting sensor data, made for RFP Enceladus Project with Raspbot
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through science.objects.
"""

try:
    import tkinter
    from sense_hat import SenseHat
    from time import gmtime
    from time import strftime
    import serial
    from time import sleep
except ImportError as e:
    tkinter = None
    gmtime = None
    strftime = None
    SenseHat = None
    serial = None
    sleep = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
    exit(1)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

