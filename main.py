"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# Made by Taian Chen
"""

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
    from Cryptodome import Exception as EncryptionError
    import socket
    import configparser
    from sys import exit as app_end
    import multiprocessing
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
    EncryptionError = Exception
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

class Raspbot:
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
        self.components = [[None], [None, None, None], [None]] # [Base Set [CAM], RFP Enceladus [SenseHAT, DISTANCE, DUST], Upgrade #1 [CHARGER]]
        print("[INFO]: Loading configurations...")
        config_parse = configparser.ConfigParser()
        try:
            config_parse.read("main.cfg")
            self.components[0][0] = config_parse["HARDWARE"]["CAM"]
            self.components[1][0] = config_parse["HARDWARE"]["SenseHAT"]
            self.components[1][1] = config_parse["HARDWARE"]["DISTANCE"]
            self.components[1][2] = config_parse["HARDWARE"]["DUST"]
            self.components[2][0] = config_parse["HARDWARE"]["CHARGER"]
            self.host = config_parse["NET"]["IP"]
            self.port = config_parse["NET"]["PORT"]
            self.key = config_parse["ENCRYPT"]["KEY"]
            self.key = MD5.new(self.key).hexdigest()
            self.key = self.key.encode(encoding = "ascii", errors = "replace")
            self.hmac_key = config_parse["ENCRYPT"]["HMAC_KEY"]
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
        self.root.mainloop()
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
        confirm = Raspbot.receive_acknowledgement(self)
        if confirm is False:
            return None
        pass
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
        # confirm = Raspbot.receive_acknowledgement(self)
        # if confirm is False:
        #     return None
        # pass
        # self.socket.sendall(hash_public)
        # confirm = Raspbot.receive_acknowledgement(self)
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
            raise EncryptionError("[FAIL]: Message is not authentic, failed HMAC validation!")
        pass
        ciphering = Salsa20.new(self.key, nonce = nonce)
        return ciphering.decrypt(encrypted_input)
    pass
    def receive_acknowledgement(self):
        """Listens for an acknowledgement byte string, returns booleans whether string was received or failed."""
        acknowledgement = b""
        try:
            acknowledgement = self.socket.recv(30)
        except socket.error:
            print("[FAIL]: Failed to receive acknowledgement string.")
        if acknowledgement == b"rca-1.2:connection_acknowledge":
            print("[INFO]: Received acknowledgement.")
            return True
        else:
            self.connect_retries += 1
            if self.connect_retries < 5:
                print("[FAIL]: Acknowledgement failed, retrying...")
                self.socket.close()
                Raspbot.connect(self)
            else:
                print("[FAIL]: Acknowledgement failed more than 5 times. Stopping connection...")
                self.socket.close()
                return False
                pass
            pass
        pass
    pass
pass

r = Raspbot()
r.connect()