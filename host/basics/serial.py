"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multiprocessing, and editing configs.
Made by perpetualCreations

Serial communications function contained within this module.
Other wrapper functions that make use of serial are included as well.
"""

def serial(port, direction, message = None):
    """
    Sends or receives serial communications to the Arduino integration.
    :param port: the port that the Arduino is connected to.
    :param direction: whether to expect to receive or send.
    :param message: what contents to send, or if receiving leave as None.
    :return: if receiving, decoded string, if sending or invalid direction, none.
    """
    arduino_connect = serial.Serial(port = port, timeout = 5)
    if direction == "receive":
        return arduino_connect.readline().decode(encoding = "utf-8", errors = "replace")
    elif direction == "send":
        arduino_connect.write(message.encode(encoding = "ascii", errors = "replace"))
    else:
        return None
    pass
pass

def nav_timer(nav_run_time, nav_distance_accept):
    """
    Navigation timer for multiprocessing, counts down until run time is over, also reads distance telemetry and forwards to client.
    :param nav_run_time: amount of time to run motors as an integer value.
    :param nav_distance_accept: whether to forward ToF data signaled by a boolean.
    :return: none.
    """
    nav_run_time_countdown = nav_run_time
    while nav_run_time_countdown != 0:
        nav_run_time_countdown -= 1
        if nav_distance_accept is True and objects.components[1][1] is True:
            host.serial("/dev/ttyACM0", "send", b"T")
            objects.interface.send(serial.serial("/dev/ttyACM0", "receive", None))
        else:
            objects.interface.send(b"No Data")
        pass
        if nav_run_time_countdown == 0:
            objects.interface.send(b"rca-1.2:nav_end")
            host.serial("/dev/ttyACM0", "send", b"A")
        pass
        sleep(1)
    pass
pass

def dock():
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

def undock():
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


def voltage():
    """
    Collects battery voltage through serial.
    :return: float, voltage
    """
    objects.serial.serial("/dev/ttyACM0", "send", "*")
    return float(objects.serial.serial("/dev/ttyACM0", "receive"))
pass
