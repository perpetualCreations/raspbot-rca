"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# Made by Taian Chen
"""
# TODO modify docstrings

try:
    print("[INFO]: Starting imports...")
    import os
    from subprocess import call
    from time import sleep
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
    # import hashlib
except ImportError as e:
    os = None
    tkinter = None
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
        self.port = 67777
        self.connect_retries = 0
        self.components = [[None], [None, None, None], [None]] # [Base Set [cam], RFP Enceladus [sensehat, distance, dust], Upgrade #1 [charger]]
        self.auth = ""
        print("[INFO]: Loading configurations...")
        config_parse_load = configparser.ConfigParser()
        try:
            config_parse_load.read("main.cfg")
            self.components[0][0] = config_parse_load["hardware"]["cam"]
            self.components[1][0] = config_parse_load["hardware"]["sensehat"]
            self.components[1][1] = config_parse_load["hardware"]["distance"]
            self.components[1][2] = config_parse_load["hardware"]["dust"]
            self.components[2][0] = config_parse_load["hardware"]["charger"]
            self.host = config_parse_load["NET"]["IP"]
            self.port = config_parse_load["NET"]["PORT"]
            self.key = config_parse_load["ENCRYPT"]["KEY"]
            self.key = MD5.new(self.key).hexdigest()
            self.key = self.key.encode(encoding="ascii", errors="replace")
            self.hmac_key = config_parse_load["ENCRYPT"]["HMAC_KEY"]
            self.auth = config_parse_load["ENCRYPT"]["AUTH"]
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
        self.root.geometry('{}x{}'.format(400, 370))
        self.root.resizable(width=False, height=False)
        menu = tkinter.Menu(self.root)
        self.root.config(menu = menu)
        app_menu = tkinter.Menu(menu)
        hardware_menu = tkinter.Menu(app_menu)
        base_set_menu = tkinter.Menu(hardware_menu)
        base_set_menu.add_command(label = "Enable", command = lambda: client.set_configuration(self.components[0][0], True, "hardware", "cam", False))
        base_set_menu.add_command(label = "Disable", command = lambda: client.set_configuration(self.components[1][0], False, "hardware", "cam", False))
        rfp_enceladus_menu = tkinter.Menu(hardware_menu)
        rfp_enceladus_menu.add_command(label = "Enable", command = lambda: client.set_configuration([self.components[1][0], self.components[1][1], self.components[1][2]], [True, True, True], ["hardware", "hardware", "hardware"], ["sensehat", "distance", "dust"], True))
        rfp_enceladus_menu.add_command(label = "Disable", command = lambda: client.set_configuration([self.components[1][0], self.components[1][1], self.components[1][2]], [False, False, False], ["hardware", "hardware", "hardware"], ["sensehat", "distance", "dust"], True))
        upgrade_1_menu = tkinter.Menu(hardware_menu)
        upgrade_1_menu.add_command(label = "Enable", command = lambda: client.set_configuration(self.components[2][0], True, "hardware", "charger", False))
        upgrade_1_menu.add_command(label = "Disable", command = lambda: client.set_configuration(self.components[2][0], False, "hardware", "charger", False))
        hardware_menu.add_cascade(label = "Base Set", menu = base_set_menu)
        hardware_menu.add_cascade(label = "RFP Enceladus", menu = rfp_enceladus_menu)
        hardware_menu.add_cascade(label = "Upgrade #1", menu = upgrade_1_menu)
        app_menu.add_command(label = "Edit Configs")
        app_menu.add_cascade(label = "Edit Hardware Set", menu = hardware_menu)
        app_menu.add_command(label = "Exit", command = lambda: client.exit(0))
        menu.add_cascade(label = "App", menu = app_menu)
        self.root.mainloop()
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
    def exit(status):
        """Stops application."""
        print("[INFO]: Stopping application...")
        app_end(status)
    pass
    def connect(self):
        """Connects to an IP with port number, and starts an encrypted connection."""
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
        """Wrapper for host.encrypt, formats output to be readable for sending.."""
        encrypted = client.encrypt(self, message)
        return encrypted[1] + b" " + encrypted[2] + b" " + encrypted[0]
    pass
    def receive(self, socket_input):
        """
        Wrapper for host.decrypt, formats received input and returns decrypted message.
        Use as host.receive(self, socket.receive(integer)).
        """
        socket_input_spliced = socket_input.split()
        nonce = socket_input_spliced[0]
        hmac = socket_input_spliced[1]
        encrypted_message = socket_input_spliced[2]
        return client.decrypt(self, encrypted_message, hmac, nonce)
    pass
    def encrypt(self, byte_input):
        """Takes byte input and returns encrypted input using a key and encryption nonce."""
        ciphering = Salsa20.new(self.key)
        validation = HMAC.new(self.hmac_key, msg = ciphering.encrypt(byte_input), digestmod = SHA256)
        return [ciphering.encrypt(byte_input), ciphering.nonce, validation.hexdigest()]
    pass
    def decrypt(self, encrypted_input, validate, nonce):
        """Decrypts given encrypted message and validates message with HMAC and nonce from encryption."""
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

# c = client()
config_parse = configparser.ConfigParser()
config_parse.read("main.cfg")
config_parse.set("hardware", "cam", "True")
with open("main.cfg", "w") as w:
    config_parse.write(w)
pass