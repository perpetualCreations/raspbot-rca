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

        with connection:
            print("[INFO]: Received connection from ", client_address, ".")
            comms.acknowledge.send(1000)
            data = SHA3_512.new(comms.interface.receive()).hexdigest().encode(encoding = "ascii", errors = "replace")
            if data == self.auth:
                print("[INFO]: Client authenticated!")
                comms.acknowledge.send(1000)
            else:
                print("[FAIL]: Client authentication invalid! Given code does not match authentication code.")
                comms.acknowledge.send_acknowledgement(2001)
                comms.objects.socket.close(1)
                basics.restart_shutdown.restart()
            pass
            while True:
                command = comms.interface.receive()
                if command == b"rca-1.2:command_shutdown":
                    comms.acknowledge.send_acknowledgement(1000)
                    basics.restart_shutdown.shutdown()
                elif command == b"rca-1.2:command_reboot":
                    comms.acknowledge.send(1000)
                    basics.restart_shutdown.reboot()
                elif command == b"rca-1.2:command_update":
                    comms.acknowledge.send(1000)
                    basics.basics.os_update()
                elif command == b"rca-1.2:command_battery_check":
                    comms.acknowledge.send(1000)
                elif command == b"rca-1.2:command_science_collect":
                    comms.acknowledge.send(1000)
                    if self.components[1][0] is True or self.components[1][1] is True or self.components[1][2]:
                        connection.sendall(host.send(self, science.science.get()))
                    else:
                        connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                    pass
                elif command == b"rca-1.2:nav_start":
                    comms.acknowledge.send(1000)
                    nav_command = comms.interface.receive().decode(encoding = "utf-8", errors = "replace")
                    nav_command_list = nav_command.split()
                    basics.basics.serial("/dev/ttyACM0", "send", nav_command_list[0].encode(encoding = "ascii", errors = "replace"))
                    basics.process.create_process(host.nav_timer, (self, int(nav_command_list[1]), literal_eval(nav_command_list[2])))
                elif command == b"rca-1.2:disconnected":
                    comms.objects.socket.close(0)
                    print("[INFO]: Client has disconnected.")
                    basics.restart_shutdown.restart()
                elif command == b"rca-1.2:led_graphics":
                    comms.acknowledge.send(1000)
                    if self.components[1][0] is True and self.components[1][1] is True and self.components[1][2] is True:
                        led_command = comms.interface.receive().decode(encoding = "utf-8", errors = "replace")
                        if led_command == b"play":
                            raise NotImplementedError
                        elif led_command == b"image":
                            comms.acknowledge.send(1000)
                            led_graphics.led_graphics.display("image", self.pattern_led[
                                int(comms.interface.receive().decode(encoding = "utf-8", errors = "replace"))])
                        elif led_command == b"stop":
                            comms.acknowledge.send(1000)
                            led_graphics.led_graphics.display("stop", None)
                        pass
                    else:
                        connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                    pass
                elif command == b"rca-1.2:command_ch_check":
                    comms.acknowledge.send(1000)
                    hardware_check.computer_hardware_check.collect()
                    hardware_check.computer_hardware_check.convert()
                    connection.sendall(host.send(self, hardware_check.computer_hardware_check.report()))
                elif command == b"rca-1.2:get_dock_status":
                    if self.components[2][0] is True:
                        comms.acknowledge.send(1000)
                        dock_status_str = str(self.dock_status)
                        connection.sendall(host.send(self, dock_status_str.encode(encoding = "ascii", errors = "replace")))
                    else:
                        connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                    pass
                elif command == b"rca-1.2:command_dock":
                    if self.components[2][0] is True:
                        pass
                        # TODO write dock logic
                    else:
                        connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                    pass
                elif command == b"rca-1.2:command_undock":
                    if self.components[2][0] is True:
                        pass
                        # TODO write undock logic
                    else:
                        connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                    pass
                else:
                    connection.sendall(host.send(self, b"rca-1.2:unknown_command"))
                pass  # add more keys here
            pass
        pass
    pass
pass

h = host()
