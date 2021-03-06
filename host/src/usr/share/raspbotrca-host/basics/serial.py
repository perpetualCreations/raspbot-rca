"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multithreading, and editing configs.
Made by perpetualCreations

Serial communications function contained within this module.
Other wrapper functions that make use of serial are included as well.
"""

from basics import objects
from typing import Union

def serial(port:str = "/dev/ttyACM0", direction:str = "receive", message:Union[None, str, bytes] = None) -> Union[None, str]:
    """
    Sends or receives serial communications to the Arduino integration.
    ===
    Dear Dev(s),
    If you're trying to run a unit test using this function on Windows, please set the port to 'COM<X>'.
    Also please ignore the "could not open port" message in console.
    Regards, PC
    ===
    :param port: str, the port that the Arduino is connected to, default set to /dev/ttyACM0.
    :param direction: str, whether to expect to receive or send, default set to receive.
    :param message: str, message to send, or if receiving leave as None, default set to None automatically, can be bytestring or normal string.
    :return: if receiving, decoded string, if sending or invalid direction, None
    """
    if port != objects.serial_connection.port:
        while objects.serial_lock is True: pass
        objects.serial_lock = True
        if objects.serial_connection.is_open is True: objects.serial_connection.close()
        objects.serial_connection.port = port
        objects.serial_connection.open()
        objects.sleep(4)
        objects.serial_lock = False
    pass
    if message is None: return None
    if isinstance(message, bytes): message = message.decode(encoding = "utf-8", errors = "replace")
    try:
        while objects.serial_lock is True: pass
        objects.serial_lock = True
        for x in range(0, len(message)): objects.serial_connection.write(message[x].encode(encoding = "ascii", errors = "replace"))
        objects.serial_connection.write(b"\x0A") # hexcode for newline character, signals the end of the message and for accumulator dump
        if direction == "receive":
            response = objects.serial_connection.read_until(b"\x0A").rstrip(b"\n").decode(encoding = "utf-8", errors = "replace")
            objects.serial_lock = False
            return response
        else:
            objects.serial_lock = False
            return None
    except objects.serial.serialposix.SerialException as SerialExceptionMessage:
        print("[FAIL]: Unable to access serial!")
        print(SerialExceptionMessage)
        objects.serial_lock = False
        if direction == "receive": return "ERROR"
        else: return None
    pass
pass

def nav_timer(nav_run_time: int) -> None:
    """
    Navigation timer for multithreading, waits for given number of seconds and then sends arrest command to Arduino, ending the operation.
    :param nav_run_time: amount of time to run motors as an integer value.
    :return: None
    """
    objects.sleep(nav_run_time)
    serial(direction = "send", message = b"A")
pass

def nav_adjust_speed(speed: int) -> None:
    """
    Changes motor speed through serial, with vetting before executing user input.
    @param speed: int, must be in range 0-255 or return None with no execution, signals motor speed
    @return: None
    """
    if speed not in range(0, 256): return None
    print("[INFO]: Changing motor speed to " + str(speed) + "/255.")
    serial(direction = "send", message = "MS " + str(speed))
pass

def dock() -> None:
    """
    Docks Raspbot.

    This means:
    A. The user must plug in the external power supply to power the Raspi.
    B. The user may also charge the lithium-polymer battery, through the battery's balance connector.
    C. The motors will be disabled until undocked.

    This entails:
    A. The relay controlling the power supply for Raspi is to be switched to external, which is normally closed.
    B. The MOSFET switch for the motors is to be opened, disabling them.
    """
    objects.serial.serial(direction = "send", message = ")")
    objects.serial.serial(direction = "send", message = "<")
    objects.dock_status = True
pass

def undock() -> None:
    """
    Undocks Raspbot.

    This means:
    A. The user must disconnect the battery balance connector to stop charging.
      1. The battery must have sufficient charge.
    B. The user may disconnect the external power supply to power the Raspi AFTER the relay has switched.
    C. The motors will be re-enabled after undocking.

    This entails:
    A. The relay controlling the power supply for Raspi is to be switched to internal, which is normally open.
      1. This must be done immediately after the balance connector has been disconnected, and before the external power supply has been disconnected.
      2. If the relay is switched to internal with the external supply disconnected, everything will be unpowered, and shutdown.
    B. The MOSFET switch for motor is to be closed, enabling them.
      1. Because the motors are powered, any connectors still connected must be disconnected, for safety.
    """
    if float(objects.serial.serial(direction = "receive", message = "*")) <= 9: return None # TODO add proper error handle
    objects.serial.serial(direction = "send", message = "(")
    objects.serial.serial(direction = "send", message = ">")
    objects.dock_status = False
pass

def voltage() -> Union[float, str]:
    """
    Collects battery voltage through serial.
    :return: float, voltage
    """
    raw = serial(message = "*")
    if raw == "ERROR": return "NaN"
    else: return float(raw)
pass

def arrest() -> None:
    """
    Stop all motor movement.
    @return: None
    """
    serial(direction = "send", message = "A")
pass
