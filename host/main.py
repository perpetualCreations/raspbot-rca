"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Made by perpetualCreations
"""

try:
    print("[INFO]: Starting imports...")
    from time import sleep
    import socket, configparser, multiprocessing, serial, cv2
    from sys import exit as app_end
    from ast import literal_eval
    # RCA Modules, basics is first to let logging start earlier
    import basics
    # logging initiation
    basics.basics.log_init()
    import hardware_check, led_graphics, science, comms
except ImportError as ImportErrorMessage:
    print("[FAIL]: Imports failed! See below.")
    print(ImportErrorMessage)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(ImportWarningMessage)
pass

class host:
    """
    Main host class.
    """
    def __init__(self):
        """
        Initiation function of Raspbot RCA. Reads configs and starts boot processes.
        """
        print("[INFO]: Starting host Raspbot RC Application...")
        print("[INFO]: Declaring variables...")
        self.socket = None
        self.host = ""
        self.port = 64220
        self.connect_retries = 0
        self.components = [[None], [None, None, None], [None], [None, None]]  # [Base Set [cam], RFP Enceladus [sensehat, distance, dust], Upgrade #1 [charger], Robotic Arm Kit [arm, arm_cam]]
        self.dock_status = False
        print("[INFO]: Loading configurations...")
        config_parse_load = configparser.ConfigParser()
        try:
            config_parse_load.read("hardware.cfg")
            self.components[0][0] = literal_eval(config_parse_load["HARDWARE"]["cam"])
            self.components[1][0] = literal_eval(config_parse_load["HARDWARE"]["sensehat"])
            self.components[1][1] = literal_eval(config_parse_load["HARDWARE"]["distance"])
            self.components[1][2] = literal_eval(config_parse_load["HARDWARE"]["dust"])
            self.components[2][0] = literal_eval(config_parse_load["HARDWARE"]["charger"])
            self.components[3][0] = literal_eval(config_parse_load["HARDWARE"]["arm"])
            self.components[3][1] = literal_eval(config_parse_load["HARDWARE"]["arm_cam"])
        except configparser.Error as ce:
            print("[FAIL]: Failed to load configurations! See below for details.")
            print(ce)
            basics.basics.exit(1)
        except KeyError as ke:
            print("[FAIL]: Failed to load configurations! Configuration file is corrupted or has been edited incorrectly.")
            print(ke)
            basics.basics.exit(1)
        except FileNotFoundError:
            print("[FAIL]: Failed to load configurations! Configuration file is missing.")
            basics.basics.exit(1)
        pass
        if self.components[1][0] is True:
            self.pattern_led = [["error1.png", "error2.png"], ["helloworld.png"], ["idle1.png", "idle2.png"], ["power-on.png"], ["power-off.png"], ["start1.png", "start2.png", "start3.png", "start4.png"]]
        pass

    pass
pass

h = host()
