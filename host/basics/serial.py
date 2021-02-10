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
    :param port: str, the port that the Arduino is connected to, default set to /dev/ttyACM0.
    :param direction: str, whether to expect to receive or send, default set to receive.
    :param message: str, message to send, or if receiving leave as None, default set to None automatically, can be bytestring or normal string.
    :return: if receiving, decoded string, if sending or invalid direction, None
    """
    if message is not None and isinstance(message, bytes): message = message.decode(encoding = "utf-8", errors = "replace")
    with objects.serial.Serial(port = port, timeout = 0) as connect:
        connect.flush()
        connect.readline()
        connect.timeout(2)
        if isinstance(message, bytes) is True: message = message.decode(encoding = "utf-8", errors = "replace")
        if direction == "receive": return connect.readline().rstrip(b"\n").decode(encoding = "utf-8", errors = "replace")
        elif direction == "send":
            for x in range(0, len(message)): connect.write(message[x].encode(encoding = "ascii", errors = "replace"))
            connect.write(b"\x0A") # hexcode for newline character, signals the end of the message and for accumulator dump
        else: return None
    pass
pass

def nav_timer(nav_run_time: int) -> None:
    """
    Navigation timer for multithreading, waits for given number of seconds and then sends arrest command to Arduino, ending the operation.
    :param nav_run_time: amount of time to run motors as an integer value.
    :return: None
    """
    sleep(nav_run_time)
    objects.interface.send(b"rca-1.2:nav_end")
    host.serial("/dev/ttyACM0", "send", b"A")
pass

def nav_adjust_speed(speed: int) -> None:
    """
    Changes motor speed through serial, with vetting before executing user input.
    @param speed:
    @return:
    """
    if speed not in range(0, 256): return None
    print("[INFO]: Changing motor speed to " + str(speed) + "/255.")
    serial(direction = "send", message = "MS " + str(speed))

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
    objects.serial.serial("/dev/ttyACM0", "send", ")")
    objects.serial.serial("/dev/ttyACM0", "send", "<")
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
    objects.serial.serial("/dev/ttyACM0", "send", "*")
    if float(objects.serial.serial("/dev/ttyACM0", "receive")) <= 9: return None # TODO add proper error handle
    objects.serial.serial("/dev/ttyACM0", "send", "(")
    objects.serial.serial("/dev/ttyACM0", "send", ">")
    objects.dock_status = False
pass

def voltage() -> float:
    """
    Collects battery voltage through serial.
    :return: float, voltage
    """
    objects.serial.serial("/dev/ttyACM0", "send", "*")
    return float(objects.serial.serial())
pass

def arrest() -> None:
    """
    Stop all motor movement.
    @return: None
    """
    serial(direction = "send", message = "A")
pass
