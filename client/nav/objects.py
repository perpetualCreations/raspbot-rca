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
    import comms # if I import comms from main, it doesn't use the current main module instance, it starts a new one
    import basics
    from ast import literal_eval
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
