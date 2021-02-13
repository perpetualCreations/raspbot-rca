"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Contains function for starting and managing telemetry stream.
"""

from comms import objects, interface
import telemetry
from time import sleep

def stream() -> None:
    """
    Initializes telemetry stream, creates loop for broadcasting to be ran through multithreading.
    Upon kill flag being raised, telemetry stream is stopped and socket is closed.
    @return: None
    """
    telemetry_interface = telemetry.telemetry()
    while objects.process_telemetry_broadcast_kill_flag is False:
        if objects.camera_is_restarting_flag: is_camera_restarting = "\nVideo stream stopped, camera is restarting..."
        else: is_camera_restarting = "\nCamera stream up. "
        interface.send(telemetry_interface.get() + is_camera_restarting, objects.socket_telemetry)
    print("[INFO]: Telemetry stream has ended.")
pass
