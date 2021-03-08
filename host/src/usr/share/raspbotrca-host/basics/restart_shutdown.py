"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multithreading, and editing configs.
Made by perpetualCreations

Handles reboot, restart, and shutdown.
"""

from basics import objects, basics

def restart() -> None:
    """
    Restarts application.
    :return: None
    """
    if objects.restart_lock is True:
        print("[INFO]: Restart was called more than once. Ignoring excess call.")
        return None
    pass
    objects.restart_lock = True
    print("[INFO]: Restarting. Starting new instance of application...")
    objects.Popen("python3 main.py", shell = True)
    basics.exit(0)
pass

def shutdown() -> None:
    """
    Shuts down bot.
    :return: None
    """
    objects.call("sudo shutdown now", shell = True)
    basics.exit(0)
pass

def reboot() -> None:
    """
    Reboots bot.
    :return: None
    """
    objects.call("sudo reboot now", shell = True)
    basics.exit(0)
pass
