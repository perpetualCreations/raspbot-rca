"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Contains function for starting and managing telemetry stream.
"""

from comms import objects, interface
import telemetry
from time import sleep


# noinspection PyBroadException
def stream() -> None:
    """
    Initializes telemetry stream, creates loop for broadcasting to be ran through multithreading.
    Upon kill flag being raised, telemetry stream is stopped and socket is closed.
    @return: None
    """
    telemetry_interface = telemetry.telemetry()
    while objects.process_telemetry_broadcast_kill_flag is False:
        if objects.camera_is_restarting_flag: is_camera_restarting = "\nVideo stream stopped, camera is restarting..."
        else: is_camera_restarting = "\nCamera stream up."
        try:
            interface.send(message = telemetry_interface.get() + is_camera_restarting, socket_object = objects.socket_telemetry)
            if interface.receive(socket_object = objects.socket_telemetry).decode(encoding = "utf-8", errors = "replace") != "rca-1.2:ok": print("[FAIL]: Received invalid telemetry stream confirmation message.")
        except BaseException: # please stop complaining about the noinspection tag.
            print("[FAIL]: Telemetry stream raised exception. Client has disconnected/failed abruptly.")
            objects.restart_shutdown.restart()
        pass
    print("[INFO]: Telemetry stream has ended.")
pass
