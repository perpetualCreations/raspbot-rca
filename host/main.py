"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
# Made by Taian Chen
"""

try:
    import configparser
    import socket
    from subprocess import call
    import multiprocessing
    from sys import exit as app_end
    import hashlib
    from crypto.PublicKey import RSA
except ImportError as e:
    configparser = None
    socket = None
    call = None
    multiprocessing = None
    app_end = None
    hashlib = None
    RSA = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class host:
    """Main class."""
    def __init__(self):
        """Initiation function of RCA. Reads configs and starts boot processes."""
        print("[INFO]: Starting host Raspbot RC Application...")
        print("[INFO]: Declaring variables...")
        self.port = 67777
        print("[INFO]: Loading configurations...")
        config_parse = configparser.ConfigParser()
        try:
            config_parse.read("main.cfg")
            self.port = config_parse["NET"]["PORT"]
        except configparser.Error as ce:
            print("[FAIL]: Failed to load configurations! See below for details.")
            print(ce)
        except FileNotFoundError:
            print("[FAIL]: Failed to load configurations! Configuration file is missing.")
        pass
        print("[INFO]: Creating open server socket...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.socket.settimeout(10)
        self.socket.bind((socket.gethostname(), self.port))
        self.socket.listen(1)
        connection, from_address = self.socket.accept()
        with connection:
            print("[INFO]: Received connection from ", from_address, ".")
            connection.sendall(b"rca-1.2:connection_acknowledge")
            data = connection.recv(1024)
            data = data.decode(encoding = "utf-8", errors = "replace") # TODO perform auth check and rsa events

        pass
    pass
    def receive_acknowledgement(self): # TODO adapt for host
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
                host.connect(self)
            else:
                print("[FAIL]: Acknowledgement failed more than 5 times. Stopping connection...")
                self.socket.close()
                return False
                pass
            pass
        pass
    pass
    def create_process(self, target, args):
        """Creates a new process from multiprocessing."""
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
    def shutdown(self):
        """Shuts down bot."""
        call("sudo shutdown now", shell = True)
    pass
    def reboot(self):
        """Reboots bot."""
        call("sudo reboot now", shell = True)
    pass
    def exit(self):
        """Stops host application."""
        app_end(0)
    pass
    def os_update(self):
        """Updates apt packages and host operating system."""
        call("sudo apt-get update && sudo apt-get upgrade -y", shell = True)
        return True

    pass
pass
