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
    interface.send(b"rca-1.2:disconnected")
    objects.net_status_data.set("Status: " + "Disconnected")
    objects.socket.close(0)
    print("[INFO]: Disconnected from bot.")
pass
