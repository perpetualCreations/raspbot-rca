"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through comms.objects.
"""

try:
    import socket, configparser, imagezmq, cv2
    from imutils.video import VideoStream
    from platform import system
    from time import sleep
    from Cryptodome.Cipher import Salsa20
    from Cryptodome.Hash import HMAC, SHA256, MD5
    from ast import literal_eval
    from basics import basics, process, restart_shutdown
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

host = None # host address goes here, for binding socket
port = 64220 # default port config, is overwritten by configuration file read
cam_port = 64221 # default port config, is overwritten by configuration file read
telemetry_port = 64222 # default port config, is overwritten by configuration file read

dock_status = None
components = [[None], [None, None, None], [None], [None, None]] # components list, overwritten by __init__

acknowledgement_dictionary = {1000:"rca-1.2:connection_acknowledge", 2001:"rca-1.2:authentication_invalid", 2002:"rca-1.2:unknown_command", 2003:"rca-1.2:hardware_unavailable"} # look up dictionary to convert numeric ID codes to readable alphabetical IDs
acknowledgement_id = None # placeholder, will be overwritten by lookup with acknowledgement_dictionary
acknowledgement_num_id = None # placeholder, will be overwritten by receiving socket input

socket_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket object for initial connection.
socket_init.settimeout(10)
socket_init.setblocking(True)
socket_main = None # actually the connection object, gets overwritten by connection accept in main
socket_telemetry_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_telemetry_init.settimeout(10)
socket_telemetry_init.setblocking(True)
socket_telemetry = None # like socket_main, connection object for telemetry, gets overwritten by comms.telemetry

client_address = None # client IP address

camera_sender = None # ImageZMQ's ImageSender object
camera_stream = None # VideoStream object

process_camera_capture = None # placeholder for multithreading object that runs capturing
process_camera_capture_kill_flag = False # flag variable that holds a boolean, when True camera_capture process is killed.

process_telemetry_broadcast = None # placeholder for multithreading object that runs telemetry broadcast
process_telemetry_broadcast_kill_flag = False # flag variable that holds a boolean, when True telemetry_broadcast process is killed.
