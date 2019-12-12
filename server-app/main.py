"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
# Made by Taian Chen
"""

try:
    import configparser
    import socket
except ImportError as e:
    configparser = None
    socket = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class server:
    """Main class."""
    def __init__(self):
        """Initiation function of RCA. Reads configs and starts boot processes."""
        print("[INFO]: ")