"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics.py module, contains basic application functions such as exiting client software, multithreading, and editing configs.
Made by perpetualCreations

Host version of basics module.
"""

print("[INFO]: Initiating basics module...")

from basics import basics, objects, process, restart_shutdown, serial

try:
    try: objects.serial_connection.open()
    except objects.serial.serialposix.SerialException as SerialExceptionMessage:
        print("[FAIL]: Failed to initialize serial!")
        print(SerialExceptionMessage)
    pass
except AttributeError: # compatibility for Windows, this is an extremely dirty bodge
    try: objects.serial_connection.open()
    except objects.serial.serialwin32.SerialException as SerialExceptionMessage:
        print("[FAIL]: Failed to initialize serial!")
        print(SerialExceptionMessage)
    pass
pass

objects.sleep(1.5) # delays the end of initialization for serial to warm up

print("[INFO]: Initiation of basics complete!")
