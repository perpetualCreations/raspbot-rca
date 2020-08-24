"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
nav.py module, contains navigation functions
Made by Taian Chen

Contains navigation load/execution and telemetry functions.
"""

from nav import objects

def nav_execute(direction, run_time):
    """
    Wrapper for client.send(), formats instructions and does hardware check for distance sensor.
    :param direction: direction of navigation.
    :param run_time: amount of time to run motors in that direction.
    :return: none.
    """
    if objects.components[1][1] is True:
        get_distance = True
    else:
        get_distance = False
    pass
    instructions = direction + " " + run_time + " " + str(get_distance)
    objects.comms.interface.send(instructions.encode(encoding = "ascii", errors = "replace"))
    if objects.comms.acknowledge.receive_acknowledgement() is False:
        return None
    pass
    if get_distance is True:
        client.create_process(client.nav_telemetry_get, self)
    pass
pass

def nav_load(file_name):
    """
    Reads from a given file line-by-line for instructions, and executes them through client.nav_execute().
    Reads syntax as <NAV DIRECTION/ACTION> <RUN TIME>. It looks similar to GCODE-style syntax. Telemetry is enabled when hardware passes, cannot be custom.
    Example of syntax: F 100
    :param file_name: name of file to read from.
    :return: none.
    """
    instructions = open(file_name)
    instruction_line = sum(1 for _ in instructions)
    while instruction_line > 0:
        raw_instructions = instructions.readline()
        instructions_split = raw_instructions.split()
        nav.nav_execute(self, instructions_split[0], instructions_split[1])
        sleep(int(instructions_split[1]))
        instruction_line -= 1
    pass
    instructions.close()
pass
def nav_telemetry_get():
    """
    Listens for telemetry data, made to be ran through multiprocessing.
    :return: none
    """
    stop = False
    while stop is False:
        nav_telemetry = self.socket.recv(4096).decode(encoding="utf-8", errors="replace") # TODO update this from self.socket
        if nav_telemetry == "rca-1.2:nav_end":
            stop = True
            content = "[END]"
        else:
            content = nav_telemetry
        pass
        self.nav_telemetry_text.configure(state=tkinter.NORMAL)
        self.nav_telemetry_text.insert("1.0", content)
        self.nav_telemetry_text.update_idletasks()
        self.nav_telemetry_text.configure(state=tkinter.DISABLED)
    pass
pass
