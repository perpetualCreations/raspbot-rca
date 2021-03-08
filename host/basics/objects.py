"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multithreading, and editing configs.
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through basics.objects.
"""

try:
    import threading, sys, configparser, serial
    from time import gmtime, strftime
    from subprocess import call, Popen
    from ast import literal_eval
    from basics import basics
    from time import sleep
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

serial_connection = serial.Serial(timeout = 5)
serial_connection.port = "/dev/ttyACM0"

serial_lock = False # bool, if True new serial operations cannot be made until changed back to False

restart_lock = False # bool, restart_shutdown.restart() checks if this is False, if True the call to the function is ignored, it will only execute if False
                     # this also exists because for some reason, restart() is getting called twice and instead of being responsible and finding out why, I decided to just throw in a lock variable
