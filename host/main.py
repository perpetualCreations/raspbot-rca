"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Made by perpetualCreations
"""

try:
    print("[INFO]: Starting imports...")
    from time import sleep
    from Cryptodome.Cipher import Salsa20
    from Cryptodome.Hash import HMAC, SHA256, MD5, SHA3_512, cv2
    import socket, configparser, multiprocessing, serial
    from sys import exit as app_end
    from ast import literal_eval
    # RCA Modules
    import hardware_check, led_graphics, basics, science
except ImportError as ImportErrorMessage:
    print("[FAIL]: Imports failed! See below.")
    print(ImportErrorMessage)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(ImportWarningMessage)
pass

# logging, bottom line is to stop PyCharm from throwing a warning when ImportError is raised and basics becomes a None boolean object.
# noinspection PyUnboundLocalVariable
basics.basics.log_init()

class host:
    """Main class."""
    def __init__(self):
        """Initiation function of RCA. Reads configs and starts boot processes."""
        print("[INFO]: Starting host Raspbot RC Application...")
        print("[INFO]: Declaring variables...")
        self.socket = None
        self.host = ""
        self.port = 64220
        self.connect_retries = 0
        self.components = [[None], [None, None, None], [None], [None, None]]  # [Base Set [cam], RFP Enceladus [sensehat, distance, dust], Upgrade #1 [charger], Robotic Arm Kit [arm, arm_cam]]
        self.dock_status = False
        print("[INFO]: Loading configurations...")
        config_parse_load = configparser.ConfigParser()
        try:
            config_parse_load.read("main.cfg")
            self.host = config_parse_load["NET"]["ip"]
            self.port = config_parse_load["NET"]["port"]
            self.cam_port = config_parse_load["NET"]["cam_port"]
            self.cam_port = int(self.cam_port)
            self.port = int(self.port)
            raw_key = config_parse_load["ENCRYPT"]["key"]
            raw_key_hash = MD5.new(raw_key.encode(encoding = "ascii", errors = "replace"))
            self.key = raw_key_hash.hexdigest()
            self.key = self.key.encode(encoding = "ascii", errors = "replace")
            self.hmac_key = config_parse_load["ENCRYPT"]["hmac_key"]
            self.auth = config_parse_load["ENCRYPT"]["auth"]
            self.auth = self.auth.encode(encoding = "ascii", errors = "replace")
        except configparser.Error as ce:
            print("[FAIL]: Failed to load configurations! See below for details.")
            print(ce)
            basics.basics.exit(1)
        except KeyError as ke:
            print("[FAIL]: Failed to load configurations! Configuration file is corrupted or has been edited incorrectly.")
            print(ke)
            basics.basics.exit(1)
        except FileNotFoundError:
            print("[FAIL]: Failed to load configurations! Configuration file is missing.")
            basics.basics.exit(1)
        pass
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
            basics.basics.exit(1)
        except KeyError as ke:
            print("[FAIL]: Failed to load configurations! Configuration file is corrupted or has been edited incorrectly.")
            print(ke)
            basics.basics.exit(1)
        except FileNotFoundError:
            print("[FAIL]: Failed to load configurations! Configuration file is missing.")
            basics.basics.exit(1)
        pass
        if self.components[1][0] is True:
            self.pattern_led = [["error1.png", "error2.png"], ["helloworld.png"], ["idle1.png", "idle2.png"], ["power-on.png"], ["power-off.png"], ["start1.png", "start2.png", "start3.png", "start4.png"]]
        pass
        print("[INFO]: Creating open server socket...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.socket.settimeout(5)
        self.socket.bind((socket.gethostname(), self.port))
        self.socket.setblocking(True)
        self.socket.listen(1)
        connection, client_address = self.socket.accept()
        self.socket.setblocking(False)
        with connection:
            print("[INFO]: Received connection from ", client_address, ".")
            connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
            data = SHA3_512.new(host.receive(self, connection.recv(4096))).hexdigest().encode(encoding = "ascii", errors = "replace")
            if data == self.auth:
                print("[INFO]: Client authenticated!")
                connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
            else:
                print("[FAIL]: Client authentication invalid! Given code does not match authentication code.")
                connection.sendall(host.send(self, b"rca-1.2:authentication_invalid"))
                self.socket.close()
                basics.restart_shutdown.restart()
            pass
            while True:
                command = host.receive(self, connection.recv(4096))
                if command == b"rca-1.2:command_shutdown":
                    connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                    basics.restart_shutdown.shutdown()
                elif command == b"rca-1.2:command_reboot":
                    connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                    basics.restart_shutdown.reboot()
                elif command == b"rca-1.2:command_update":
                    connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                    basics.basics.os_update()
                elif command == b"rca-1.2:command_battery_check":
                    connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                elif command == b"rca-1.2:command_science_collect":
                    connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                    if self.components[1][0] is True and self.components[1][1] is True and self.components[1][2]:
                        connection.sendall(host.send(self, science.science.get()))
                    else:
                        connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                    pass
                elif command == b"rca-1.2:nav_start":
                    connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                    nav_command = host.receive(self, connection.recv(4096)).decode(encoding = "utf-8", errors = "replace")
                    nav_command_list = nav_command.split()
                    nav_direction = nav_command_list[0]
                    nav_run_time = nav_command_list[1]
                    nav_distance_accept = nav_command_list[2]
                    host.serial("/dev/ttyACM0", "send", nav_direction.encode(encoding = "ascii", errors = "replace"))
                    basics.process.create_process(host.nav_timer, (self, int(nav_run_time), literal_eval(nav_distance_accept)))
                elif command == b"rca-1.2:disconnected":
                    self.socket.close()
                    print("[INFO]: Client has disconnected.")
                    basics.restart_shutdown.restart()
                elif command == b"rca-1.2:led_graphics":
                    connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                    if self.components[1][0] is True and self.components[1][1] is True and self.components[1][2] is True:
                        led_command = host.receive(self, connection.recv(4096)).decode(encoding = "utf-8", errors = "replace")
                        if led_command == b"play":
                            raise NotImplementedError
                        elif led_command == b"image":
                            connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                            led_graphics.led_graphics.display("image", self.pattern_led[int(host.receive(self, connection.recv(4096)).decode(encoding = "utf-8", errors = "replace"))])
                        elif led_command == b"stop":
                            connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                            led_graphics.led_graphics.display("stop", None)
                        pass
                    else:
                        connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                    pass
                elif command == b"rca-1.2:command_ch_check":
                    connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                    hardware_check.computer_hardware_check.collect()
                    hardware_check.computer_hardware_check.convert()
                    connection.sendall(host.send(self, hardware_check.computer_hardware_check.report()))
                elif command == b"rca-1.2:get_dock_status":
                    if self.components[2][0] is True:
                        connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                        dock_status_str = str(self.dock_status)
                        connection.sendall(host.send(self, dock_status_str.encode(encoding = "ascii", errors = "replace")))
                    else:
                        connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                    pass
                elif command == b"rca-1.2:command_dock":
                    if self.components[2][0] is True:
                        pass
                        # TODO write dock logic
                    else:
                        connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                    pass
                elif command == b"rca-1.2:command_undock":
                    if self.components[2][0] is True:
                        pass
                        # TODO write undock logic
                    else:
                        connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                    pass
                else:
                    connection.sendall(host.send(self, b"rca-1.2:unknown_command"))
                pass # add more keys here
            pass
        pass
    pass
    @staticmethod
    def serial(port, direction, message):
        """
        Sends or receives serial communications to the Arduino integration.
        :param port: the port that the Arduino is connected to.
        :param direction: whether to expect to receive or send.
        :param message: what contents to send, or if receiving leave as None.
        :return: if receiving, decoded string, if sending or invalid direction, none.
        """
        arduino_connect = serial.Serial(port = port, timeout = 5)
        if direction == "receive":
            return arduino_connect.readline().decode(encoding = "utf-8", errors = "replace")
        elif direction == "send":
            if message not in [""]: # TODO list all possible commands
                return None
            pass
            arduino_connect.write(message.encode(encoding = "ascii", errors = "replace"))
            return None
        else:
            return None
        pass
    pass
    def send(self, message):
        """
        Wrapper for host.encrypt, formats output to be readable for sending.
        Use as socket.sendall(host.send(self, b"message")).
        :param message: message to be encrypted.
        :return: formatted byte string with encrypted message, HMAC validation, and nonce.
        """
        encrypted = host.encrypt(self, message)
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
        return host.decrypt(self, encrypted_message, hmac, nonce)
    pass
    def encrypt(self, byte_input):
        """
        Takes byte input and returns encrypted input using a key and encryption nonce.
        :param byte_input: byte string to be encrypted.
        :return: encrypted string, nonce, and HMAC validation.
        """
        if isinstance(byte_input, bytes):
            pass
        else:
            byte_input.encode(encoding = "ascii", errors = "replace")
        pass
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
            basics.restart_shutdown.restart()
            raise Exception("[FAIL]: Message is not authentic, failed HMAC validation!")
        pass
        ciphering = Salsa20.new(self.key, nonce = nonce)
        return ciphering.decrypt(encrypted_input)
    pass
    def receive_acknowledgement(self):
        """
        Listens for an acknowledgement byte string, returns booleans whether string was received or failed.
        :return: if received, returns True, otherwise returns False indicating a failure in receiving acknowledgement.
        """
        try:
            acknowledgement = host.receive(self, self.socket.recv(4096))
        except socket.error as sae:
            print("[FAIL]: Failed to receive acknowledgement string. See below for details.")
            print(sae)
            return False
        pass
        if acknowledgement == b"rca-1.2:connection_acknowledge":
            print("[INFO]: Received acknowledgement.")
            return True
        else:
            print("[FAIL]: Did not receive an acknowledgement. Instead received: ")
            print(acknowledgement.decode(encoding = "uft-8", errors = "replace"))
            return False
        pass
    pass
    def nav_timer(self, nav_run_time, nav_distance_accept):
        """
        Navigation timer for multiprocessing, counts down until run time is over, also reads distance telemetry and forwards to client.
        :param nav_run_time:
        :param nav_distance_accept:
        :return: none.
        """
        nav_run_time_countdown = nav_run_time
        while nav_run_time_countdown != 0:
            nav_run_time_countdown -= 1
            if nav_distance_accept is True:
                host.serial("/dev/ttyACM0", "send", b"T")
                self.socket.sendall(host.send(self, host.serial("/dev/ttyACM0", "recieve", None)))
            pass
            if nav_run_time_countdown == 0:
                self.socket.sendall(host.send(self, b"rca-1.2:nav_end"))
                host.serial("/dev/ttyACM0", "send", b"A")
            pass
            sleep(1)
        pass
    pass
pass

h = host()
