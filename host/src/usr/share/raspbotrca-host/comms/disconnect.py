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
    objects.process_camera_capture_kill_flag = True
    objects.process_telemetry_broadcast_kill_flag = True
    try:
        interface.send(b"rca-1.2:disconnected")
        objects.socket_init.close()
        objects.socket_main.close()
        objects.socket_telemetry_init.close()
        objects.socket_telemetry.close()
        print("[INFO]: Disconnected from client.")
    except OSError: pass
pass
