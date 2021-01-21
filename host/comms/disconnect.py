"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Contains disconnect function.
"""

from comms import objects, interface

def disconnect():
    """
    Sends a message to host notifying that client has disconnected and then closes socket.
    :return: none.
    """
    try:
        interface.send(b"rca-1.2:disconnected")
        objects.socket_main.close()
    except OSError:
        pass
    pass
    print("[INFO]: Disconnected from client.")
    objects.basics.restart_shutdown.restart()
pass
