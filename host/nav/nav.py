"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
nav.py module, contains navigation functions
Made by perpetualCreations

Contains navigation execution function.
"""

# TODO when comms is implemented, please change socket interactions in timer function

from nav import objects

def nav_timer(nav_run_time, nav_distance_accept):
    """
    Navigation timer for multiprocessing, counts down until run time is over, also reads distance telemetry and forwards to client.
    :param nav_run_time: amount of time to run motors as an integer value.
    :param nav_distance_accept: whether to forward ToF data signaled by a boolean.
    :return: none.
    """
    nav_run_time_countdown = nav_run_time
    while nav_run_time_countdown != 0:
        nav_run_time_countdown -= 1
        if nav_distance_accept is True and objects.components[1][1] is True:
            host.serial("/dev/ttyACM0", "send", b"T")
            socket.sendall(host.send(self, serial.serial("/dev/ttyACM0", "receive", None)))
        else:
            socket.sendall(host.send(self, b"No Data"))
        pass
        if nav_run_time_countdown == 0:
            socket.sendall(host.send(self, b"rca-1.2:nav_end"))
            host.serial("/dev/ttyACM0", "send", b"A")
        pass
        sleep(1)
    pass
pass
