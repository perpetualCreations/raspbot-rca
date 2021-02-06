"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
nav.py module, contains navigation functions
Made by Taian Chen

Contains navigation load/execution and telemetry functions.
"""

from nav import objects
from typing import Union

def nav_execute(direction: str, run_time: Union[str, int]) -> None:
    """
    Wrapper for client.send(), formats instructions and does hardware check for distance sensor.
    :param direction: direction of navigation.
    :param run_time: amount of time to run motors in that direction.
    :return: None
    """
    objects.comms.interface.send("rca-1.2:nav_start")
    if isinstance(run_time, int) is True: run_time = str(run_time)
    objects.comms.interface.send((direction + " " + run_time).encode(encoding = "ascii", errors = "replace"))
    if objects.comms.acknowledge.receive_acknowledgement() is False: return None
pass

def nav_load(file_name: str) -> None:
    """
    Reads from a given file line-by-line for instructions, and executes them through client.nav_execute().
    Reads syntax as <NAV DIRECTION/ACTION> <RUN TIME>. It looks similar to GCODE-style syntax. Telemetry is enabled when hardware passes, cannot be custom.
    Example of syntax: F 100
    :param file_name: name of file to read from.
    :return: None
    """
    instructions = open(file_name)
    instruction_line = sum(1 for _ in instructions)
    while instruction_line > 0:
        raw_instructions = instructions.readline()
        instructions_split = raw_instructions.split()
        nav_execute(instructions_split[0], instructions_split[1])
        objects.sleep(int(instructions_split[1]))
        instruction_line -= 1
    pass
    instructions.close()
pass
