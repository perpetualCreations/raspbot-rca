"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through comms.objects.
"""

try:
    import tkinter, socket, configparser, cv2, imagezmq
    from tkinter import messagebox
    from platform import system
    from subprocess import call, Popen
    from time import sleep
    from Cryptodome.Cipher import Salsa20
    from Cryptodome.Hash import HMAC, SHA256, MD5
    from ast import literal_eval
    from basics import basics, process
except ImportError as ImportErrorMessage:
    print("[FAIL]: Import failed!")
    print(ImportErrorMessage)
    basics.exit(1)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Imports raised warnings.")
    print(ImportWarningMessage)
    basics.exit(1)
pass

key = None # Salsa20 encryption key
hmac_key = None # HMAC replay attack mitigation key
auth = None # Authentication key

host = None # host IP address
port = 64220 # default port config, is overwritten by configuration file read
cam_port = 64221 # default port config, is overwritten by configuration file read

socket_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_main.settimeout(10)
socket_main.setblocking(True)

dock_status = None
components = [[None], [None, None, None], [None], [None, None]] # components list, overwritten by __init__

root_placeholder = tkinter.Toplevel()
root_placeholder.withdraw() # prevents Tkinter from drawing a blank window, since this isn't an actual GUI, just a Toplevel object to allow net_status_data to be a tkinter.StringVar.
net_status_data = tkinter.StringVar(root_placeholder)

acknowledgement_dictionary = {1000:"rca-1.2:connection_acknowledge", 2001:"rca-1.2:authentication_invalid", 2002:"rca-1.2:unknown_command", 2003:"rca-1.2:hardware_unavailable"} # look up dictionary to convert numeric ID codes to readable alphabetical IDs
acknowledgement_id = None # placeholder, will be overwritten by lookup with acknowledgement_dictionary
acknowledgement_num_id = None # placeholder, will be overwritten by receiving socket input

image_hub = None # placeholder for ImageZMQ's ImageHub object, is overwritten by connect
process_camera_feed = None # placeholder for multiprocessing object that runs rendering
