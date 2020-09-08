"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multiprocessing, and editing configs.
Made by perpetualCreations

Handles reboot, restart, and shutdown.
"""

from basics import objects, basics

def restart():
    """
    Restarts application.
    :return: none.
    """
    print("[INFO]: Starting new instance of application...")
    objects.Popen("python main.py")
    basics.exit(0)
pass

def shutdown():
    """
    Shuts down bot.
    :return: none.
    """
    objects.call("sudo shutdown now", shell = True)
    basics.exit(0)
pass

def reboot():
    """
    Reboots bot.
    :return: none.
    """
    objects.call("sudo reboot now", shell = True)
    basics.exit(0)
pass
