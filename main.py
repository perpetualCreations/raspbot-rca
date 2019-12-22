"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# Made by Taian Chen
"""

try:
    print("[INFO]: Starting imports...")
    import time
    import os
    from subprocess import call
    from time import sleep
    from Cryptodome.PublicKey import RSA
    from Cryptodome import Random
    from Cryptodome.Cypher import AES
    import socket
    import configparser
    import hashlib
except ImportError as e:
    time = None
    os = None
    tkinter = None
    call = None
    Popen = None
    RSA = None
    AES = None
    Random = None
    hashlib = None
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
        self.private = None
        self.public = None
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
        print("[INFO]: Encrypting...")
        random_generator = Random.new().read
        self.private = RSA.generate(1024, random_generator)
        self.public = self.private.publickey().exportKey()
        hash_object = hashlib.sha1(self.public)
        hex_digest = hash_object.hexdigest()
        self.socket.sendall(self.public)
        confirm = Raspbot.receive_acknowledgement(self)
        if confirm is False:
            return None
        pass
        self.socket.sendall(hex_digest)
        confirm = Raspbot.receive_acknowledgement(self)
        if confirm is False:
            return None
        pass
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