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
    from Cryptodome.Hash import SHA3_512
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
        comms.connect_accept.connect_accept()
        print("[INFO]: Received connection from ", comms.objects.client_address, ".")
        comms.acknowledge.send_acknowledgement(1000)
        data_receiving = comms.interface.receive()
        data = (SHA3_512.new(data_receiving).hexdigest()).encode(encoding = "ascii", errors = "replace")
        if data == comms.objects.auth:
            print("[INFO]: Client authenticated!")
            comms.acknowledge.send_acknowledgement(1000)
        else:
            print("[FAIL]: Client authentication invalid! Given code does not match authentication code, received: " + data.decode(encoding = "utf-8", errors = "replace") + ".")
            comms.acknowledge.send_acknowledgement(2001)
            comms.objects.socket_main.close(0)
            basics.restart_shutdown.restart()
        pass
        comms.camera_capture.connect()
        print("[INFO]: Waiting for commands...")
        while True:
            command = comms.interface.receive()
            if command == b"rca-1.2:command_shutdown":
                comms.acknowledge.send_acknowledgement(1000)
                basics.restart_shutdown.shutdown()
            elif command == b"rca-1.2:command_reboot":
                comms.acknowledge.send_acknowledgement(1000)
                basics.restart_shutdown.reboot()
            elif command == b"rca-1.2:command_update":
                comms.acknowledge.send_acknowledgement(1000)
                basics.basics.os_update()
            elif command == b"rca-1.2:command_battery_check":
                comms.acknowledge.send_acknowledgement(1000)
            elif command == b"rca-1.2:command_science_collect":
                comms.acknowledge.send_acknowledgement(1000)
                if self.components[1][0] is True or self.components[1][1] is True or self.components[1][2]:
                    comms.interface.send(science.science.get())
                else:
                    comms.interface.send(b"rca-1.2:hardware_unavailable")
                pass
            elif command == b"rca-1.2:nav_start":
                comms.acknowledge.send_acknowledgement(1000)
                nav_command = comms.interface.receive().decode(encoding = "utf-8", errors = "replace")
                nav_command_list = nav_command.split()
                basics.basics.serial("/dev/ttyACM0", "send", nav_command_list[0].encode(encoding = "ascii", errors = "replace"))
                basics.process.create_process(host.nav_timer, (self, int(nav_command_list[1]), literal_eval(nav_command_list[2])))
            elif command == b"rca-1.2:disconnected":
                basics.process.stop_process(comms.objects.process, True)
                comms.objects.socket_main.close()
                print("[INFO]: Client has disconnected.")
                basics.restart_shutdown.restart()
            elif command == b"rca-1.2:led_graphics":
                comms.acknowledge.send_acknowledgement(1000)
                if self.components[1][0] is True and self.components[1][1] is True and self.components[1][2] is True:
                    led_command = comms.interface.receive().decode(encoding = "utf-8", errors = "replace")
                    if led_command == b"play":
                        raise NotImplementedError
                    elif led_command == b"image":
                        comms.acknowledge.send_acknowledgement(1000)
                        led_graphics.led_graphics.display("image", self.pattern_led[int(comms.interface.receive().decode(encoding = "utf-8", errors = "replace"))])
                    elif led_command == b"stop":
                        comms.acknowledge.send_acknowledgement(1000)
                        led_graphics.led_graphics.display("stop", None)
                    pass
                else:
                    comms.interface.send(b"rca-1.2:hardware_unavailable")
                pass
            elif command == b"rca-1.2:command_ch_check":
                comms.acknowledge.send_acknowledgement(1000)
                hardware_check.computer_hardware_check.collect()
                hardware_check.computer_hardware_check.convert()
                comms.interface.send(hardware_check.computer_hardware_check.report().encode(encoding = "ascii", errors = "replace"))
            elif command == b"rca-1.2:get_dock_status":
                if self.components[2][0] is True:
                    comms.acknowledge.send_acknowledgement(1000)
                    dock_status_str = str(self.dock_status)
                    comms.interface.send(dock_status_str.encode(encoding = "ascii", errors = "replace"))
                else:
                    comms.interface.send(b"rca-1.2:hardware_unavailable")
                pass
            elif command == b"rca-1.2:command_dock":
                if self.components[2][0] is True:
                    pass
                    # TODO write dock logic
                else:
                    comms.interface.send(b"rca-1.2:hardware_unavailable")
                pass
            elif command == b"rca-1.2:command_undock":
                if self.components[2][0] is True:
                    pass
                    # TODO write undock logic
                else:
                    comms.interface.send(b"rca-1.2:hardware_unavailable")
                pass
            else:
               comms.interface.send(b"rca-1.2:unknown_command")
            pass  # add more keys here
            print("[INFO]: Executed command: " + command.decode(encoding = "utf-8", errors = "replace"))
        pass
    pass
pass

h = host()
