"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# Made by Taian Chen
"""

try:
    print("[INFO]: Starting imports...")
    import time
    import os
    from subprocess import call
    from subprocess import Popen
    import serial
    import tkinter
    from time import sleep
except ImportError as e:
    time = None
    os = None
    serial = None
    tkinter = None
    call = None
    Popen = None
    sleep = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class Raspbot:
    def __init__(self):
        """Initiation function of Raspbot RCA."""
        print("[INFO]: Starting Raspbot RC Application...")
        print("[INFO]: Retrieving current directory.")
        print("[INFO]: Starting other modules...")
        print("[INFO]: Starting module cmdline...")
        Popen("sudo python3 cmdline.py", shell = True)
        print("[INFO]: Starting module science...")
        Popen("sudo python3 science.py", shell = True)
        print("[INFO]: Starting module vitals-gui...")
        Popen("sudo python3 vitals-gui.py", shell = True)
        print("[INFO]: Starting module nav...")
        Popen("sudo python3 nav.py", shell = True)
        print("[INFO]: Starting module led_graphics...")
        Popen("sudo python3 led_graphics.py", shell = True)
        print("[INFO]: Starting live view from Pyimagesearch.")
        Popen("sudo python3 tkinter-photo-booth/photo_booth.py", shell = True)
    pass
pass

r = Raspbot()
