"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multithreading, and editing configs.
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through basics.objects.
"""

try:
    import threading, sys, configparser
    from time import gmtime, strftime
    from tkinter import messagebox
    from ast import literal_eval
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

log_file_handle = None # overwritten by basics module's log_init()
origin_stdout = None # overwritten by basics module's log_init()
