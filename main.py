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
    from crypto import RSA
    from crypto import Random
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
        print("[INFO]: Loading configurations...")
        with configparser as c:
            c.open("main.cfg", "w+")
        print("[INFO]: Starting GUI...")
        self.root = tkinter.Tk()
        self.root.title("Raspbot RCA: Client")
        self.root.configure(bg = "#344561")
        self.root.geometry('{}x{}'.format(400, 370))
        self.root.resizable(width=False, height=False)
        graphics_title = tkinter.Label(self.root, text = "Science", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 0, column = 0, padx = (0, 500))
        self.graphics_science = tkinter.Text(self.root, height = 15)
        self.graphics_science.configure(state = tkinter.DISABLED)
        self.graphics_science.grid(row = 1, column = 0, pady = (5, 14))
        graphics_science_frame_buttons = tkinter.Frame(self.root, bg = "#344561")
        graphics_science_button_reload = tkinter.Button(graphics_science_frame_buttons, text = "Refresh", fg = "white", bg = "#344561", width = 40, font = ("Calibri", 12), command = lambda: science.science_get(self))
        graphics_science_button_reload.pack(side = tkinter.TOP)
        graphics_science_button_save = tkinter.Button(graphics_science_frame_buttons, text = "Save", fg = "white", bg = "#344561", width = 40, font = ("Calibri", 12), command = lambda: science.science_save(self))
        graphics_science_button_save.pack(side = tkinter.BOTTOM)
        graphics_science_frame_buttons.grid(row = 2, column = 0, padx = (0, 250))
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
