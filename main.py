"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# Made by Taian Chen
"""
# TODO modify docstrings

try:
    print("[INFO]: Starting imports...")
    from subprocess import call
    from time import sleep
    from time import strftime
    from time import gmtime
    # AES + RSA-based encryption was not finished, and sections using it were commented out.
    # from Cryptodome.PublicKey import RSA
    # from Cryptodome import Random
    # from Cryptodome.Cipher import AES
    from Cryptodome.Cipher import Salsa20
    from Cryptodome.Hash import HMAC
    from Cryptodome.Hash import SHA256
    from Cryptodome.Hash import MD5
    import socket
    import configparser
    from sys import exit as app_end
    import multiprocessing
    import tkinter
    from tkinter import messagebox
    from ast import literal_eval
    from ping3 import ping
    # import hashlib
except ImportError as e:
    sleep = None
    strftime = None
    gmtime = None
    tkinter = None
    messagebox = None
    call = None
    Popen = None
    Salsa20 = None
    HMAC = None
    SHA256 = None
    socket = None
    configparser = None
    MD5 = None
    app_end = None
    multiprocessing = None
    literal_eval = None
    ping = None
    # RSA = None
    # AES = None
    # Random = None
    # hashlib = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class client:
    """Main class."""
    def __init__(self):
        """Initiation function of Raspbot RCA."""
        print("[INFO]: Starting client Raspbot RC Application...")
        print("[INFO]: Declaring variables...")
        # AES + RSA-based encryption was not finished, and sections using it were commented out.
        # self.key = None
        # self.private = None
        # self.public = None
        self.socket = None
        self.host = ""
        self.port = 64220
        self.connect_retries = 0
        self.components = [[None], [None, None, None], [None]] # [Base Set [cam], RFP Enceladus [sensehat, distance, dust], Upgrade #1 [charger]]
        self.auth = ""
        self.ping_text = None
        self.ping_button = None
        self.report_content = ""
        print("[INFO]: Loading configurations...")
        config_parse_load = configparser.ConfigParser()
        try:
            config_parse_load.read("main.cfg")
            self.components[0][0] = literal_eval(config_parse_load["HARDWARE"]["cam"])
            self.components[1][0] = literal_eval(config_parse_load["HARDWARE"]["sensehat"])
            self.components[1][1] = literal_eval(config_parse_load["HARDWARE"]["distance"])
            self.components[1][2] = literal_eval(config_parse_load["HARDWARE"]["dust"])
            self.components[2][0] = literal_eval(config_parse_load["HARDWARE"]["charger"])
            self.host = config_parse_load["NET"]["ip"]
            self.port = config_parse_load["NET"]["port"]
            self.port = int(self.port)
            self.key = config_parse_load["ENCRYPT"]["key"]
            self.key = self.key.encode(encoding="ascii", errors="replace")
            self.key = MD5.new(self.key).hexdigest()
            self.hmac_key = config_parse_load["ENCRYPT"]["hmac_key"]
            self.auth = config_parse_load["ENCRYPT"]["auth"]
            self.auth = self.auth.encode(encoding = "ascii", errors = "replace")
        except configparser.Error as ce:
            print("[FAIL]: Failed to load configurations! See below for details.")
            print(ce)
        except FileNotFoundError:
            print("[FAIL]: Failed to load configurations! Configuration file is missing.")
        pass
        print("[INFO]: Starting GUI...")
        self.root = tkinter.Tk()
        self.root.title("Raspbot RCA: Client")
        self.root.configure(bg = "#344561")
        self.root.geometry('{}x{}'.format(1200, 600))
        self.root.resizable(width=False, height=False)
        menu = tkinter.Menu(self.root)
        self.root.config(menu = menu)
        app_menu = tkinter.Menu(menu)
        hardware_menu = tkinter.Menu(app_menu)
        base_set_menu = tkinter.Menu(hardware_menu)
        base_set_menu.add_command(label = "Enable", command = lambda: client.set_configuration(self.components[0][0], True, "HARDWARE", "cam", False))
        base_set_menu.add_command(label = "Disable", command = lambda: client.set_configuration(self.components[1][0], False, "HARDWARE", "cam", False))
        rfp_enceladus_menu = tkinter.Menu(hardware_menu)
        rfp_enceladus_menu.add_command(label = "Enable", command = lambda: client.set_configuration([self.components[1][0], self.components[1][1], self.components[1][2]], [True, True, True], ["HARDWARE", "HARDWARE", "HARDWARE"], ["sensehat", "distance", "dust"], True))
        rfp_enceladus_menu.add_command(label = "Disable", command = lambda: client.set_configuration([self.components[1][0], self.components[1][1], self.components[1][2]], [False, False, False], ["HARDWARE", "HARDWARE", "HARDWARE"], ["sensehat", "distance", "dust"], True))
        upgrade_1_menu = tkinter.Menu(hardware_menu)
        upgrade_1_menu.add_command(label = "Enable", command = lambda: client.set_configuration(self.components[2][0], True, "HARDWARE", "charger", False))
        upgrade_1_menu.add_command(label = "Disable", command = lambda: client.set_configuration(self.components[2][0], False, "HARDWARE", "charger", False))
        hardware_menu.add_cascade(label = "Base Set", menu = base_set_menu)
        hardware_menu.add_cascade(label = "RFP Enceladus", menu = rfp_enceladus_menu)
        hardware_menu.add_cascade(label = "Upgrade #1", menu = upgrade_1_menu)
        app_menu.add_command(label = "Edit Configs", command = lambda: client.set_configuration_gui())
        app_menu.add_cascade(label = "Edit Hardware Set", menu = hardware_menu)
        app_menu.add_command(label = "Exit", command = lambda: client.exit(0))
        menu.add_cascade(label = "App", menu = app_menu)
        net_menu = tkinter.Menu(menu)
        net_tools_menu = tkinter.Menu(net_menu)
        net_tools_menu.add_command(label = "Ping", command = lambda: client.ping_gui(self))
        net_menu.add_cascade(label = "Tools", menu = net_tools_menu)
        menu.add_cascade(label = "Net", menu = net_menu)
        vitals_frame = tkinter.Frame(self.root, bg = "#506a96", highlightthickness = 2, bd = 0)
        vitals_frame.grid(row = 0, column = 0, padx = (10, 0), pady = (15, 0))
        vitals_label = tkinter.Label(vitals_frame, bg = "#506a96", fg = "white", text = "Bot Vitals", font = ("Calibri", 12))
        vitals_label.grid(row = 0, column = 0, padx = (5, 0))
        self.vitals_text = tkinter.Text(vitals_frame, bg = "white", fg = "black", state = tkinter.DISABLED, height = 10, width = 40, font = ("Calibri", 10))
        self.vitals_text.grid(row = 1, column = 0, padx = (5, 5), pady = (10, 0))
        vitals_refresh_button = tkinter.Button(vitals_frame, text = "Refresh", bg = "white", fg = "black", command = lambda: client.vitals_refresh(self, False))
        vitals_refresh_button.grid(row = 2, column = 0, padx = (5, 5), pady = (10, 5))
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
        net_disconnect_button = tkinter.Button(net_frame, bg = "white", fg = "black", text = "Disconnect", font = ("Calibri", 12), width = 10, height = 1, command = lambda: self.socket.close())
        net_disconnect_button.grid(row = 2, column = 0, padx = (5, 0), pady = (10, 0))
        net_connect_button = tkinter.Button(net_frame, bg = "white", fg = "black", text = "Connect", font = ("Calibri", 12), width = 10, height = 1, command = lambda: client.connect(self))
        net_connect_button.grid(row = 3, column = 0, padx = (5, 0))
        net_help_button = tkinter.Button(net_frame, bg = "#506a96", fg = "white", text = "?", width = 1, height = 1, font = ("Calibri", 10), command = lambda: messagebox.showinfo("Raspbot RCA: Net Help", "This panel controls your network connection with the bot. See the NET options in menu bar for additional tools and actions."))
        net_help_button.grid(row = 4, column = 0, padx = (5, 150), pady = (20, 5))
        report_frame = tkinter.Frame(multi_frame, bg = "#506a96", highlightthickness = 2, bd = 0)
        report_frame.grid(row = 0, column = 1, padx = (5, 0))
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
        report_collect_button = tkinter.Button(report_frame, bg = "white", fg = "black", text = "Collect", font = ("Calibri", 12), width = 10, command = lambda: client.report_collect(self))
        report_collect_button.grid(row = 2, column = 0, padx = (5, 0), pady = (5, 0))
        report_view_button = tkinter.Button(report_frame, bg = "white", fg = "black", text = "View", font = ("Calibri", 12), width = 10, command = lambda: client.report_gui(self, report_type_data.get(), self.report_content))
        report_view_button.grid(row = 3, column = 0, padx = (5, 0), pady = (5, 0))
        report_save_button = tkinter.Button(report_frame, bg = "white", fg = "black", text = "Save", font = ("Calibri", 12), width = 10, command = lambda: client.report_save(self, report_type_data.get(), self.report_content))
        report_save_button.grid(row = 4, column = 0, padx = (5, 0), pady = (5, 0))
        report_help_button = tkinter.Button(report_frame, bg = "#506a96", fg = "white", text = "?", width = 1, height = 1, font = ("Calibri", 12), command = lambda: messagebox.showinfo("Raspbot RCA: Report Help", "This panel allows you to request, view, and save reports of a vareity of types. These include computer hardware checks (CH Check) and science reports (Science, RFP Enceladus)."))
        report_help_button.grid(row = 5, column = 0, padx = (5, 150), pady = (20, 5))
        self.root.mainloop()
    pass
    @staticmethod
    def create_process(target, args):
        """
        Creates a new process from multiprocessing.
        :param target: the function being processed.
        :param args: the arguments for said function being processed.
        :return: if failed, returns nothing. otherwise returns dummy variable.
        """
        if __name__ == '__main__':
            try:
                dummy = multiprocessing.Process(target = target, args = args)
                dummy.start()
                dummy.join()
            except multiprocessing.ProcessError as me:
                print("[FAIL]: Process creation failed! Details below.")
                print(me)
                return None
            pass
            return dummy
        else:
            return None
        pass
    pass
    @staticmethod
    def stop_process(target, error_ignore):
        """
        Stops target process from multiprocessing.
        :param target: process to be stopped.
        :param error_ignore: boolean to tell the function to throw a failure message or not when failed.
        :return: none.
        """
        if __name__ == '__main__':
            try:
                target.terminate()
            except Exception as spe:
                if error_ignore is True:
                    print("[INFO]: Stop process failed, however this is indicated to be normal.")
                else:
                    print("[FAIL]: Stop process failed! See details below.")
                    print(spe)
                pass
            pass
        pass
    pass
    def vitals_refresh(self, loop):
        """
        Requests bot vitals.
        :param loop: boolean input deciding whether the function should loop. Enable only for multiprocessing.
        :return: none.
        """
        if loop is True:
            while True:
                self.socket.sendall(client.send(self, b"rca-1.2:vitals_request"))
                reply = client.receive(self, self.socket.recv(4096))
                vitals_text_data = reply.decode(encoding = "utf-8", errors = "replace")
                self.vitals_text.configure(state = tkinter.NORMAL)
                self.vitals_text.delete("1.0", tkinter.END)
                self.vitals_text.insert("1.0", vitals_text_data)
                self.vitals_text.update_idletasks()
                self.vitals_text.configure(state = tkinter.DISABLED)
            pass
        else:
            self.socket.sendall(client.send(self, b"rca-1.2:vitals_request"))
            reply = client.receive(self, self.socket.recv(4096))
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
    def set_configuration(var, value, section, key, multi):
        """
        Edits entry in configuration file and applies new edit to variables.
        :param var: variable being updated.
        :param value: value to be assigned to variable and entered into configuration file.
        :param section: section in the configuration file to be edited.
        :param key: key to variable in section in the configuration file to be edited.
        :param multi: boolean for whether to run a for range when reading params, useful when making multiple configuration settings.
        :return: None
        """
        print("[INFO]: Editing configurations...")
        str(var)
        str(value)
        str(section)
        str(key)
        if multi is True:
            cycles = len(var)
            while cycles != 0:
                parameter_key = cycles - 1
                var[parameter_key] = value[parameter_key]
                config_parse_edit = configparser.ConfigParser()
                config_parse_edit[section[parameter_key]][key[parameter_key]] = var[parameter_key]
                with open("main.cfg", "w") as config_write:
                    config_parse_edit.write(config_write)
                pass
                cycles -= 1
            pass
            config_write.close()
        else:
            var = value
            config_parse_edit = configparser.ConfigParser()
            print(section)
            print(key)
            config_parse_edit[section][key] = var
            with open("main.cfg", "w") as config_write:
                config_parse_edit.write(config_write)
            pass
            config_write.close()
        pass
    pass
    @staticmethod
    def set_configuration_gui():
        """
        Does exactly what client.set_configuration does, but with a GUI window.
        """
        raise NotImplementedError
        # TODO write configuration gui
    pass
    def ping(self):
        """
        Pings host address and records latency and losses.
        :return: average latency, nested list with individual latency values, total losses, nested list with individual losses, if host resolution failed
        """
        scans = [ping(self.host, timeout = 10, size = 64, unit = "ms"), ping(self.host, timeout = 10, size = 64, unit = "ms"), ping(self.host, timeout = 10, size = 64, unit = "ms"), ping(self.host, timeout = 10, size = 64, unit = "ms")]
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
            return result
        pass
    pass
    def ping_wrapper(self):
        """
        Wrapper for client.ping() for ping_gui.
        :return: none
        """
        raise NotImplementedError
        # TODO Complete
    pass
    def ping_gui(self):
        """
        Does exactly what client.set_configuration does, but with a GUI window.
        :return: none.
        """ # TODO complete
        raise NotImplementedError
        root = tkinter.Toplevel()
        root.title("Raspbot RCA: Ping")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(200, 150))
        root.resizable(width = False, height = False)
        self.ping_text = tkinter.Text(root, bg = "white", fg = "black", state = tkinter.DISABLED, height = 20, width = 15, font = ("Calibri", 10))
        ping_text.grid(row = 0, column = 0, padx = (5, 5), pady = (10, 0))
        self.ping_button = tkinter.Button(root, bg = "white", fg = "black", text = "Ping", font = ("Calibri", 12), command = ping_wrapper)
        ping_button.grid(row = 1, column = 0, padx = (5, 5), pady = (5, 5))
    pass
    def report_collect(self, report_type):
        """
        Sends a report request to host with given type and sets self.report_content with results.
        :param report_type: type of report.
        :return: none.
        """
        if report_type == "Science":
            if self.components[1][0] is True and self.components[1][1] is True and self.components[1][2] is True:
                self.socket.sendall(client.send(self, b"rca-1.2:command_science_collect"))
            else:
                return None # TODO finish
            pass
        elif report_type == "CH Check":
            self.socket.sendall(client.send(self, b"rca-1.2:command_ch_check"))
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
        graphics_report.configure(state = tkinter.DISABLED)
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
        if self.report_content == "":
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
    @staticmethod
    def exit(status):
        """
        Stops application.
        """
        print("[INFO]: Stopping application...")
        app_end(status)
    pass
    def connect(self):
        """
        Connects to an IP with port number, and starts an encrypted connection.
        """
        print("[INFO]: Creating socket connection...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.socket.settimeout(10)
        try:
            self.socket.connect((self.host, self.port))
        except socket.error as se:
            print("[FAIL]: Failed to connect! See below for details.")
            print(se)
        pass
        confirm = client.receive_acknowledgement(self)
        if confirm is False:
            return None
        pass
        self.socket.sendall(client.send(self, self.auth))
        confirm = client.receive_acknowledgement(self)
        if confirm is False:
            print("[INFO]: Closing connection due to invalid authentication...")
            self.socket.close()
            return None
        pass
        print("[INFO]: Successfully connected to host!")
        # AES + RSA-based encryption was not finished, and sections using it were commented out.
        # print("[INFO]: Generating encryption keys...")
        # random = Random.new().read
        # self.key = RSA.generate(1024, random)
        # self.private = self.key.exportKey()
        # self.public = self.key.publickey().exportKey()
        # hash_public_object = hashlib.sha1(self.public)
        # hash_public = hash_public_object.hexdigest()
        # print("[INFO]: Forwarding keys to host...")
        # self.socket.sendall(self.public)
        # confirm = client.receive_acknowledgement(self)
        # if confirm is False:
        #     return None
        # pass
        # self.socket.sendall(hash_public)
        # confirm = client.receive_acknowledgement(self)
        # if confirm is False:
        #     return None
        # pass
        # msg = self.socket.recv(1024)
        # self.socket.sendall(b"rca-1.2:connection_acknowledge")
        # en = eval(msg)
        # decrypt = self.key.decrypt(en)
        # hashing sha1
        # en_object = hashlib.sha1(decrypt)
        # en_digest = en_object.hexdigest()
    pass
    def send(self, message):
        """
        Wrapper for host.encrypt, formats output to be readable for sending.
        Use as socket.sendall(host.send(self, b"message")).
        :param message: message to be encrypted.
        :return: formatted byte string with encrypted message, HMAC validation, and nonce.
        """
        encrypted = client.encrypt(self, message)
        return encrypted[1] + b" " + encrypted[2] + b" " + encrypted[0]
    pass
    def receive(self, socket_input):
        """
        Wrapper for host.decrypt, formats received input and returns decrypted message.
        Use as host.receive(self, socket.receive(integer)).
        :param socket_input: byte string being decrypted.
        :return: decrypted message.
        """
        socket_input_spliced = socket_input.split()
        nonce = socket_input_spliced[0]
        hmac = socket_input_spliced[1]
        encrypted_message = socket_input_spliced[2]
        return client.decrypt(self, encrypted_message, hmac, nonce)
    pass
    def encrypt(self, byte_input):
        """
        Takes byte input and returns encrypted input using a key and encryption nonce.
        :param byte_input: byte string to be encrypted.
        :return: encrypted string, nonce, and HMAC validation.
        """
        ciphering = Salsa20.new(self.key)
        validation = HMAC.new(self.hmac_key, msg = ciphering.encrypt(byte_input), digestmod = SHA256)
        return [ciphering.encrypt(byte_input), ciphering.nonce, validation.hexdigest()]
    pass
    def decrypt(self, encrypted_input, validate, nonce):
        """
        Decrypts given encrypted message and validates message with HMAC and nonce from encryption.
        :param encrypted_input: encrypted string to be decrypted.
        :param validate: HMAC validation byte string.
        :param nonce: nonce, additional security feature to prevent replay attacks.
        """
        validation = HMAC.new(self.hmac_key, msg = encrypted_input, digestmod = SHA256)
        try:
            validation.hexverify(validate)
        except ValueError:
            self.socket.close()
            raise Exception("[FAIL]: Message is not authentic, failed HMAC validation!")
        pass
        ciphering = Salsa20.new(self.key, nonce = nonce)
        return ciphering.decrypt(encrypted_input)
    pass
    def receive_acknowledgement(self):
        """Listens for an acknowledgement byte string, returns booleans whether string was received or failed."""
        try:
            acknowledgement = client.receive(self, self.socket.recv(4096))
        except socket.error as sae:
            print("[FAIL]: Failed to receive acknowledgement string. See below for details.")
            print(sae)
            return False
        pass
        if acknowledgement == b"rca-1.2:connection_acknowledge":
            print("[INFO]: Received acknowledgement.")
            return True
        elif acknowledgement == b"rca-1.2:authentication_invalid":
            print("[FAIL]: Did not receive an acknowledgement. Authentication was invalid.")
            return False
        else:
            print("[FAIL]: Did not receive an acknowledgement. Instead received: ")
            print(acknowledgement.decode(encoding = "uft-8", errors = "replace"))
        pass
    pass
pass

c = client()
