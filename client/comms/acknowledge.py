"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by Taian Chen

Contains acknowledgement handle function.
"""

from comms import objects, interface

def receive_acknowledgement():
    """
    Listens for an acknowledgement byte string, returns booleans whether string was received or failed.
    :return: True/False boolean, only returns True when an acknowledgement is successfully received, otherwise returns False for errors.
    """
    try:
        acknowledgement = interface.receive()
    except objects.socket.error as sae:
        print("[FAIL]: Failed to receive acknowledgement string. See below for details.")
        print(sae)
        return False
    pass
    if acknowledgement == b"rca-1.2:connection_acknowledge":
        print("[INFO]: Received acknowledgement.")
        return True
    elif acknowledgement == b"rca-1.2:authentication_invalid":
        print("[FAIL]: Did not receive an acknowledgement. Authentication was invalid.")
        return False
    elif acknowledgement == b"rca-1.2:unknown_command":
        print("[FAIL]: Command unrecognized by host.")
        return False
    else:
        objects.messagebox.showwarning("Raspbot RCA: Bad Acknowledgement", "The host has replied with an invalid acknowledgement." + "\n Received: " + acknowledgement.decode(encoding = "utf-8", errors = "replace"))
        print("[FAIL]: Did not receive an acknowledgement. Instead received: ")
        print(acknowledgement.decode(encoding = "uft-8", errors = "replace")) # WARN if buffersize is large enough for overflow, this display code could be a vulnerability. Luckily it's 4096 bytes, but still...
        return False
    pass
pass
