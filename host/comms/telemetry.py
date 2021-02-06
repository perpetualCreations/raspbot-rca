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
        interface.send(telemetry_interface.get(), objects.socket_telemetry)
        sleep(0.25)
    pass
    print("[INFO]: Telemetry stream has ended.")
pass
