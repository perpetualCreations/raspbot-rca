"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
science module, for collecting sensor data, made for RFP Enceladus Project with Raspbot
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through science.objects.
"""

try:
    import tkinter, serial
    import sense_hat
    from time import gmtime, strftime, sleep
except ImportError as e:
    sense_hat = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
    exit(1)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

sense = sense_hat.SenseHat()
