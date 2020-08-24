"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by Taian Chen

Contains objects for module, including any package imports. Interact with these objects through comms.objects.
"""

try:
    import tkinter
    from tkinter import messagebox
    from platform import system
    from subprocess import call, Popen
    from time import sleep
    import socket
    from Cryptodome.Cipher import Salsa20
    from Cryptodome.Hash import HMAC, SHA256, MD5
    import configparser
    from ast import literal_eval
    from os import getcwd
except ImportError as ImportErrorMessage:
    socket = None
    print("[NAV][FAIL]: Import failed!")
    print(ImportErrorMessage)
except ImportWarning as ImportWarningMessage:
    print("[NAV][FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
pass

key = None # Salsa20 encryption key
hmac_key = None # HMAC replay attack mitigation key
auth = None # Authentication key

host = None # host IP address
port = 64220 # default port config, is overwritten by configuration file read
cam_port = 64221 # default port config, is overwritten by configuration file read

socket_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_main.setblocking(False)
socket_main.settimeout(10)
socket_camera = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_camera.setblocking(False)
socket_camera.settimeout(10)

dock_status = None # TODO have main reference this instead.
components = [[None], [None, None, None], [None], [None, None]] # components list, overwritten by __init__

net_status_data = tkinter.StringVar() # TODO have main reference this variable, and have an update function invoked after a connect/disconnect
