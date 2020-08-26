"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Made by Taian Chen

Startup script.
Currently it's rather excessive and unnecessary, it only handles whether to run with or without a console output.
In future releases, it will also handle logging.
"""

from subprocess import call
from ast import literal_eval
import configparser
from platform import system
from tkinter import messagebox
import tkinter
import sys

root = tkinter.Tk()
root.withdraw()

config_parse_load = configparser.ConfigParser()
gui_hide_console = False

try:
    config_parse_load.read("main.cfg")
    gui_hide_console = literal_eval(config_parse_load["GUI"]["hide_console"])
except configparser.Error as ce:
    messagebox.showerror("Raspbot RCA: Startup Error", "Unable to load configurations. Check configuration files!")
    sys.exit(1)
except KeyError as ke:
    messagebox.showerror("Raspbot RCA: Startup Error", "Unable to load configurations. Check configuration files!")
    sys.exit(1)
except FileNotFoundError as nf:
    messagebox.showerror("Raspbot RCA: Startup Error", "Unable to load configurations. See if configuration file exists, it appears to be missing!")
    sys.exit(1)
pass

if system() == "Windows":
    if gui_hide_console is True:
        call("pythonw main.py", shell = True)
    else:
        call("python main.py", shell = True)
    pass
else:
    # assumes you are running a Linux system.
    if gui_hide_console is True:
        call("python main.py > /dev/null 2>&1", shell = True)
    else:
        call("python main.py", shell = True)
    pass
pass

# below here is where logging options will be added.
