"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
# Made by Taian Chen
"""

try:
    print("[INFO]: Starting imports...")
    from subprocess import call, Popen
    from time import sleep, strftime, gmtime
    import socket, configparser, multiprocessing, tkinter, ping3, imagezmq, cv2
    from tkinter import messagebox
    from ast import literal_eval
    # RCA Modules
    import basics, comms, nav
    from platform import system
except ImportError as e:
    literal_eval = None
    sleep = None
    Popen = None
    strftime = None
    gmtime = None
    tkinter = None
    messagebox = None
    call = None
    socket = None
    configparser = None
    multiprocessing = None
    ping3 = None
    cv2 = None
    imagezmq = None
    # RCA Modules
    basics = None
    comms = None
    nav = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class client:
    """
    Main client class.
    """
    def __init__(self):
        """
        Initiation function of Raspbot RCA.
        """
        print("[INFO]: Starting client Raspbot RC Application...")
        print("[INFO]: Declaring variables...")
        self.connect_retries = 0
        self.components = [[None], [None, None, None], [None], [None, None]] # [Base Set [cam], RFP Enceladus [sensehat, distance, dust], Upgrade #1 [charger], Robotic Arm Kit [arm, arm_cam]]
        self.ping_text = None
        self.ping_button = None
        self.ping_results = ""
        self.report_content = ""
        print("[INFO]: Loading configurations...")
        config_parse_load = configparser.ConfigParser()
        try:
            config_parse_load.read("hardware.cfg")
            self.components[0][0] = literal_eval(config_parse_load["HARDWARE"]["cam"])
            self.components[1][0] = literal_eval(config_parse_load["HARDWARE"]["sensehat"])
            self.components[1][1] = literal_eval(config_parse_load["HARDWARE"]["distance"])
            self.components[1][2] = literal_eval(config_parse_load["HARDWARE"]["dust"])
            self.components[2][0] = literal_eval(config_parse_load["HARDWARE"]["charger"])
            self.components[3][0] = literal_eval(config_parse_load["HARDWARE"]["arm"])
            self.components[3][1] = literal_eval(config_parse_load["HARDWARE"]["arm_cam"])
        except configparser.Error as ce:
            print("[FAIL]: Failed to load configurations! See below for details.")
            print(ce)
        except FileNotFoundError as nf:
            print("[FAIL]: Failed to load configurations! Configuration file is missing.")
            print(nf)
        pass
        print("[INFO]: Starting GUI...")
        self.root = tkinter.Tk()
        self.root.title("Raspbot RCA: Client")
        self.root.configure(bg = "#344561")
        self.root.geometry('{}x{}'.format(1200, 530))
        self.root.resizable(width=False, height=False)
        menu = tkinter.Menu(self.root)
        self.root.config(menu = menu)
        app_menu = tkinter.Menu(menu)
        hardware_menu = tkinter.Menu(app_menu)
        base_set_menu = tkinter.Menu(hardware_menu)
        base_set_menu.add_command(label = "Enable", command = lambda: basics.basics.set_configuration(self.components[0][0], True, "HARDWARE", "cam", False))
        base_set_menu.add_command(label = "Disable", command = lambda: basics.basics.set_configuration(self.components[1][0], False, "HARDWARE", "cam", False))
        rfp_enceladus_menu = tkinter.Menu(hardware_menu)
        rfp_enceladus_menu.add_command(label = "Enable", command = lambda: basics.basics.set_configuration([self.components[1][0], self.components[1][1], self.components[1][2]], [True, True, True], ["HARDWARE", "HARDWARE", "HARDWARE"], ["sensehat", "distance", "dust"], True))
        rfp_enceladus_menu.add_command(label = "Disable", command = lambda: basics.basics.set_configuration([self.components[1][0], self.components[1][1], self.components[1][2]], [False, False, False], ["HARDWARE", "HARDWARE", "HARDWARE"], ["sensehat", "distance", "dust"], True))
        upgrade_1_menu = tkinter.Menu(hardware_menu)
        upgrade_1_menu.add_command(label = "Enable", command = lambda: basics.basics.set_configuration(self.components[2][0], True, "HARDWARE", "charger", False))
        upgrade_1_menu.add_command(label = "Disable", command = lambda: basics.basics.set_configuration(self.components[2][0], False, "HARDWARE", "charger", False))
        hardware_menu.add_cascade(label = "Base Set", menu = base_set_menu)
        hardware_menu.add_cascade(label = "RFP Enceladus", menu = rfp_enceladus_menu)
        hardware_menu.add_cascade(label = "Upgrade #1", menu = upgrade_1_menu)
        app_menu.add_command(label = "Edit Configs", command = lambda: client.set_configuration_gui())
        app_menu.add_cascade(label = "Edit Hardware Set", menu = hardware_menu)
        app_menu.add_command(label = "AquaSilva Ops", command = None)
        app_menu.add_command(label = "Exit", command = lambda: basics.basics.exit(0))
        menu.add_cascade(label = "App", menu = app_menu)
        net_menu = tkinter.Menu(menu)
        net_tools_menu = tkinter.Menu(net_menu)
        net_tools_menu.add_command(label = "Ping", command = lambda: client.ping_gui(self))
        net_menu.add_cascade(label = "Tools", menu = net_tools_menu)
        menu.add_cascade(label = "Net", menu = net_menu)
        addon_menu = tkinter.Menu(menu)
        addon_menu.add_command(label = "SenseHAT LEDs", command = lambda: client.led_gui(self))
        if self.components[3][0] is True:
            addon_menu.add_command(label = "Arm Control", command = lambda: client.arm_control_gui(self))
        pass
        menu.add_cascade(label = "Add-Ons", menu = addon_menu)
        vitals_frame = tkinter.Frame(self.root, bg = "#506a96", highlightthickness = 2, bd = 0, height = 50, width = 60)
        vitals_frame.grid(row = 0, column = 0, padx = (10, 0), pady = (15, 0))
        vitals_label = tkinter.Label(vitals_frame, bg = "#506a96", fg = "white", text = "Bot Vitals", font = ("Calibri", 12))
        vitals_label.grid(row = 0, column = 0, padx = (5, 0))
        self.vitals_text = tkinter.Text(vitals_frame, bg = "white", fg = "black", state = tkinter.DISABLED, height = 10, width = 50, font = ("Calibri", 10))
        self.vitals_text.grid(row = 1, column = 0, padx = (5, 5), pady = (10, 0))
        vitals_refresh_button = tkinter.Button(vitals_frame, text = "Refresh", bg = "white", fg = "black", command = lambda: client.vitals_refresh(self, False))
        vitals_refresh_button.grid(row = 2, column = 0, padx = (5, 5), pady = (10, 5))
        cam_view_frame = tkinter.Frame(self.root, bg = "#506a96", highlightthickness = 2, bd = 0)
        cam_view_frame.grid(row = 0, column = 2, padx = (10, 0), pady = (15, 0))
        multi_frame = tkinter.Frame(self.root, bg = "#344561")
        multi_frame.grid(row = 1, column = 0, padx = (10, 0), pady = (10, 0))
        net_frame = tkinter.Frame(multi_frame, bg = "#506a96", highlightthickness = 2, bd = 0)
        net_frame.grid(row = 0, column = 0, padx = (0, 5))
        net_label = tkinter.Label(net_frame, bg = "#506a96", fg = "white", text = "Network", font = ("Calibri", 12))
        net_label.grid(row = 0, column = 0, padx = (5, 0))
        self.net_status_data = tkinter.StringVar()
        self.net_status_data.set("Status: " + "Disconnected")
        net_status_label = tkinter.Label(net_frame, bg = "#506a96", fg = "white", textvariable = self.net_status_data, font = ("Calibri", 12))
        net_status_label.grid(row = 1, column = 0, padx = (5, 0), pady = (10, 0))
        net_disconnect_button = tkinter.Button(net_frame, bg = "white", fg = "black", text = "Disconnect", font = ("Calibri", 12), width = 10, height = 1, command = lambda: comms.disconnect.disconnect())
        net_disconnect_button.grid(row = 2, column = 0, padx = (5, 0), pady = (10, 0))
        net_connect_button = tkinter.Button(net_frame, bg = "white", fg = "black", text = "Connect", font = ("Calibri", 12), width = 10, height = 1, command = lambda: comms.connect.connect())
        net_connect_button.grid(row = 3, column = 0, padx = (5, 0))
        net_help_button = tkinter.Button(net_frame, bg = "#506a96", fg = "white", text = "?", width = 1, height = 1, font = ("Calibri", 10), command = lambda: messagebox.showinfo("Raspbot RCA: Net Help", "This panel controls your network connection with the bot. See the NET options in menu bar for additional tools and actions."))
        net_help_button.grid(row = 4, column = 0, padx = (5, 150), pady = (71, 5))
        report_frame = tkinter.Frame(multi_frame, bg = "#506a96", highlightthickness = 2, bd = 0)
        report_frame.grid(row = 0, column = 2, padx = (5, 0))
        report_label = tkinter.Label(report_frame, bg = "#506a96", fg = "white", text = "Reports", font = ("Calibri", 12))
        report_label.grid(row = 0, column = 0, padx = (5, 0))
        report_type_list = [
            "None",
            "CH Check",
            "Science"
        ]
        report_type_data = tkinter.StringVar(report_frame)
        report_type_data.set(report_type_list[0])
        report_dropdown = tkinter.OptionMenu(report_frame, report_type_data, report_type_list[0], report_type_list[1], report_type_list[2])
        report_dropdown.configure(width = 7)
        report_dropdown.grid(row = 1, column = 0, padx = (5, 0), pady = (10, 0))
        report_collect_button = tkinter.Button(report_frame, bg = "white", fg = "black", text = "Collect", font = ("Calibri", 12), width = 10, command = lambda: client.report_collect(self, report_type_data.get()))
        report_collect_button.grid(row = 2, column = 0, padx = (5, 0), pady = (5, 0))
        report_view_button = tkinter.Button(report_frame, bg = "white", fg = "black", text = "View", font = ("Calibri", 12), width = 10, command = lambda: client.report_gui(self, report_type_data.get(), self.report_content))
        report_view_button.grid(row = 3, column = 0, padx = (5, 0), pady = (5, 0))
        report_save_button = tkinter.Button(report_frame, bg = "white", fg = "black", text = "Save", font = ("Calibri", 12), width = 10, command = lambda: client.report_save(self, report_type_data.get(), self.report_content))
        report_save_button.grid(row = 4, column = 0, padx = (5, 0), pady = (5, 0))
        report_help_button = tkinter.Button(report_frame, bg = "#506a96", fg = "white", text = "?", width = 1, height = 1, font = ("Calibri", 10), command = lambda: messagebox.showinfo("Raspbot RCA: Report Help", "This panel allows you to request, view, and save reports of a vareity of types. These include computer hardware checks (CH Check) and science reports (Science, RFP Enceladus)."))
        report_help_button.grid(row = 5, column = 0, padx = (5, 150), pady = (22, 7))
        control_frame = tkinter.Frame(self.root, bg = "#344561")
        control_frame.grid(row = 1 , column = 3, padx = (5, 0))
        os_control_frame = tkinter.Frame(control_frame, bg = "#506a96", highlightthickness = 2, bd = 0)
        os_control_frame.grid(row = 0, column = 0, pady = (10, 0))
        os_control_update_button = tkinter.Button(os_control_frame, bg = "white", fg = "black", text = "Update OS", height = 1, width = 10, font = ("Calibri", 12), command = lambda: comms.interface.send(b"command_update"))
        os_control_update_button.grid(row = 0, column = 0, padx = (5, 5), pady = (40, 5))
        os_control_shutdown_button = tkinter.Button(os_control_frame, bg = "white", fg = "black", text = "Shutdown", height = 1, width = 10, font = ("Calibri", 12), command = lambda: client.os_control_shutdown_wrapper(self))
        os_control_shutdown_button.grid(row = 1, column = 0, padx = (5, 5), pady = (0, 5))
        os_control_reboot_button = tkinter.Button(os_control_frame, bg = "white", fg = "black", text = "Reboot", height = 1, width = 10, font = ("Calibri", 12), command = lambda: comms.interface.send(b"command_reboot"))
        os_control_reboot_button.grid(row = 2, column = 0, padx = (5, 5), pady = (0, 10))
        os_control_notice_button = tkinter.Button(os_control_frame, bg = "#506a96", fg = "white", text = "!", height = 1, width = 1, command = lambda: messagebox.showinfo("Raspbot RCA: OS Command Notice", "When using this panel's functions, please note that:" + "\n" + "1. OS Update assumes that your host OS is Debian or Debian-based, and updates through APT." + "\n" + "2. Shutdown and reboot uses Linux's built-in functions to do so through shell." + "\n" + "3. After shutting down, there is no way to turn the bot back on besides cutting and restoring power. Please use cautiously."))
        os_control_notice_button.grid(row = 3, column = 0, padx = (1, 80), pady = (50, 2))
        nav_control_frame = tkinter.Frame(control_frame, bg = "#506a96", highlightthickness = 2, bd = 0)
        nav_control_frame.grid(row = 0, column = 1, padx = (10, 0))
        nav_control_label = tkinter.Label(nav_control_frame, bg = "#506a96", fg = "white", text = "Navigation", font = ("Calibri", 12))
        nav_control_label.grid(row = 0, column = 0, padx = (10, 20), pady = (5, 0))
        nav_control_help = tkinter.Button(nav_control_frame, bg = "#506a96", fg = "white", text = "?", font = ("Calibri", 10), command = lambda: messagebox.showinfo("Raspbot RCA: Nav Help", "This panel allows you to control the bot's movement through selections." + "\n" + "To chose a direction or action, select an option from the dropdown menu, and then enter the number of seconds the motors should be run." + "\n" + "Alternatively, you can create and load navigations through the buttons below Execute Nav. These create another interface for you to write scripts and load them." + "\n" + "It should be noted in some cases navigation will be unavailable (i.e when charging)."))
        nav_control_help.grid(row = 1, column = 0, padx = (0, 60))
        nav_task_list = [
            "None",
            "Forwards",
            "Backwards",
            "Left Forwards",
            "Left Backwards",
            "Right Forwards",
            "Right Backwards",
            "Spin Clockwise",
            "Spin Counterclockwise"
        ]
        nav_type_data = tkinter.StringVar(nav_control_frame)
        nav_type_data.set(nav_task_list[0])
        nav_control_task_dropdown = tkinter.OptionMenu(nav_control_frame, nav_type_data, nav_task_list[0], nav_task_list[1], nav_task_list[2], nav_task_list[3], nav_task_list[4], nav_task_list[5], nav_task_list[6], nav_task_list[6], nav_task_list[7], nav_task_list[8])
        nav_control_task_dropdown.configure(width = 15)
        nav_control_task_dropdown.grid(row = 1, column = 1, padx = (10, 10), pady = (0, 10))
        nav_control_time_entry_data = tkinter.StringVar(nav_control_frame)
        nav_control_time_entry_entry = tkinter.Entry(nav_control_frame, bg = "white", fg = "black", textvariable = nav_control_time_entry_data, width = 15, font = ("Calibri", 12))
        nav_control_time_entry_entry.grid(row = 2, column = 1, padx = (10, 10))
        nav_control_script_frame = tkinter.Frame(nav_control_frame, bg = "#506a96")
        nav_control_script_frame.grid(row = 3, column = 1, padx = (10, 10), pady = (18, 18))
        nav_control_execute_button = tkinter.Button(nav_control_script_frame, bg = "white", fg = "black", text = "Execute Nav", height = 1, width = 15, font = ("Calibri", 12), command = lambda: client.nav_execute(self, nav_type_data.get(), float(nav_control_time_entry_data.get()))) # TODO after completing nav module please change these
        nav_control_execute_button.grid(row = 0, column = 0)
        nav_control_load_button = tkinter.Button(nav_control_script_frame, bg = "white", fg = "black", text = "Load Navigation", height = 1, width = 15, font = ("Calibri", 12), command = lambda: client.nav_load_gui(self))
        nav_control_load_button.grid(row = 1, column = 0, pady = (5, 0))
        nav_control_edit_button = tkinter.Button(nav_control_script_frame, bg = "white", fg = "black", text = "Edit Navigation", height = 1, width = 15, font = ("Calibri", 12), command = lambda: client.nav_edit())
        nav_control_edit_button.grid(row = 2, column = 0, pady = (5, 0))
        self.root.mainloop()
    pass
    def vitals_refresh(self, loop):
        """
        Requests bot vitals.
        :param loop: boolean input deciding whether the function should loop. Enable only for multiprocessing.
        :return: none.
        """
        if loop is True:
            while True:
                comms.interface.send(b"rca-1.2:vitals_request")
                reply = comms.interface.receive()
                vitals_text_data = reply.decode(encoding = "utf-8", errors = "replace")
                self.vitals_text.configure(state = tkinter.NORMAL)
                self.vitals_text.delete("1.0", tkinter.END)
                self.vitals_text.insert("1.0", vitals_text_data)
                self.vitals_text.update_idletasks()
                self.vitals_text.configure(state = tkinter.DISABLED)
            pass
        else:
            comms.interface.send(b"rca-1.2:vitals_request")
            reply = comms.interface.receive()
            vitals_text_data = reply.decode(encoding = "utf-8", errors = "replace")
            self.vitals_text.configure(state = tkinter.NORMAL)
            self.vitals_text.delete("1.0", tkinter.END)
            self.vitals_text.insert("1.0", vitals_text_data)
            self.vitals_text.update_idletasks()
            self.vitals_text.configure(state = tkinter.DISABLED)
        pass
        sleep(1)
    pass
    @staticmethod
    def set_configuration_gui():
        """
        Either opens nano text editor for Linux systems or will open OS' built-in text editor if not Linux.
        In the future, does exactly what client.set_configuration does, but with a GUI window.

        TODO update set_configuartion_gui to tkinter GUI
        """
        platform = system()
        if platform in ["Linux", "Ubuntu", "Debian", "Raspbian", "Kubuntu", "Arch", "Arch Linux", "Fedora", "Linux Mint"]:
            call("sudo nano main.cfg", shell = True)
        elif platform == "Windows":
            Popen(["notepad.exe", "main.cfg"])
        else:
            messagebox.showerror("Raspbot RCA: OS Unsupported", "Client OS is unsupported, please manually edit configuration! The accepted operating systems are Linux and Linux distributions, and Windows. If you believe this is a mistake please open an issue on the repository page.")
        pass
    pass
    def ping(self):
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
    def ping_wrapper(self):
        """
        Wrapper for client.ping() for ping_gui.
        :return: none
        """
        ping_results_raw = client.ping(self)
        if ping_results_raw[4] is True:
            self.ping_results = "Unable to resolve hostname," + "\n" + "is the NET configuration correct?" + "\n" + "Host IP was:" + "\n" + comms.objects.host
        else:
            ping_results_raw[0] = round(ping_results_raw[0], 2)
            ping_results_raw[1][0] = round(ping_results_raw[1][0], 2)
            ping_results_raw[1][1] = round(ping_results_raw[1][1], 2)
            ping_results_raw[1][2] = round(ping_results_raw[1][2], 2)
            ping_results_raw[1][3] = round(ping_results_raw[1][3], 2)
            if ping_results_raw[3][0] is True:
                ping_results_raw[1][0] = "Timed out!"
            elif ping_results_raw[3][1] is True:
                ping_results_raw[1][1] = "Timed out!"
            elif ping_results_raw[3][2] is True:
                ping_results_raw[1][2] = "Timed out!"
            elif ping_results_raw[3][3] is True:
                ping_results_raw[1][3] = "Timed out!"
            pass
            self.ping_results = "Average Latency (ms): " + str(ping_results_raw[0]) + "\n" + "Test 1 Latency: " + str(ping_results_raw[1][0]) + "\n" + "Test 2 Latency: " + str(ping_results_raw[1][1]) + "\n" + "Test 3 Latency: " + str(ping_results_raw[1][2]) + "\n" + "Test 4 Latency: " + str(ping_results_raw[1][3]) + "\n" + str(ping_results_raw[2]) + "/4" + " Loss"
        pass
        self.ping_text.configure(state = tkinter.NORMAL)
        self.ping_text.insert("1.0", self.ping_results)
        self.ping_text.update_idletasks()
        self.ping_text.configure(state = tkinter.DISABLED)
    pass
    def ping_gui(self):
        """
        Ping tool GUI.
        :return: none.
        """
        root = tkinter.Toplevel()
        root.title("Raspbot RCA-G: Ping Tool")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(255, 290))
        root.resizable(width = False, height = False)
        self.ping_text = tkinter.Text(root, height = 8, width = 30, bg = "white", fg = "black", font = ("Calibri", 12))
        self.ping_text.grid(row = 0, column = 0, pady = (8, 14), padx = (5, 5))
        self.ping_text.configure(state = tkinter.DISABLED)
        self.ping_button = tkinter.Button(root, bg = "white", fg = "black", text = "Ping", width = 20, font = ("Calibri", 12), command = lambda: client.ping_wrapper(self))
        self.ping_button.grid(row = 1, column = 0, pady = (0, 2))
        save_button = tkinter.Button(root, bg = "white", fg = "black", text = "Save", width = 20, font = ("Calibri", 12), command = lambda: client.report_save(self, "PING", self.ping_results))
        save_button.grid(row = 2, column = 0, pady = (0, 2))
        close_button = tkinter.Button(root, bg = "white", fg = "black", text = "Close", width = 20, font = ("Calibri", 12), command = lambda: root.destroy())
        close_button.grid(row = 3, column = 0, pady = (0, 10))
        root.mainloop()
    pass
    def report_collect(self, report_type):
        """
        Sends a report request to host with given type and sets self.report_content with results.
        :param report_type: type of report.
        :return: none.
        """
        if report_type == "Science":
            if self.components[1][0] is True and self.components[1][1] is True and self.components[1][2] is True:
                comms.interface.send(b"rca-1.2:command_science_collect")
                data = comms.interface.receive().decode(encoding = "utf-8", errors = "replace")
                if data == "rca-1.2:hardware_unavailable":
                    print("[FAIL]: Host replies that RFP Enceladus hardware is unavailable. This conflicts with current configuration, please correct configurations.")
                    return None
                pass
                self.report_content = data
            else:
                return None
            pass
        elif report_type == "CH Check":
            comms.interface.send(b"rca-1.2:command_ch_check")
            if comms.acknowledge.receive_acknowledgement() is False:
                return None
            pass
            data = comms.interface.receive()
            data = data.decode(encoding="utf-8", errors="replace")
            self.report_content = data
        else:
            return None
        pass
    pass
    def report_gui(self, report_type, content):
        """
        Views a report with given type and contents.
        :param report_type: type of report.
        :param content: report contents to be displayed.
        :return: none.
        """
        if self.report_content == "":
            return None
        pass
        root = tkinter.Toplevel()
        root.title("Raspbot RCA-G: Report Viewer, " + report_type)
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(400, 370))
        root.resizable(width = False, height = False)
        graphics_report = tkinter.Text(root, height = 15, bg = "white", fg = "black", font = ("Calibri", 12))
        graphics_report.configure(state = tkinter.NORMAL)
        graphics_report.insert("1.0", content)
        graphics_report.update_idletasks()
        graphics_report.configure(state = tkinter.DISABLED)
        graphics_report.grid(row = 0, column = 0, pady = (5, 14))
        graphics_report_close_button = tkinter.Button(root, bg = "white", fg = "black", text = "Close", width = 40, font = ("Calibri", 12), command = lambda: root.destroy())
        graphics_report_close_button.grid(row = 1, column = 0, pady = (0, 10))
        root.mainloop()
    pass
    def report_save(self, report_type, content):
        """
        Saves a report with given type and contents.
        :param report_type: type of report.
        :param content: report contents to be saved.
        :return: none.
        """
        if self.report_content == "" and report_type != "PING":
            return None
        pass
        print("[INFO]: Generating timestamps for report...")
        timestamp = strftime("%b%d%Y%H%M%S"), gmtime()
        timestamp_output = timestamp[0]
        timestamp_str = str(timestamp_output)
        file_report_name = report_type + "_report-" + timestamp_str + ".txt"
        print("[INFO]: Generating text file report...")
        file_report = open(file_report_name, "w+")
        file_report.write(content)
        file_report.close()
        print("[INFO]: Report saved.")
    pass
    def dock(self):
        """
        Instructs host to dock with charger station.
        """
        comms.interface.send(b"rca-1.2:command_dock")
        if comms.acknowledge.receive_acknowledgement() is False:
            return None
        pass
        comms.objects.dock_status = True
    # TODO add logic for dock that triggers other changes
    pass
    def undock(self):
        """
        Instructs host to undock from charger station.
        :return: none.
        """
        comms.interface.send(b"rca-1.2:comamnd_undock")
        if comms.acknowledge.receive_acknowledgement() is False:
            return None
        pass
        comms.objects.dock_status = False
    # TODO add logic for dock that triggers other changes
    pass
    def os_control_shutdown_wrapper(self):
        """
        Creates dialogue asking for user to confirm to shutdown bot.
        :return: none.
        """
        confirm_dialogue = messagebox.askyesno("Raspbot RCA: Confirm Shutdown?", "Are you sure you want to shutdown the bot? There is no way to boot it besides physically restarting its power source, and if the Arduino fails, you may overdischarge your battery.")
        if confirm_dialogue is True:
            comms.interface.send(b"rca-1.2:command_shutdown")
            comms.disconnect.disconnect()
        else:
            return None
        pass
    pass
    @staticmethod
    def led_command(command, frame):
        """
        Issues commands to host for controlling LED matrix on SenseHAT by controlling transmissions.
        :param command: command to be executed by host.
        :param frame: index number for target frame set to be played, if command is not image or play, is ignored.
        :return: none.
        """
        comms.interface.send(b"rca-1.2:led_graphics")
        if comms.acknowledge.receive_acknowledgement() is False:
            return None
        pass
        if frame is None:
            command_frame = "0"
        else:
            command_frame = frame
        pass
        comms.interface.send(command.encode(encoding = "ascii", errors = "replace"))
        if comms.acknowledge.receive_acknowledgement() is False:
            return None
        pass
        if command == "image":
            comms.interface.send(command_frame.encode(encoding = "ascii", errors = "replace"))
        pass
    pass
    def led_gui(self):
        """
        If SenseHAT is included in hardware configuration, creates GUI for controlling LED matrix on SenseHAT.
        :return: none.
        """
        root = tkinter.Toplevel()
        root.title("Raspbot RCA-G: LED Controls")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(260, 131))
        root.resizable(width=False, height=False)
        graphics_title = tkinter.Label(root, text = "LED Controls", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 0, column = 0, padx = (0, 290))
        graphics_led_frame_buttons = tkinter.Frame(root, bg = "#344561")
        graphics_led_button_off = tkinter.Button(graphics_led_frame_buttons, text = "Off", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: client.led_command("stop", None))
        graphics_led_button_off.pack(side = tkinter.TOP)
        graphics_led_button_hello_world = tkinter.Button(graphics_led_frame_buttons, text = "Hello World", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: client.led_command("image", "1"))
        graphics_led_button_hello_world.pack(side = tkinter.BOTTOM)
        graphics_led_button_idle = tkinter.Button(graphics_led_frame_buttons, text = "Idle", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: client.led_command("image", "2"))
        graphics_led_button_idle.pack(side=tkinter.BOTTOM)
        graphics_led_frame_buttons.grid(row = 2, column = 0, padx = (0, 250))
        root.mainloop()
    pass

    def arm_control_gui(self):
        """
        Creates GUI for user to control arm.
        This will only be available if enabled, hardware check is performed at creation of main window.
        :return: none.
        """

        pass
    pass
pass

c = client()
