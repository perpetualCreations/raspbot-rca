"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Logic for initial connection request handling.
"""

from comms import objects

def connect_accept():
    """
    Listens for incoming connection requests, and with socket_init creates connection object socket_main.
    """
    objects.socket_init.setblocking(False)
    objects.socket_init.settimeout(5)
    objects.socket_init.bind((objects.socket.gethostname(), objects.port))
    objects.socket_init.setblocking(True)
    objects.socket_init.listen()
    objects.socket_main, objects.client_address = objects.socket_init.accept()
    objects.socket_init.setblocking(False)
pass
