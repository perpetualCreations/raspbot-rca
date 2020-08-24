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
    import comms
    import basics
    from ast import literal_eval
    from os import getcwd
except ImportError as ImportErrorMessage:
    print("[NAV][FAIL]: Import failed!")
    print(ImportErrorMessage)
except ImportWarning as ImportWarningMessage:
    print("[NAV][FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
pass

nav_instructions = None
nav_instruction_line = None

components = [[None], [None, None, None], [None], [None, None]] # components list, overwritten by __init__

nav_telemetry_text = None # TODO figure out what this is.
