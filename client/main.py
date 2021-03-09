"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Made by perpetualCreations

Main client class.
"""

try:
    print("[INFO]: Starting imports...")
    from subprocess import Popen
    from time import sleep
    import socket, configparser, ping3, webbrowser, cv2, tkinter
    from tkinter import messagebox
    from ast import literal_eval
    from platform import system
    from typing import Union
    from sys import argv
    from os import remove, rename, path
    from pynput.keyboard import Key, Listener
    # Pyside6
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import QApplication, QDialog
    from PySide6.QtCore import QFile, QIODevice, Signal, Slot, QObject
    from PySide6.QtGui import *
    # RCA Modules
    import basics
    basics.basics.log_init()
    import comms
except ImportError as ImportErrorMessage:
    print("[FAIL]: Imports failed! See below.")
    print(ImportErrorMessage)
    exit(1)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(ImportWarningMessage)
    exit(1)
pass

class client(QObject):
    """
    Main client class.
    """

    signal_status_refresh = Signal(object, str, str, bool, bool)  # connect message, dock message, is in erroneous state
    signal_telemetry_refresh = Signal(object, str)  # telemetry message
    signal_gui_lock_from_state = Signal(object, bool, bool)  # is connected, is docked
    signal_camera_refresh_clock = Signal(object) # no passed parameters

    def __init__(self) -> None:
        """
        Initiation function of Raspbot RCA. Reads configs and starts various process and GUI.
        """
        print("[INFO]: Starting client Raspbot RC Application...")
        super(client, self).__init__()
        print("[INFO]: Declaring variables...")
        self.connect_retries = 0
        self.ping_results = "" # placeholder, overwritten by any return from ping functions to be displayed as results
        self.report_content = "" # placeholder, overwritten by any return from report functions
        self.gui_hide_console = False # configuration variable to hide/show Python console, unused
        self.process_status_refresh_kill_flag = False
        self.process_gui_lock_from_state_kill_flag = False
        self.process_camera_view_refresh_clock_kill_flag = False
        self.keyboard_input_active = False # variable for toggling keyboard controls
        self.nav_script = "" # placeholder, for str path to navigation script selected for execution
        self.no_signal_frame = cv2.imread("camera_fail.png")
        self.is_holding = False
        self.host_listening = False
        print("[INFO]: Loading configurations...")
        self.components = basics.basics.load_hardware_config()  # [[sensehat, distance, dust], [arm, arm_cam]]
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
            basics.basics.exit(1)
        pass
        self.window.connectbutton.clicked.connect(lambda: comms.connect.connect())
        self.window.disconnectbutton.clicked.connect(lambda: comms.disconnect.disconnect())
        self.window.updateosbutton.clicked.connect(lambda: comms.interface.send(b"rca-1.2:command_update"))
        self.window.shutdownbutton.clicked.connect(lambda: client.os_control_shutdown_wrapper())
        self.window.rebootbutton.clicked.connect(lambda: client.os_control_reboot_wrapper())
        self.window.helpbutton.clicked.connect(lambda: messagebox.showinfo("Raspbot RCA: Control Help", "Use Update OS to update APT packages,\n Shutdown and Reboot perform operations as labeled."
                                                                           + "\nA word of caution, after shutting down, there is no way to turn the bot back on besides physically power cycling.\n Please use cautiously."
                                                                           + "\nChoose a report-type with the dropdown, select Collect Report to as labeled collect the report,\n and either use Save or View Report afterwards."))
        self.window.executebutton.clicked.connect(lambda: client.nav_script_parse(self.nav_script))
        self.window.loadbutton.clicked.connect(lambda: client.nav_load(self))
        self.window.editbutton.clicked.connect(lambda: client.nav_edit())
        self.window.keyboardtogglebutton.clicked.connect(lambda: client.keyboard_input_active_swap(self))
        self.window.navhelpbutton.clicked.connect(lambda: messagebox.showinfo("Raspbot RCA: Navigation Help", "This panel contains navigation controls.\nUse Load, Edit, and Execute to run scripts."
                                                                              + "\nSee documentation regarding how to write these scripts.\nPress Toggle Keyboard Control to enable or disable keyboard controls."
                                                                              + "\nDisconnect, report collection, LED controls, shutdown, reboot, update, motor speed change,\ndock, undock, and navigation script execution are disabled when\nkeyboard input is active."
                                                                              + "\nUse the Change Speed button to enter a number 0-255, 255 being the highest speed and 0 being completely off."
                                                                              + "\n\nKeyboard controls in question are:\nW - Forwards\nA - Left Turn\nS - Backwards\nD - Right Turn\nQ - Clockwise Spin\nE - Counterclockwise Spin"))
        self.window.saveframebutton.clicked.connect(lambda: cv2.imwrite("image-" + basics.basics.make_timestamp(log_suppress = True) + ".jpg", comms.objects.frame_current))
        self.window.collectbutton.clicked.connect(lambda: client.report_collect(self, self.window.typeselect.currentText()))
        self.window.savebutton.clicked.connect(lambda: client.report_save(self, self.window.typeselect.currentText(), self.report_content))
        self.window.viewbutton.clicked.connect(lambda: client.report_gui(self, self.window.typeselect.currentText(), self.report_content))
        self.window.telemetryview.setReadOnly(True)
        self.window.dockbutton.clicked.connect(lambda: comms.interface.send(b"rca-1.2:command_dock"))
        self.window.undockbutton.clicked.connect(lambda: comms.interface.send(b"rca-1.2:command_undock"))
        self.window.changespeedbutton.clicked.connect(lambda: client.nav_request_adjust_speed())
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
        self.window.changespeedbutton.setEnabled(False)
        self.window.show()
        print("[INFO]: Keyboard initializing...")

        class globalsAreForNerds:
            """
            An extremely dirty and depressing hack to get keyboard_listen handlers to accept non-local variables.
            pynput back-end shenanigans and irresponsible use of positional arguments has forced my hand.
            """
            def __init__(self, outer_self): self.outer_self = outer_self

            def keyboard_listen_press_handler(self, key) -> None:
                """
                Event function, called upon keypress event by the keyboard listener under the keyboard listen control forward thread.
                :param key: key pressed, object key.x
                :return: None
                """
                SWITCH = {"w": "forwards", "a": "left", "s": "backwards", "d": "right", "q": "clockwise", "e": "counterclockwise", "r": "stop"}
                try:
                    if self.outer_self.is_holding is False and self.outer_self.keyboard_input_active and self.outer_self.host_listening is True:
                        comms.interface.send(SWITCH[str(key).rstrip("'").lstrip("'")])
                        self.outer_self.is_holding = True
                except KeyError: pass  # KeyError is ignored, this likely will occur when a non-nav-control key is pressed
            pass

            def keyboard_listen_release_handler(self, key) -> Union[None, bool]:
                """
                Wrapper event function, called upon key release event by the keyboard listener.
                :param key: key released, object key.x
                :return: None or False, False upon escape
                """
                SWITCH = {"w": "forwards", "a": "left", "s": "backwards", "d": "right", "q": "clockwise", "e": "counterclockwise", "r": "stop"}

                if self.outer_self.keyboard_input_active is True and self.outer_self.host_listening is True:
                    self.outer_self.is_holding = False
                    if key == Key.esc:
                        comms.interface.send("stop")
                        self.outer_self.keyboard_input_active = False
                        return False
                    else:
                        try:
                            if SWITCH[str(key).rstrip("'").lstrip("'")] is not None: comms.interface.send("stop")
                        except KeyError: return None
                    pass
                pass
            pass
        pass

        handlerInstance = globalsAreForNerds(self)
        self.listener = Listener(on_press = handlerInstance.keyboard_listen_press_handler, on_release = handlerInstance.keyboard_listen_release_handler)
        self.listener.start()
        basics.process.create_process(self.listener.join, ())
        print("[INFO]: Additional threading for main GUI starting...")
        self.process_telemetry_refresh = basics.process.create_process(client.telemetry_refresh, (self,))
        self.process_status_refresh = basics.process.create_process(client.status_refresh, (self,))
        self.process_gui_lock_from_state = basics.process.create_process(client.gui_lock_from_connect_state, (self,))
        self.process_camera_view_refresh_clock = basics.process.create_process(client.camera_view_refresh_clock, (self,))
        self.signal_telemetry_refresh.connect(client.telemetry_refresh_commit)
        self.signal_status_refresh.connect(client.status_refresh_commit)
        self.signal_gui_lock_from_state.connect(client.gui_lock_from_connect_state_commit)
        self.signal_camera_refresh_clock.connect(client.camera_view_commit)
        print("[INFO]: Loading complete.")
        basics.basics.exit(self.app.exec_())
    pass

    def keyboard_input_active_swap(self) -> None:
        """
        Lambda statements cannot be used to assign variables, function instead to be bound to keyboardtogglebutton.
        :return: None
        """
        self.keyboard_input_active = not self.keyboard_input_active
        if self.keyboard_input_active is True and self.host_listening is False:
            print("[INFO]: Entered keyboard navigation.")
            comms.interface.send("rca-1.2:nav_keyboard_start")
            if comms.acknowledge.receive_acknowledgement() is False:
                print("[FAIL]: Failed to enter keyboard navigation! Host did not acknowledge request, exiting state.")
                self.keyboard_input_active = False
            self.host_listening = True
        if self.keyboard_input_active is False and self.host_listening is True:
            comms.interface.send("exit nav input stream")
            self.host_listening = False
            print("[INFO]: Exited keyboard navigation.")
        pass
    pass

    @staticmethod
    def toggle_camera_view_popout() -> None:
        """
        Lambda statements cannot be used to assign variables, function instead tobe bound to menubar's expandcamera option.
        :return: None
        """
        comms.objects.popout_camera_feed = not comms.objects.popout_camera_feed
        if comms.objects.popout_camera_feed is False: cv2.destroyAllWindows()

    def menu_trigger(self, qobj: object) -> None:
        """
        Function for executing menubar selections.
        :param qobj: Qt object
        :return: None
        """
        SWITCH = {"Exit":lambda: basics.basics.exit(0), "Edit Network":lambda: client.edit_gui("comms/comms.cfg", "comms.cfg"), "Edit Hardware":lambda: client.edit_gui("hardware.cfg", "hardware.cfg"), "Edit Main":lambda: client.edit_gui("main.cfg", "main.cfg"), "Ping": lambda: client.ping_gui(self), "SenseHAT LEDs":lambda: client.led_gui(self), "Arm Control":lambda: client.arm_control_gui(self), "View Documentation":lambda: Popen("python3 webhelper.py https://dreamerslegacy.xyz/projects/raspbot/docs.html"), "Visit Github Repo":lambda: Popen("python3 webhelper.py https://github.com/perpetualCreations/raspbot-rca/"), "Expand Camera":lambda: client.toggle_camera_view_popout()}
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
            self.window.changespeedbutton.setEnabled(True)
            if docked is False:
                self.window.undockbutton.setEnabled(False)
                self.window.dockbutton.setEnabled(True)
                self.window.keyboardtogglebutton.setEnabled(True)
                self.window.executebutton.setEnabled(True)
            else:
                self.window.dockbutton.setEnabled(False)
                self.window.undockbutton.setEnabled(True)
                self.window.keyboardtogglebutton.setEnabled(False)
                self.window.executebutton.setEnabled(False)
                self.keyboard_input_active = False
            pass
            if self.keyboard_input_active is True:
                self.window.disconnectbutton.setEnabled(False)
                self.window.collectbutton.setEnabled(False)
                self.window.shutdownbutton.setEnabled(False)
                self.window.rebootbutton.setEnabled(False)
                self.window.updateosbutton.setEnabled(False)
                self.window.dockbutton.setEnabled(False)
                self.window.undockbutton.setEnabled(False)
                self.window.executebutton.setEnabled(False)
                self.window.changespeedbutton.setEnabled(False)
            else:
                self.window.disconnectbutton.setEnabled(True)
                self.window.collectbutton.setEnabled(True)
                self.window.shutdownbutton.setEnabled(True)
                self.window.rebootbutton.setEnabled(True)
                self.window.updateosbutton.setEnabled(True)
                self.window.dockbutton.setEnabled(True)
                self.window.undockbutton.setEnabled(True)
                self.window.executebutton.setEnabled(True)
                self.window.changespeedbutton.setEnabled(True)
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
            self.window.changespeedbutton.setEnabled(False)
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
            previous_connect = comms.objects.is_connected
            previous_dock = comms.objects.dock_status
            previous_keyboard = self.keyboard_input_active
            sleep(1)
            if previous_connect != comms.objects.is_connected or previous_dock != comms.objects.dock_status or previous_keyboard != self.keyboard_input_active: self.signal_gui_lock_from_state.emit(self, comms.objects.is_connected, comms.objects.dock_status)
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

    # noinspection PyBroadException
    def telemetry_refresh(self) -> None:
        """
        Produces signal and string for telemetry refresh. Intended solely for multithreading.
        :return: None
        """
        print("[INFO]: Telemetry refresh thread started.")
        while comms.objects.process_telemetry_refresh_kill_flag is False:
            while comms.objects.is_connected is False: pass
            try:
                self.signal_telemetry_refresh.emit(self, comms.interface.receive(socket_object = comms.objects.socket_telemetry).decode(encoding = "utf-8", errors = "replace"))
                comms.interface.send("rca-1.2:ok", socket_object = comms.objects.socket_telemetry)
            except BaseException: # no john, I'm not going to write 60 exception clauses for every possible error that could occur at runtime, when they're all going to do the same thing
                print("[FAIL]: Telemetry stream raised exception. Host has disconnected/failed abruptly.")
                comms.disconnect.disconnect()
                self.keyboard_input_active = False
            pass
        pass
        print("[INFO]: Telemetry refresh thread ended.")

    @Slot(str, str, bool, bool)
    def status_refresh_commit(self, connect: str, dock: str, error: bool, keyboard: bool) -> None:
        """
        Refreshes status display.
        :param connect: return of SWITCH_CONNECT[comms.objects.is_connected]
        :param dock: return of SWITCH_DOCK[comms.objects.dock_status]
        :param error: bool, if True set status as "Unknown status"
        :param keyboard: bool, if True, set keyboardstatuslabel to "Keyboard control enabled."
        :return: None
        """
        if error is not True: self.window.status.setText(connect + ", currently " + dock + ".")
        else: self.window.status.setText("Unknown status.")
        if keyboard is True: self.window.keyboardstatuslabel.setText("Keyboard control enabled.")
        else: self.window.keyboardstatuslabel.setText("Keyboard control disabled.")
        if isinstance(self.nav_script, str) is True: self.window.scriptlabel.setText(self.nav_script)

    def status_refresh(self) -> None:
        """
        Produces signal and strings for status refresh. Intended solely for multithreading.
        :return: None
        """
        print("[INFO]: Status refresh thread started.")
        SWITCH_CONNECT = {False:"Disconnected", True:"Connected"}
        SWITCH_DOCK = {False:"undocked", True:"docked", None:"dock status is unknown"}
        while self.process_status_refresh_kill_flag is False:
            try: self.signal_status_refresh.emit(self, SWITCH_CONNECT[comms.objects.is_connected], SWITCH_DOCK[comms.objects.dock_status], False, self.keyboard_input_active)
            except KeyError: self.signal_status_refresh.emit("UNKNOWN", "UNKNOWN", True, self.keyboard_input_active)
            sleep(1)
        pass
        print("[INFO]: Status refresh thread ended.")

    @Slot(object)
    def camera_view_commit(self) -> None:
        """
        Converts OpenCV image object to QImage, forwards changes to camera view widget.
        :return: None
        """
        try: image = cv2.cvtColor(comms.objects.frame_current, cv2.COLOR_BGR2RGB)
        except cv2.error: image = cv2.cvtColor(self.no_signal_frame, cv2.COLOR_BGR2RGB) # exception usually occurs if source is empty, this just replaces camera image with an error message
        self.window.cameraview.setPixmap(QPixmap.fromImage(QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888))) # ignore warnings, this actually runs just fine with no errors
        if comms.objects.popout_camera_feed is True:
            cv2.imshow("Raspbot RCA: Expanded Camera Feed", comms.objects.frame_current)

    def camera_view_refresh_clock(self) -> None:
        """
        Checks comms.object.camera_tick, if value is greater than previous value, emit signal to commit frame.
        As the name of the function suggests, this serves as a "clock signal" for updating the camera view.
        Intended for multithreading.
        :return: None
        """
        print("[INFO]: Camera view refresh clock thread started.")
        while self.process_camera_view_refresh_clock_kill_flag is False:
            while comms.objects.is_connected is False: pass
            if comms.objects.camera_updated is True:
                self.signal_camera_refresh_clock.emit(self)
                comms.objects.camera_updated = False
        print("[INFO]: Camera view refresh clock thread ended.")

    @staticmethod
    def gui_dialog_loader(ui_file: str) -> Union[object, None]:
        """
        Creates QDialog from given UI file, initializes and starts window, returns QDialog object.
        :param ui_file: str, path or filename of UI file
        :return: QDialog
        """
        ui_file = QFile(ui_file)
        if not ui_file.open(QIODevice.ReadOnly):
            print("[FAIL]: UI XML file is not in read-only. Is it being edited by another application?")
            return None
        pass
        loader = QUiLoader()
        dialog = loader.load(ui_file)
        ui_file.close()
        dialog.setWindowIcon(QIcon("favicon.ico"))  # it just works
        if not dialog:
            print("[FAIL]: UI XML file could not be loaded to generate interface.")
            print(dialog.errorString())
            return None
        pass
        dialog.show()
        return dialog

    @staticmethod
    def edit_gui(file: str, edit_type: str) -> None:
        """
        Starts the EDIT dialog to open a file and allow the user to edit it.
        :param file: str, path to file or if in working directory, filename
        :param edit_type: str, type of file, configuration or navscript, configurations should be named
        :return: None
        """
        print("[INFO]: Displayed edit_gui, with params for " + file + " and type " + edit_type + ".")
        edit_gui = client.gui_dialog_loader("edit.ui")
        edit_gui.editor.setReadOnly(False)
        edit_gui.closebutton.clicked.connect(lambda: edit_gui.close())
        edit_gui.filelabel.setText("Currently editing: " + edit_type)

        def wrapper() -> None:
            """
    `       Wrapper function nested in edit_gui.
            Checks if editor is empty, returns None. If not, write to file.
            If the file that already exists, move old file to file_name.file_extension.old.
            If a .old file already exists, overwrite previous .old file.
            """
            if edit_gui.editor.toPlainText() == "": return None
            else:
                if path.isfile(file) is True:
                    if path.isfile(file + ".old") is True: remove(file + ".old")
                    rename(file, file + ".old")

                with open(file, "w") as write_handle: write_handle.write(edit_gui.editor.toPlainText())

        try:
            with open(file) as read_handle: edit_gui.editor.setPlainText(read_handle.read())
        except FileNotFoundError: edit_gui.editor.setPlainText("")
        edit_gui.savebutton.clicked.connect(lambda: wrapper())

    @staticmethod
    def ping() -> list:
        """
        Pings host address and records latency and losses.
        :return: average latency, nested list with individual latency values, total losses, nested list with individual losses, if host resolution failed
        """
        print("[INFO]: Starting PING test...")
        scans = [ping3.ping(comms.objects.host, timeout = 5, size = 64, unit = "ms"), ping3.ping(comms.objects.host, timeout = 5, size = 64, unit = "ms"), ping3.ping(comms.objects.host, timeout = 5, size = 64, unit = "ms"), ping3.ping(comms.objects.host, timeout = 5, size = 64, unit = "ms")]
        if None in scans or False in scans:
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
            print(scans)
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
            self.ping_results = "Unable to resolve hostname," + "\n" + "is the NET configuration correct, or is the host down?" + "\n" + "Host IP was:" + "\n" + comms.objects.host
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
    pass

    def ping_gui(self) -> None:
        """
        GUI tool for pinging IP addresses.
        :return: None
        """
        print("[INFO]: Displayed ping_gui.")
        ping_gui = client.gui_dialog_loader("ping.ui")
        ping_gui.pingview.setReadOnly(True)

        def wrapper() -> None:
            """
            Wrapper function nested in ping_gui.
            When called, calls client.ping_wrapper(self) and also updates ping_gui.pingview.
            :return:
            """
            if client.ping_wrapper(self) is None: ping_gui.pingview.setPlainText(self.ping_results) # this waits until client.ping_wrapper returns None, effectively delaying setPlainText until the results have been gathered

        ping_gui.closebutton.clicked.connect(lambda: ping_gui.close())
        ping_gui.savebutton.clicked.connect(lambda: client.report_save(self, "PING", self.ping_results))
        ping_gui.pingbutton.clicked.connect(lambda: wrapper())
    pass

    def nav_load(self):
        """
        Shows Enter Path dialog, vets user input before dumping entry to self.nav_script.
        :return: None
        """
        print("[INFO]: Displayed nav_load dialog.")
        nav_load_gui = client.gui_dialog_loader("selectpath.ui")

        def wrapper() -> None:
            """
            Wrapper function nested in nav_load_gui.
            When called, gets entry input and checks if target is a valid file, and ends with .navscript.
            If both conditions are True, cache path to self.nav_script and close dialog.
            :return: None
            """
            if path.isfile(nav_load_gui.pathentry.text()) is True:
                if nav_load_gui.pathentry.text().endswith(".navscript") is True:
                    self.nav_script = nav_load_gui.pathentry.text()
                    nav_load_gui.close()
                else: messagebox.showerror("Raspbot RCA: Nav Script Error", "Selected file is not a navigation script, the accepted file extension is .navscript.")
            else: messagebox.showerror("Raspbot RCA: Nav Script Error", "Selected file does not exist. Did you mistype the path?")

        nav_load_gui.closebutton.clicked.connect(lambda: nav_load_gui.close())
        nav_load_gui.confirmbutton.clicked.connect(lambda: wrapper())

    @staticmethod
    def nav_edit():
        """
        Shows Enter Path dialog, vets user input before opening it with client.edit_gui.
        :return: None
        """
        print("[INFO]: Displayed nav_edit path dialog.")
        nav_edit_gui = client.gui_dialog_loader("selectpath.ui")
        nav_edit_gui.dialoglabel.setText("Enter path to file being edited or created.")

        def wrapper() -> None:
            """
            Wrapper function nested in nav_edit_gui.
            When called, gets entry input and checks if target is in valid directory.
            If True, if target does not end with .navscript file extension, append extension to target.
            Forward target to client.edit_gui and close dialog after.
            :return: None
            """
            if path.isdir(path.split(nav_edit_gui.pathentry.text())[0]) is True:
                target = nav_edit_gui.pathentry.text()
                if target.endswith(".navscript") is not True: target += ".navscript"
                client.edit_gui(target, "nav script")
                nav_edit_gui.close()
            else: messagebox.showerror("Raspbot RCA: Nav Script Error", "Path is not valid. Did you mistype it?")

        nav_edit_gui.closebutton.clicked.connect(lambda: nav_edit_gui.close())
        nav_edit_gui.confirmbutton.clicked.connect(lambda: wrapper())

    def report_collect(self, report_type: str) -> None:
        """
        Sends a report request to host with given type and sets self.report_content with results.
        :param report_type: type of report.
        :return: None
        """
        if report_type == "Science":
            if self.components[0][0] is True or self.components[0][2] is True:
                comms.interface.send(b"rca-1.2:command_science_collect")
                if comms.acknowledge.receive_acknowledgement() is False: return None
                self.report_content = comms.interface.receive().decode(encoding = "utf-8", errors = "replace")
            else: return None
        elif report_type == "Hardw.":
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
        report_gui = client.gui_dialog_loader("reportview.ui")
        report_gui.setWindowTitle("Raspbot RCA: View Report - " + report_type)
        report_gui.reportdisplay.setReadOnly(True)
        report_gui.reportdisplay.setPlainText(content)
        report_gui.closebutton.clicked.connect(lambda: report_gui.close())
        report_gui.savebutton.clicked.connect(lambda: client.report_save(self, report_type, content))
    pass

    def report_save(self, report_type: str, content: str) -> None:
        """
        Saves a report with given type and contents.
        :param report_type: type of report.
        :param content: report contents to be saved.
        :return: None
        """
        if self.report_content == "" and report_type != "PING": return None
        if self.ping_results == "" and report_type == "PING": return None
        file_report_name = report_type + "_report-" + basics.basics.make_timestamp() + ".txt"
        print("[INFO]: Generating text file report...")
        with open(file_report_name, "w+") as file_report: file_report.write(content)
        print("[INFO]: Report saved.")
    pass

    @staticmethod
    def dock() -> None:
        """
        Instructs host to dock with charger station.
        :return: None
        """
        if messagebox.askyesno("Raspbot RCA: Docking", "Plug in the external power supply through the two exposed pins."
                                                       "\nPress Yes to continue once you've plugged in the external power supply,"
                                                       "\nPress No to cancel."
                                                       "\n\nConfirming this operation while unplugged will result in the onboard Raspi shutting down, and requiring recovery.") is True: pass
        else: return None
        print("[INFO]: Docking...")
        comms.interface.send(b"rca-1.2:command_dock")
        if comms.acknowledge.receive_acknowledgement() is False: return None
        comms.objects.dock_status = True
    pass

    @staticmethod
    def undock() -> None:
        """
        Instructs host to undock from charger station.
        :return: None
        """
        if messagebox.askyesno("Raspbot RCA: Undocking", "Unplug the external power supply from the two exposed pins."
                                                         "\nPress Yes to continue once you've unplugged the external power supply,"
                                                         "\nPress No to cancel."
                                                         "\n\nNavigation will be re-enabled once undocked. \nBe sure the power supply is not obstructing or attached to the vehicle before executing navigation.") is True: pass
        else: return None
        print("[INFO]: Undocking...")
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
        if self.components[0][0] is not True or self.keyboard_input_active is True: return None
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
        return None # TODO integrated arm hardware
    pass

    @staticmethod
    def nav_request_adjust_speed() -> None:
        """
        Shows Enter Speed dialog, accepts entry input.
        Checks if input can be converted to an integer 0-255. Make request to host and forward speed if so.
        :return:
        """
        print("[INFO]: Displayed enter_speed dialog.")
        nav_request_adjust_speed_gui = client.gui_dialog_loader("specifymotorspeed.ui")

        def wrapper() -> None:
            """
            Wrapper function nested in nav_request_adjust_speed_gui.
            When called, gets entry input and checks if input is an integer 0-255.
            Make request to host as specified in previous docstring.
            :return: None
            """
            try:
                if int(nav_request_adjust_speed_gui.intentry.text()) in range(0, 256):
                    comms.interface.send("rca-1.2:nav_speed_change")
                    if comms.acknowledge.receive_acknowledgement() is False: return None
                    comms.interface.send(str(int(nav_request_adjust_speed_gui.intentry.text())))
                    nav_request_adjust_speed_gui.close()
                else: messagebox.showerror("Raspbot RCA: Input Motor Speed Error", "Given motor speed is not between 0 to 255. Check your input.")
            except ValueError: messagebox.showerror("Raspbot RCA: Input Motor Speed Error", "Given motor speed is not a number. Check your input.")

        nav_request_adjust_speed_gui.closebutton.clicked.connect(lambda: nav_request_adjust_speed_gui.close())
        nav_request_adjust_speed_gui.confirmbutton.clicked.connect(lambda: wrapper())

    @staticmethod
    def nav_execute(direction: str, run_time: Union[str, int]) -> None:
        """
        Wrapper for client.send(), formats instructions and does hardware check for distance sensor.
        Only used by client.nav_script_parse.
        :param direction: direction of navigation.
        :param run_time: amount of time to run motors in that direction.
        :return: None
        """
        comms.interface.send("rca-1.2:nav_start")
        if comms.acknowledge.receive_acknowledgement() is False: return None
        if isinstance(run_time, int) is True: run_time = str(run_time)
        comms.interface.send(direction + " " + run_time)
        if comms.acknowledge.receive_acknowledgement() is False: return None
    pass

    @staticmethod
    def nav_script_parse(file_name: str) -> None:
        """
        Reads from a given file line-by-line for instructions, and executes them through client.nav_execute().
        Reads syntax as <NAV DIRECTION/ACTION> <RUN TIME>. It looks similar to GCODE-style syntax. Telemetry is enabled when hardware passes, cannot be custom.
        Example of syntax: F 100
        :param file_name: str, name of file to read from.
        :return: None
        """
        with open(file_name) as script_handle: instructions = script_handle.read()
        instructions = instructions.split("\n")
        for x in range(0, len(instructions)):
            try:
                client.nav_execute(instructions[x].split()[0], instructions[x].split()[1])
                sleep(int(instructions[x].split()[1]))
            except IndexError:
                messagebox.showerror("Raspbot RCA: Nav Script Error", "Nav script raised an error while executing. Check syntax.")
                return None
            pass
        pass
    pass
pass

if __name__ == "__main__": client()
