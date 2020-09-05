"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Logic for initial connection request handling.
"""

from comms import objects

comms.objects.socket.setblocking(False)
comms.objects.socket.settimeout(5)
comms.objects.socket.bind((socket.gethostname(), self.port))
comms.objects.socket.setblocking(True)
comms.objects.socket.listen(1)
connection, client_address = comms.objects.socket.accept()
comms.objects.socket.setblocking(False)