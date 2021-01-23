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
    objects.process.stop_process(objects.process_camera_feed, True)
    try:
        interface.send(b"rca-1.2:disconnected")
        objects.socket_main.close()
        objects.socket_main = objects.socket.socket(objects.socket.AF_INET, objects.socket.SOCK_STREAM) # reset socket, as originally defined in objects
        objects.socket_main.settimeout(10)
        objects.socket_main.setblocking(True)
    except OSError:
        pass
    pass
    objects.net_status_data.set("Status: " + "Disconnected")
    print("[INFO]: Disconnected from bot.")
pass
