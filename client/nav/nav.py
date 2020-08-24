"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
nav.py module, contains navigation functions
Made by Taian Chen
"""

try:
    import tkinter
    from tkinter import messagebox
    from platform import system
    from subprocess import call, Popen
    from time import sleep
    from .socket import comms
except ImportError as ImportErrorMessage:
    tkinter = None
    messagebox = None
    system = None
    call = None
    Popen = None
    sleep = None
    print("[NAV][FAIL]: Import failed!")
    print(ImportErrorMessage)
except ImportWarning as ImportWarningMessage:
    print("[NAV][FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
pass

class nav:
    """
    Main class
    """
    def __init__(self, components):
        """
        Initiation instructions.
        """
        print("[NAV][INFO]: Nav loaded!")
        self.nav_instructions = None
        self.nav_instruction_line = None
        self.components = components
    pass
    def nav_execute(self, direction, run_time):
        """
        Wrapper for client.send(), formats instructions and does hardware check for distance sensor.
        :param direction: direction of navigation.
        :param run_time: amount of time to run motors in that direction.
        :return: none.
        """
        if self.components[1][1] is True:
            get_distance = True
        else:
            get_distance = False
        pass
        instructions = direction + " " + run_time + " " + str(get_distance)
        self.socket.sendall(client.send(self, instructions.encode(encoding = "ascii", errors = "replace")))
        if client.receive_acknowledgement(self) is False:
            return None
        pass
        if get_distance is True:
            client.create_process(client.nav_telemetry_get, self)
        pass
    pass
    def nav_load_gui(self):
        """
        Creates GUI for loading navigation script.
        :return: none.
        """
        root = tkinter.Toplevel()
        root.title("Raspbot RCA: Nav Load")
        root.configure(bg="#344561")
        root.geometry('{}x{}'.format(260, 131))
        root.resizable(width=False, height=False)
        graphics_title = tkinter.Label(root, text="Enter script name to load.", fg="white", bg="#344561",
                                       font=("Calibri", 16))
        graphics_title.grid(row=0, column=0)
        graphics_entry = tkinter.Entry(root, bg="white", fg="black", font=("Calibri", 12))
        graphics_entry.grid(row=1, column=0, padx=(10, 0))
        graphics_confirm_button = tkinter.Button(root, bg="white", fg="black", text="Confirm", width=8, height=1,
                                                 font=("Calibri", 12),
                                                 command=lambda: client.nav_load(self, graphics_entry.get()))
        graphics_confirm_button.grid(row=2, column=0, padx=(10, 0), pady=(5, 0))
        root.mainloop()
    pass
    def nav_load(self, file_name):
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
    def nav_telemetry_get(self):
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
    @staticmethod
    def nav_edit():
        """
        Opens OS built-in text editor, similarly to client.set_configuration_gui().
        :return: none.
        """
        platform = system()
        if platform in ["Linux", "Ubuntu", "Debian", "Raspbian"]:
            root = tkinter.Toplevel()
            root.title("Raspbot RCA: Nav Name Entry")
            root.configure(bg = "#344561")
            root.geometry('{}x{}'.format(260, 131))
            root.resizable(width = False, height = False)
            graphics_title = tkinter.Label(root, text = "Enter script name.", fg = "white", bg = "#344561", font = ("Calibri", 16))
            graphics_title.grid(row = 0, column = 0)
            graphics_entry = tkinter.Entry(root, bg = "white", fg = "black", font = ("Calibri", 12))
            graphics_entry.grid(row = 1, column = 0, padx = (10, 0))
            graphics_confirm_button = tkinter.Button(root, bg = "white", fg = "black", text = "Confirm", width = 8, height = 1, font = ("Calibri", 12), command = lambda: call("sudo nano " + graphics_entry.get(), shell = True))
            graphics_confirm_button.grid(row = 2, column = 0, padx = (10, 0), pady = (5, 0))
            root.mainloop()
        elif platform == "Windows":
            root = tkinter.Toplevel()
            root.title("Raspbot RCA: Nav Name Entry")
            root.configure(bg = "#344561")
            root.geometry('{}x{}'.format(260, 131))
            root.resizable(width = False, height = False)
            graphics_title = tkinter.Label(root, text = "Enter script name.", fg = "white", bg = "#344561", font = ("Calibri", 16))
            graphics_title.grid(row = 0, column = 0)
            graphics_entry = tkinter.Entry(root, bg = "white", fg = "black", font = ("Calibri", 12))
            graphics_entry.grid(row = 1, column = 0, padx = (10, 0))
            graphics_confirm_button = tkinter.Button(root, bg = "white", fg = "black", text = "Confirm", width = 8, height = 1, font = ("Calibri", 12), command = lambda: Popen(["notepad.exe", graphics_entry.get()]))
            graphics_confirm_button.grid(row = 2, column = 0, padx = (10, 0), pady = (5, 0))
            root.mainloop()
        else:
            messagebox.showerror("Raspbot RCA: OS Unsupported", "Client OS is unsupported, please manually edit configuration! Open an issue on Github for your operating system to be supported.")
        pass
    pass
pass