"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
nav.py module, contains navigation functions
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through nav.objects.
"""

try:
    from basics import basics, serial
    import configparser
    from ast import literal_eval
    from comms import interface
except ImportError as ImportErrorMessage:
    print("[FAIL]: Import failed!")
    print(ImportErrorMessage)
    basics.exit(1)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
    basics.exit(1)
pass

components = [[None], [None, None, None], [None], [None, None]] # components list, overwritten by __init__
