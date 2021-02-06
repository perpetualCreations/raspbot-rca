"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Made by perpetualCreations

Main client class.
"""

try:
    print("[INFO]: Starting imports...")
    from subprocess import call, Popen
    from time import sleep
    import socket, configparser, ping3, webbrowser
    import tkinter
    from tkinter import messagebox
    from ast import literal_eval
    from platform import system
    from typing import Union
    from sys import argv
    # Pyside6
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QFile, QIODevice, Signal, Slot, QObject
    from PySide6.QtGui import *
    # RCA Modules
    import basics, comms, nav
except ImportError as ImportErrorMessage:
    print("[FAIL]: Imports failed! See below.")
    print(ImportErrorMessage)
    exit(1)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(ImportWarningMessage)
    exit(1)
pass

# basics.basics.log_init()
# TODO uncomment logging init, for dev

class client(QObject):
    """
    Main client class.
    """

    signal_status_refresh = Signal(object, str, str, bool)  # connect message, dock message, is in erroneous state
    signal_telemetry_refresh = Signal(object, str)  # telemetry message
    signal_gui_lock_from_state = Signal(object, bool, bool)  # is connected, is docked

    def __init__(self) -> None:
        """
        Initiation function of Raspbot RCA. Reads configs and starts various process and GUI.
        """
        print("[INFO]: Starting client Raspbot RC Application...")
        super(client, self).__init__()
        print("[INFO]: Declaring variables...")
        self.connect_retries = 0
        self.ping_text = None # GUI element referenced across two functions, has a class variable to allow for it
        self.ping_button = None # GUI element referenced across two functions, has a class variable to allow for it
        self.ping_results = "" # placeholder, overwritten by any return from ping functions to be displayed as results
        self.report_content = "" # placeholder, overwritten by any return from report functions
        self.gui_hide_console = False # configuration variable to hide/show Python console, unused
        self.process_status_refresh_kill_flag = False
        self.process_gui_lock_from_state_kill_flag = False
        print("[INFO]: Loading configurations...")
        self.components = basics.basics.load_hardware_config()  # [Base Set [cam], RFP Enceladus [sensehat, distance, dust], Upgrade #1 [charger], Robotic Arm Kit [arm, arm_cam]]
        config_parse_load = configparser.ConfigParser()
        try:
            config_parse_load.read("main.cfg")
            self.gui_hide_console = literal_eval(config_parse_load["GUI"]["hide_console"])
        except configparser.Error as ConfigParserErrorMessage:
            print("[FAIL]: Failed to load configurations! See below for details.")
            print(ConfigParserErrorMessage)
            basics.basics.exit(1)
        except KeyError as KeyErrorMessage:
            print("[FAIL]: Failed to load configurations! Configuration file is corrupted or has been edited incorrectly.")
            print(KeyErrorMessage)
            basics.basics.exit(1)
        except FileNotFoundError as NotFoundMessage:
            print("[FAIL]: Failed to load configurations! Configuration file is missing.")
            print(NotFoundMessage)
            basics.basics.exit(1)
        pass
        print("[INFO]: Starting GUI...")
        self.dummy_tkinter_root = tkinter.Tk() # stops tkinter.messagebox from making an empty window
        self.dummy_tkinter_root.withdraw()
        self.app = QApplication(argv)
        self.app.setWindowIcon(QIcon("favicon.ico")) # it just works
        ui_file = QFile("main.ui")
        if not ui_file.open(QIODevice.ReadOnly):
            print("[FAIL]: UI XML file is not in read-only. Is it being edited by another application?")
            basics.basics.exit(1)
        pass
        self.loader = QUiLoader()
        self.window = self.loader.load(ui_file)
        ui_file.close()
        if not self.window:
            print("[FAIL]: UI XML file could not be loaded to generate interface.")
            print(self.loader.errorString())
            basics.exit(1)
        pass
        self.window.connectbutton.clicked.connect(lambda: comms.connect.connect())
        self.window.disconnectbutton.clicked.connect(lambda: comms.disconnect.disconnect())
        self.window.updateosbutton.clicked.connect(lambda: comms.interface.send(b"rca-1.2:command_update"))
        self.window.shutdownbutton.clicked.connect(lambda: client.os_control_shutdown_wrapper())
        self.window.rebootbutton.clicked.connect(lambda: client.os_control_reboot_wrapper())
        self.window.helpbutton.clicked.connect(lambda: messagebox.showinfo("Raspbot RCA: Control Help", "Use Update OS to update APT packages,\n Shutdown and Reboot perform operations as labeled."
                                                                           + "\nA word of caution, after shutting down, there is no way to turn the bot back on besides physically power cycling.\n Please use cautiously."
                                                                           + "\nChoose a report-type with the dropdown, select Collect Report to as labeled collect the report,\n and either use Save or View Report afterwards."))
        self.window.executebutton.clicked.connect(lambda: print("[FAIL]: Not implemented!")) # TODO rework nav to fit new ui
        self.window.loadbutton.clicked.connect(lambda: print("[FAIL]: Not implemented!"))
        self.window.editbutton.clicked.connect(lambda: print("[FAIL]: Not implemented!"))
        self.window.keyboardtogglebutton.clicked.connect(lambda: print("[FAIL]: Not implemented!")) # TODO requires keyboard nav module
        self.window.navhelpbutton.clicked.connect(lambda: messagebox.showinfo("Raspbot RCA: Navigation Help", "This panel contains navigation controls.\nUse Load, Edit, and Execute to run scripts."
                                                                              + "\nSee documentation regarding how to write these scripts.\nPress Toggle Keyboard Control to enable or disable keyboard controls."
                                                                              + "\nKeyboard controls in question are:\nW - Forwards\nA - Left Turn\nS - Backwards\nD - Right Turn\nQ - Clockwise Spin\nE - Counterclockwise Spin"))
        self.window.saveframebutton.clicked.connect(lambda: print("[FAIL]: Not implemented!")) # TODO requires camera view to work with multiprocess- i mean threading
        self.window.collectbutton.clicked.connect(lambda: client.report_collect(self, self.window.typeselect.currentText()))
        self.window.savebutton.clicked.connect(client.report_save(self, self.window.typeselect.currentText(), self.report_content))
        self.window.viewbutton.clicked.connect(client.report_gui(self, self.window.typeselect.currentText(), self.report_content))
        self.window.telemetryview.setReadOnly(True)
        self.window.dockbutton.clicked.connect(lambda: comms.interface.send(b"rca-1.2:command_dock"))
        self.window.undockbutton.clicked.connect(lambda: comms.interface.send(b"rca-1.2:command_undock"))
        self.window.menubar.triggered[QAction].connect(self.menu_trigger)
        self.window.disconnectbutton.setEnabled(False)
        self.window.updateosbutton.setEnabled(False)
        self.window.shutdownbutton.setEnabled(False)
        self.window.rebootbutton.setEnabled(False)
        self.window.executebutton.setEnabled(False)
        self.window.keyboardtogglebutton.setEnabled(False)
        self.window.saveframebutton.setEnabled(False)
        self.window.collectbutton.setEnabled(False)
        self.window.typeselect.setEnabled(False)
        self.window.dockbutton.setEnabled(False)
        self.window.undockbutton.setEnabled(False)
        self.window.show()
        print("[INFO]: Threading for main GUI starting...")
        self.process_telemetry_refresh = basics.process.create_process(client.telemetry_refresh, (self,))
        self.process_status_refresh = basics.process.create_process(client.status_refresh, (self,))
        self.process_gui_lock_from_state = basics.process.create_process(client.gui_lock_from_connect_state, (self,))
        self.signal_telemetry_refresh.connect(client.telemetry_refresh_commit)
        self.signal_status_refresh.connect(client.status_refresh_commit)
        self.signal_gui_lock_from_state.connect(client.gui_lock_from_connect_state_commit)
        basics.basics.exit(self.app.exec_())
        print("[INFO]: Loading complete.")
    pass

    def menu_trigger(self, qobj: object) -> None:
        """
        Function for executing menubar selections.
        :param qobj: Qt object
        :return: None
        """
        SWITCH = {"Exit":lambda: basics.basics.exit(0), "Edit Network":lambda: print("TODO MENU EDIT NETWORK"), "Edit Hardware":lambda: print("TODO MENU EDIT HARDWARE"), "Edit Main":lambda: print("TODO MENU EDIT MAIN"), "Ping": lambda: client.ping_gui(self), "SenseHAT LEDs":lambda: client.led_gui(self), "Arm Control":lambda: client.arm_control_gui(self), "View Documentation":lambda: webbrowser.open_new("https://dreamerslegacy.xyz/projects/raspbot/docs.html"), "Visit Github Repo":lambda: webbrowser.open_new("https://github.com/perpetualCreations/raspbot-rca/")}
        try: SWITCH[qobj.text()]()
        except KeyError:
            print("[FAIL]: client.menu_trigger was unable to process given menubar action, this should never occur. Received,")
            print(qobj.text())
        pass

    @Slot(bool, bool)
    def gui_lock_from_connect_state_commit(self, connected: bool, docked: bool) -> None:
        """
        Commits setEnabled states to widgets.
        :param connected: bool, passed from client.gui_lock_from_connect_state, is client connected
        :param docked: bool, passed from client.gui_lock_from_connect_state, is bot docked
        :return: None
        """
        if connected is True:
            self.window.connectbutton.setEnabled(False)
            self.window.disconnectbutton.setEnabled(True)
            self.window.updateosbutton.setEnabled(True)
            self.window.shutdownbutton.setEnabled(True)
            self.window.rebootbutton.setEnabled(True)
            self.window.executebutton.setEnabled(True)
            self.window.keyboardtogglebutton.setEnabled(True)
            self.window.saveframebutton.setEnabled(True)
            self.window.collectbutton.setEnabled(True)
            self.window.typeselect.setEnabled(True)
            self.window.dockbutton.setEnabled(True)
            self.window.undockbutton.setEnabled(True)
            if docked is False:
                self.window.undockbutton.setEnabled(False)
                self.window.dockbutton.setEnabled(True)
            else:
                self.window.dockbutton.setEnabled(False)
                self.window.undockbutton.setEnabled(True)
            pass
        else:
            self.window.connectbutton.setEnabled(True)
            self.window.disconnectbutton.setEnabled(False)
            self.window.updateosbutton.setEnabled(False)
            self.window.shutdownbutton.setEnabled(False)
            self.window.rebootbutton.setEnabled(False)
            self.window.executebutton.setEnabled(False)
            self.window.keyboardtogglebutton.setEnabled(False)
            self.window.saveframebutton.setEnabled(False)
            self.window.collectbutton.setEnabled(False)
            self.window.typeselect.setEnabled(False)
            self.window.dockbutton.setEnabled(False)
            self.window.undockbutton.setEnabled(False)
        pass

    def gui_lock_from_connect_state(self) -> None:
        """
        Emits signals depending on connection status.
        This prevents certain functions from being triggered at untimely states (i.e disconnect/connect being pressed twice, commands being sent while disconnected).
        For multithreading.
        :return: None
        """
        print("[INFO]: GUI lock thread started.")
        while self.process_gui_lock_from_state_kill_flag is False:
            self.signal_gui_lock_from_state.emit(self, comms.objects.is_connected, comms.objects.dock_status)
            sleep(0.5)
        pass
        print("[INFO]: GUI lock thread ended.")

    @Slot(str)
    def telemetry_refresh_commit(self, content: str) -> None:
        """
        Refreshes telemetry display.
        :param content: str, incoming telemetry data passed from client.telemetry_refresh
        :return: None
        """
        self.window.telemetryview.setPlainText(content)

    def telemetry_refresh(self) -> None:
        """
        Produces signal and string for telemetry refresh. Intended solely for multithreading.
        :return: None
        """
        print("[INFO]: Telemetry refresh thread started.")
        while comms.objects.process_telemetry_refresh_kill_flag is False:
            while comms.objects.is_connected is False: pass
            self.signal_telemetry_refresh.emit(self, comms.interface.receive(socket_object = comms.objects.socket_telemetry).decode(encoding = "utf-8", errors = "replace"))
            sleep(0.25)
        pass
        print("[INFO]: Telemetry refresh thread ended.")

    @Slot(str, str, bool)
    def status_refresh_commit(self, connect: str, dock: str, error: bool) -> None:
        """
        Refreshes status display.
        :param connect: return of SWITCH_CONNECT[comms.objects.is_connected]
        :param dock: return of SWITCH_DOCK[comms.objects.dock_status]
        :param error: bool, if True set status as "Unknown status"
        :return: None
        """
        if error is not True: self.window.status.setText(connect + ", currently " + dock + ".")
        else: self.window.status.setText("Unknown status.")

    def status_refresh(self) -> None:
        """
        Produces signal and strings for status refresh. Intended solely for multithreading.
        :return: None
        """
        print("[INFO]: Status refresh thread started.")
        SWITCH_CONNECT = {False:"Disconnected", True:"Connected"}
        SWITCH_DOCK = {False:"undocked", True:"docked", None:"dock status is unknown"}
        while self.process_status_refresh_kill_flag is False:
            try: self.signal_status_refresh.emit(self, SWITCH_CONNECT[comms.objects.is_connected], SWITCH_DOCK[comms.objects.dock_status], False)
            except KeyError: self.signal_status_refresh.emit("UNKNOWN", "UNKNOWN", True)
            sleep(0.25)
        pass
        print("[INFO]: Status refresh thread ended.")

    @staticmethod
    def set_configuration_gui(file: str) -> None:
        """
        Either opens nano text editor for Linux systems or will open OS' built-in text editor if not Linux.
        In the future, does exactly what client.set_configuration does, but with a GUI window.
        :param file: str, filename of config
        TODO update set_configuration_gui to tkinter GUI
        """
        platform = system()
        if platform in ["Linux", "Ubuntu", "Debian", "Raspbian", "Kubuntu", "Arch", "Arch Linux", "Fedora", "Linux Mint"]:
            call("sudo nano " + file, shell = True)
        elif platform == "Windows":
            Popen(["notepad.exe", file])
        else:
            messagebox.showerror("Raspbot RCA: OS Unsupported", "Client OS is unsupported, please manually edit configuration! The accepted operating systems are Linux and Linux distributions, and Windows. If you believe this is a mistake please open an issue on the repository page.")
        pass
    pass

    @staticmethod
    def ping() -> list:
        """
        Pings host address and records latency and losses.
        :return: average latency, nested list with individual latency values, total losses, nested list with individual losses, if host resolution failed
        """
        print("[INFO]: Starting PING test...")
        scans = [ping3.ping(comms.objects.host, timeout = 10, size = 64, unit = "ms"), ping3.ping(comms.objects.host, timeout = 10, size = 64, unit = "ms"), ping3.ping(comms.objects.host, timeout = 10, size = 64, unit = "ms"), ping3.ping(comms.objects.host, timeout = 10, size = 64, unit = "ms")]
        if False in scans:
            return [None, [None, None, None, None], 4, [True, True, True, True], True]
        else:
            result = [0, [scans[0], scans[1], scans[2], scans[3]], 0, [False, False, False, False], None]
            if scans[0] is None:
                result[1][0] = 0
                result[2] += 1
                result[3][0] = True
            elif scans[1] is None:
                result[1][1] = 0
                result[2] += 1
                result[3][1] = True
            elif scans[2] is None:
                result[1][2] = 0
                result[2] += 1
                result[3][2] = True
            elif scans[3] is None:
                result[1][3] = 0
                result[2] += 1
                result[3][3] = True
            pass
            result[0] = (result[1][0] + result[1][1] + result[1][2] + result[1][3])/4
            print("[INFO]: PING test complete.")
            return result
        pass
    pass

    def ping_wrapper(self) -> None:
        """
        Wrapper for client.ping() for ping_gui.
        :return: none
        """
        ping_results_raw = client.ping()
        if ping_results_raw[4] is True:
            self.ping_results = "Unable to resolve hostname," + "\n" + "is the NET configuration correct?" + "\n" + "Host IP was:" + "\n" + comms.objects.host
        else:
            ping_results_raw[0] = round(ping_results_raw[0], 2)
            ping_results_raw[1][0] = round(ping_results_raw[1][0], 2)
            ping_results_raw[1][1] = round(ping_results_raw[1][1], 2)
            ping_results_raw[1][2] = round(ping_results_raw[1][2], 2)
            ping_results_raw[1][3] = round(ping_results_raw[1][3], 2)
            if ping_results_raw[3][0] is True: ping_results_raw[1][0] = "Timed out!"
            elif ping_results_raw[3][1] is True: ping_results_raw[1][1] = "Timed out!"
            elif ping_results_raw[3][2] is True: ping_results_raw[1][2] = "Timed out!"
            elif ping_results_raw[3][3] is True: ping_results_raw[1][3] = "Timed out!"
            self.ping_results = "Average Latency (ms): " + str(ping_results_raw[0]) + "\n" + "Test 1 Latency: " + str(ping_results_raw[1][0]) + "\n" + "Test 2 Latency: " + str(ping_results_raw[1][1]) + "\n" + "Test 3 Latency: " + str(ping_results_raw[1][2]) + "\n" + "Test 4 Latency: " + str(ping_results_raw[1][3]) + "\n" + str(ping_results_raw[2]) + "/4" + " Loss"
        pass
        self.ping_text.configure(state = tkinter.NORMAL)
        self.ping_text.insert("1.0", self.ping_results)
        self.ping_text.update_idletasks()
        self.ping_text.configure(state = tkinter.DISABLED)
    pass

    def ping_gui(self) -> None:
        """
        GUI tool for pinging IP addresses.
        :return: None
        """
        print("[INFO]: Displayed ping_gui.")
        ping_gui = tkinter.Toplevel()
        ping_gui.title("Raspbot RCA: Ping")
        ping_gui.configure(bg = "#344561")
        ping_gui.geometry('{}x{}'.format(255, 290))
        ping_gui.resizable(width = False, height = False)
        self.ping_text = tkinter.Text(ping_gui, height = 8, width = 30, bg = "white", fg = "black", font = ("Calibri", 12))
        self.ping_text.grid(row = 0, column = 0, pady = (8, 14), padx = (5, 5))
        self.ping_text.configure(state = tkinter.DISABLED)
        self.ping_button = tkinter.Button(ping_gui, bg = "white", fg = "black", text = "Ping", width = 20, font = ("Calibri", 12), command = lambda: client.ping_wrapper(self))
        self.ping_button.grid(row = 1, column = 0, pady = (0, 2))
        save_button = tkinter.Button(ping_gui, bg = "white", fg = "black", text = "Save", width = 20, font = ("Calibri", 12), command = lambda: client.report_save(self, "PING", self.ping_results))
        save_button.grid(row = 2, column = 0, pady = (0, 2))
        close_button = tkinter.Button(ping_gui, bg = "white", fg = "black", text = "Close", width = 20, font = ("Calibri", 12), command = lambda: ping_gui.destroy())
        close_button.grid(row = 3, column = 0, pady = (0, 10))
        ping_gui.mainloop()
    pass

    def report_collect(self, report_type: str) -> None:
        """
        Sends a report request to host with given type and sets self.report_content with results.
        :param report_type: type of report.
        :return: None
        """
        if report_type == "Science":
            if self.components[1][0] is True or self.components[1][1] is True or self.components[1][2] is True:
                comms.interface.send(b"rca-1.2:command_science_collect")
                if comms.acknowledge.receive_acknowledgement() is False: return None
                self.report_content = comms.interface.receive().decode(encoding = "utf-8", errors = "replace")
            else: return None
        elif report_type == "CH Check":
            comms.interface.send(b"rca-1.2:command_ch_check")
            if comms.acknowledge.receive_acknowledgement() is False: return None
            data = comms.interface.receive().decode(encoding="utf-8", errors="replace")
            self.report_content = data
        else: return None
    pass

    def report_gui(self, report_type: str, content: str) -> None:
        """
        Views a report with given type and contents.
        :param report_type: type of report.
        :param content: report contents to be displayed.
        :return: None
        """
        if self.report_content == "": return None
        print("[INFO]: Displayed report_gui.")
        report_gui = tkinter.Toplevel()
        report_gui.title("Raspbot RCA: Report Viewer, " + report_type)
        report_gui.configure(bg = "#344561")
        report_gui.geometry('{}x{}'.format(400, 370))
        report_gui.resizable(width = False, height = False)
        graphics_report = tkinter.Text(report_gui, height = 15, bg = "white", fg = "black", font = ("Calibri", 12))
        graphics_report.configure(state = tkinter.NORMAL)
        graphics_report.insert("1.0", content)
        graphics_report.update_idletasks()
        graphics_report.configure(state = tkinter.DISABLED)
        graphics_report.grid(row = 0, column = 0, pady = (5, 14))
        graphics_report_close_button = tkinter.Button(report_gui, bg = "white", fg = "black", text = "Close", width = 40, font = ("Calibri", 12), command = lambda: report_gui.destroy())
        graphics_report_close_button.grid(row = 1, column = 0, pady = (0, 10))
        report_gui.mainloop()
    pass

    def report_save(self, report_type: str, content: str) -> None:
        """
        Saves a report with given type and contents.
        :param report_type: type of report.
        :param content: report contents to be saved.
        :return: None
        """
        if self.report_content == "" and report_type != "PING": return None
        file_report_name = report_type + "_report-" + basics.basics.make_timestamp() + ".txt"
        print("[INFO]: Generating text file report...")
        file_report = open(file_report_name, "w+")
        file_report.write(content)
        file_report.close()
        print("[INFO]: Report saved.")
    pass

    def dock(self) -> None:
        """
        Instructs host to dock with charger station.
        """
        comms.interface.send(b"rca-1.2:command_dock")
        if comms.acknowledge.receive_acknowledgement() is False: return None
        comms.objects.dock_status = True
    pass

    def undock(self) -> None:
        """
        Instructs host to undock from charger station.
        :return: None
        """
        comms.interface.send(b"rca-1.2:comamnd_undock")
        if comms.acknowledge.receive_acknowledgement() is False: return None
        comms.objects.dock_status = False
    pass

    @staticmethod
    def os_control_shutdown_wrapper() -> None:
        """
        Creates dialogue asking for user to confirm to shutdown bot.
        :return: None
        """
        if messagebox.askyesno("Raspbot RCA: Confirm Shutdown?", "Are you sure you want to shutdown the bot? There is no way to boot it besides physically restarting its power source, and if the Arduino fails, you may overdischarge your battery.") is True:
            comms.interface.send(b"rca-1.2:command_shutdown")
            comms.disconnect.disconnect()
        else: return None
    pass

    @staticmethod
    def os_control_reboot_wrapper() -> None:
        """
        Creates dialogue asking for user to confirm to shutdown bot.
        :return: None
        """
        if messagebox.askyesno("Raspbot RCA: Confirm Reboot?", "Are you sure you want to reboot the bot?") is True:
            comms.interface.send(b"rca-1.2:command_reboot")
            comms.disconnect.disconnect()
        else: return None
    pass

    def led_command(self, command: str, frame: Union[None, str, int] = None) -> None:
        """
        Issues commands to host for controlling LED matrix on SenseHAT by controlling transmissions.
        :param command: command to be executed by host.
        :param frame: index number for target frame set to be played, if command is not image or play, is ignored.
        :return: None
        """
        if self.components[1][0] is not True: return None
        if isinstance(frame, int) is True: frame = str(frame)
        comms.interface.send(b"rca-1.2:led_graphics")
        if comms.acknowledge.receive_acknowledgement() is False: return None
        if command != "play":
            comms.interface.send(command) # TODO command != play clause is temporary until play command is implemented
            if comms.acknowledge.receive_acknowledgement() is False: return None
            elif command == "image": comms.interface.send(frame)
    pass

    def led_gui(self) -> None:
        """
        Creates GUI for controlling LED matrix on SenseHAT.
        :return: None
        """
        print("[INFO]: Displayed led_gui.")
        led_gui = tkinter.Toplevel()
        led_gui.title("Raspbot RCA: LED Controls")
        led_gui.configure(bg = "#344561")
        led_gui.geometry('{}x{}'.format(260, 131))
        led_gui.resizable(width=False, height=False)
        graphics_title = tkinter.Label(led_gui, text = "LED Controls", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 0, column = 0, padx = (0, 290))
        graphics_led_frame_buttons = tkinter.Frame(led_gui, bg = "#344561")
        graphics_led_button_off = tkinter.Button(graphics_led_frame_buttons, text = "Off", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: client.led_command(self, "stop"))
        graphics_led_button_off.pack(side = tkinter.TOP)
        graphics_led_button_hello_world = tkinter.Button(graphics_led_frame_buttons, text = "Hello World", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: client.led_command(self, "image", "1"))
        graphics_led_button_hello_world.pack(side = tkinter.BOTTOM)
        graphics_led_button_idle = tkinter.Button(graphics_led_frame_buttons, text = "Idle", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: client.led_command(self, "image", "2"))
        graphics_led_button_idle.pack(side = tkinter.BOTTOM)
        graphics_led_frame_buttons.grid(row = 2, column = 0, padx = (0, 250))
        led_gui.mainloop()
    pass

    def arm_control_gui(self) -> None:
        """
        Creates GUI for user to control arm.
        This will only be available if enabled, hardware check is performed at creation of main window.
        :return: None
        """

        pass
    pass
pass

if __name__ == "__main__": client()
