"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

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
    from basics import basics
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

dock_status = None
components = [[None], [None, None, None], [None], [None, None]] # components list, overwritten by __init__
message_buffer_size = None # placeholder, will be overwritten by receiving socket input

acknowledgement_dictionary = {1000:"rca-1.2:connection_acknowledge", 1001:"rca-1.2:buffer_size_ok", 2000:"rca-1.2:buffer_size_over_spec", 2001:"rca-1.2:authentication_invalid", 2002:"rca-1.2:unknown_command", 2003:"rca-1.2:buffer_size_invalid"} # look up dictionary to convert numeric ID codes to readable alphabetical IDs
acknowledgement_id = None # placeholder, will be overwritten by lookup with acknowledgement_dictionary
acknowledgement_num_id = None # placeholder, will be overwritten by receiving socket input
