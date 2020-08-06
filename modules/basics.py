"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics.py module, contains functions for shutting down and rebooting the bot along with other misc. functions such as editing configs.
Made by Taian Chen
"""

try:
    from sys import exit as app_end
except ImportError as ImportErrorMessage:
    app_end = None
    print("[NAV][FAIL]: Import failed!")
    print(ImportErrorMessage)
except ImportWarning as ImportWarningMessage:
    print("[NAV][FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
pass


class basics:
    def __init__(self):
        print("[BASICS][INFO]: Basics module loaded!")
    pass
    @staticmethod
    def exit(status):
        """
        Stops application.
        :return: none.
        """
        print("[INFO]: Stopping application...")
        app_end(status)
    pass
pass