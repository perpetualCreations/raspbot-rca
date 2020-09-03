"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multiprocessing, and editing configs.
Made by perpetualCreations

Serial communications function contained within this module.
"""

def serial(port, direction, message):
    """
    Sends or receives serial communications to the Arduino integration.
    :param port: the port that the Arduino is connected to.
    :param direction: whether to expect to receive or send.
    :param message: what contents to send, or if receiving leave as None.
    :return: if receiving, decoded string, if sending or invalid direction, none.
    """
    arduino_connect = serial.Serial(port=port, timeout=5)
    if direction == "receive":
        return arduino_connect.readline().decode(encoding="utf-8", errors="replace")
    elif direction == "send":
        if message not in [""]:  # TODO list all possible commands
            return None
        pass
        arduino_connect.write(message.encode(encoding="ascii", errors="replace"))
        return None
    else:
        return None
    pass
pass
