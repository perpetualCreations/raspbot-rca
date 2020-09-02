"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
nav.py module, contains navigation functions
Made by Taian Chen

Contains objects for module, including any package imports. Interact with these objects through nav.objects.
"""

try:
    import tkinter
    from tkinter import messagebox
    from platform import system
    from subprocess import call, Popen
    from time import sleep
    import configparser
    from main import comms # this is just utterly stupid. but it probably works. probably. i feel like theres a better way of doing this.
    import basics
    from ast import literal_eval
    from os import getcwd
    from basics import basics
except ImportError as ImportErrorMessage:
    print("[FAIL]: Import failed!")
    print(ImportErrorMessage)
    basics.exit(1)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
    basics.exit(1)
pass

nav_instructions = None
nav_instruction_line = None

components = [[None], [None, None, None], [None], [None, None]] # components list, overwritten by __init__

nav_telemetry_text = None
