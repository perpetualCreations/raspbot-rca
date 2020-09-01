"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multiprocessing, and editing configs.
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through basics.objects.
"""

try:
    import multiprocessing, sys, configparser
    from time import gmtime, strftime
    from subprocess import call, Popen
except ImportError as ImportErrorMessage:
    print("[FAIL]: Import failed!")
    print(ImportErrorMessage)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
pass

log_file_handle = None # overwritten by basics module's log_init()
origin_stdout = None # overwritten by basics module's log_init()
