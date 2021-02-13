"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Contains disconnect function.
"""

from comms import objects, interface

def disconnect() -> None:
    """
    Sends a message to host notifying that client has disconnected and then closes socket.
    :return: None
    """
    objects.process_camera_feed_kill_flag = True
    objects.is_connected = False
    try:
        interface.send(b"rca-1.2:disconnected")
        objects.socket_main.close()
        objects.socket_main = objects.socket.socket(objects.socket.AF_INET, objects.socket.SOCK_STREAM) # reset socket, as originally defined in objects
        objects.socket_main.settimeout(10)
        objects.socket_main.setblocking(True)
        objects.socket_telemetry.close()
        objects.socket_telemetry = objects.socket.socket(objects.socket.AF_INET, objects.socket.SOCK_STREAM) # reset socket, as originally defined in objects
        objects.socket_telemetry.settimeout(10)
        objects.socket_telemetry.setblocking(True)
        print("[INFO]: Disconnected from bot.")
    except OSError: pass
pass
