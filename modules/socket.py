"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
socket.py module, contains socket communication functions.
Class name is comms to prevent confusion.
Made by Taian Chen
"""

try:
    import socket
    from Cryptodome.Cipher import Salsa20
    from Cryptodome.Hash import HMAC
    from Cryptodome.Hash import SHA256
    from tkinter import messagebox
except ImportError as ImportErrorMessage:
    socket = None
    Salsa20 = None
    HMAC = None
    SHA256 = None
    messagebox = None
    print("[COMMS][FAIL]: Import failed!")
    print(ImportErrorMessage)
except ImportWarning as ImportWarningMessage:
    print("[COMMS][FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
pass

class comms:
    """Class containing functions for socket communications."""
    def __init__(self, socket_object, socket_object_camera, config):
        """
        Initiation function.
        :param socket_object: first socket object for main communications.
        :param socket_object_camera: second socket object for Raspbot's camera stream.
        :param config: list structured as [self.host, self.port, self.cam_port, self.auth], defined in main.py.
        """
        print("[COMMS][INFO]: Socket (comms) module loaded!")
        self.config = config

    pass
    def connect(self):
        """
        Connects to an IP with port number, and starts an encrypted connection.
        :return: none.
        """
        print("[INFO]: Creating socket connection...")
        socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_object.setblocking(False)
        socket_object.settimeout(10)
        try:
            socket_object.connect((self.config[0], config[1]))
        except socket.error as se:
            print("[FAIL]: Failed to connect! See below for details.")
            print(se)
            messagebox.showerror("Raspbot RCA: Connection Failed",
                                 "While connecting to the bot for main communications an error was raised. Please see console output for more details.")
        pass
        if comms.receive_acknowledgement(self) is False:
            return None
        pass
        socket_object.sendall(comms.send(self, self.auth))
        if client.receive_acknowledgement(self) is False:
            print("[INFO]: Closing connection due to invalid authentication...")
            client.disconnect(self)
            return None
        pass
        print("[INFO]: Successfully connected to host!")
        print("[INFO]: Creating socket connection (for camera view)...")
        socket_object_camera = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_object_camera.setblocking(False)
        socket_object_camera.settimeout(10)
        try:
            socket_object_camera.connect((self.config[0], self.cam_port))
        except socket.error as sce:
            print("[FAIL]: Failed to connect! See below for details.")
            print(sce)
            messagebox.showerror("Raspbot RCA: Connection Failed",
                                 "While connecting to the bot for camera view, an error was raised. Please see console output for more details.")
        pass
        if comms.receive_acknowledgement(self) is False:
            return None
        pass
        socket_object.sendall(client.send(self, self.auth))
        if client.receive_acknowledgement(self) is False:
            print("[INFO]: Closing connection due to invalid authentication...")
            client.disconnect(self)
        pass
        print("[INFO]: Successfully connected to host (for camera view)!")
        if self.components[2][0]:
            socket_object.sendall(client.send(self, b"rca-1.2:get_dock_status"))
            self.dock_status = literal_eval(
                client.receive(self, socket_object.recv(1024).decode(encoding="utf-8", errors="replace")))
            print("[INFO]: Updated dock status from host.")
        pass
        messagebox.showinfo("Raspbot RCA: Connection Successful",
                            "You are now connected to the bot." + "\n Bot IP (in case you want to use SSH): " + config[0])
    pass
    def disconnect(self):
        """
        Sends a message to host notifying that client has disconnected and then closes socket.
        :return: none.
        """
        self.socket.sendall(client.send(self, b"rca-1.2:disconnected"))
        self.net_status_data.set("Status: " + "Disconnected")
        self.socket.close()
        print("[INFO]: Disconnected from bot.")
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
        return comms.decrypt(self, socket_input_spliced[2], socket_input_spliced[1], socket_input_spliced[0])
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
            byte_input.encode(encoding="ascii", errors="replace")
        pass
        ciphering = Salsa20.new(self.key)
        validation = HMAC.new(self.hmac_key, msg=ciphering.encrypt(byte_input), digestmod=SHA256)
        return [ciphering.encrypt(byte_input), ciphering.nonce, validation.hexdigest()]
    pass
    def decrypt(self, encrypted_input, validate, nonce):
        """
        Decrypts given encrypted message and validates message with HMAC and nonce from encryption.
        :param encrypted_input: encrypted string to be decrypted.
        :param validate: HMAC validation byte string.
        :param nonce: nonce, additional security feature to prevent replay attacks.
        """
        validation = HMAC.new(self.hmac_key, msg = encrypted_input, digestmod=SHA256)
        try:
            validation.hexverify(validate)
        except ValueError:
            client.disconnect(self)
            raise Exception("[FAIL]: Message is not authentic, failed HMAC validation!")
        pass
        ciphering = Salsa20.new(self.key, nonce=nonce)
        return ciphering.decrypt(encrypted_input)
    pass
    def receive_acknowledgement(self):
        """Listens for an acknowledgement byte string, returns booleans whether string was received or failed."""
        try:
            acknowledgement = comms.receive(self, self.socket.recv(4096))
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
        elif acknowledgement == b"rca-1.2:unknown_command":
            print("[FAIL]: Command unrecognized by host.")
            return False
        else:
            messagebox.showwarning("Raspbot RCA: Bad Acknowledgement",
                                   "The host has replied with an invalid acknowledgement." + "\n Received: " + acknowledgement.decode(
                                       encoding="utf-8", errors="replace"))
            print("[FAIL]: Did not receive an acknowledgement. Instead received: ")
            print(acknowledgement.decode(encoding="uft-8", errors="replace"))
            return False
        pass
    pass
pass
