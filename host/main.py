"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Made by perpetualCreations
"""

try:
    print("[INFO]: Starting imports...")
    import cv2
    from sys import exit as app_end
    from ast import literal_eval
    from Cryptodome.Hash import SHA3_512
    # RCA Modules, basics is first to let logging start earlier
    import basics
    # logging initiation
    # basics.basics.log_init()
    # TODO uncomment host logging init, this was for dev
    from science import science
    import hardware_check, comms, led_graphics, telemetry
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
        print("[INFO]: Loading configurations...")
        self.components = basics.basics.load_hardware_config()
        if self.components[1][0] is True:
            self.pattern_led = [["error1.png", "error2.png"], ["helloworld.png"], ["idle1.png", "idle2.png"], ["power-on.png"], ["power-off.png"], ["start1.png", "start2.png", "start3.png", "start4.png"]]
            for x in range(0, len(self.pattern_led)):
                for y in range(0, len(self.pattern_led[x])): self.pattern_led[x][y] = "led_graphics_patterns/" + self.pattern_led[x][y]
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
            command = b"rca-1.2:disconnected"
            try: command = comms.interface.receive()
            except comms.objects.socket.error:
                print("[FAIL]: Socket error occurred while listening for command.")
                comms.disconnect.disconnect()
            if command == b"rca-1.2:command_shutdown":
                comms.acknowledge.send_acknowledgement(1000)
                comms.disconnect.disconnect()
                basics.restart_shutdown.shutdown()
            elif command == b"rca-1.2:command_reboot":
                comms.acknowledge.send_acknowledgement(1000)
                comms.disconnect.disconnect()
                basics.restart_shutdown.reboot()
            elif command == b"rca-1.2:command_update":
                comms.acknowledge.send_acknowledgement(1000)
                basics.basics.os_update()
            elif command == b"rca-1.2:command_battery_check":
                comms.acknowledge.send_acknowledgement(1000)
            elif command == b"rca-1.2:command_science_collect":
                sensor_interface = science()
                if self.components[1][0] is True or self.components[1][1] is True or self.components[1][2]:
                    comms.acknowledge.send_acknowledgement(1000)
                    comms.interface.send(sensor_interface.get())
                else: comms.acknowledge.send_acknowledgement(2003)
            elif command == b"rca-1.2:nav_start":
                comms.acknowledge.send_acknowledgement(1000)
                nav_command = comms.interface.receive().decode(encoding = "utf-8", errors = "replace")
                nav_command_list = nav_command.split()
                basics.serial.serial(direction = "send", message = nav_command_list[0])
                basics.process.create_process(basics.serial.nav_timer, (self, int(float(nav_command_list[1])), literal_eval(nav_command_list[2])))
            elif command == b"rca-1.2:disconnected":
                comms.disconnect.disconnect()
            elif command == b"rca-1.2:led_graphics":
                comms.acknowledge.send_acknowledgement(1000)
                led_interface = led_graphics.ledGraphics()
                if led_interface.sense is not None:
                    led_command = comms.interface.receive().decode(encoding = "utf-8", errors = "replace")
                    print("[INFO]: LED display control received command: " + led_command)
                    if led_command == "play": raise NotImplementedError
                    elif led_command == "image":
                        comms.acknowledge.send_acknowledgement(1000)
                        led_interface.display("image", self.pattern_led[int(comms.interface.receive().decode(encoding = "utf-8", errors = "replace"))])
                    elif led_command == "stop":
                        comms.acknowledge.send_acknowledgement(1000)
                        led_interface.display("stop")
                    pass
                else: comms.acknowledge.send_acknowledgement(2003)
            elif command == b"rca-1.2:command_ch_check":
                comms.acknowledge.send_acknowledgement(1000)
                check_interface = hardware_check.hardwareCheck()
                comms.interface.send(check_interface.collect().encode(encoding = "ascii", errors = "replace"))
            elif command == b"rca-1.2:get_telemetry":
                comms.acknowledge.send_acknowledgement(1000)
                telemetry_interface = telemetry.telemetry()
                comms.interface.send(telemetry_interface.get())
            elif command == b"rca-1.2:get_dock_status":
                if self.components[2][0] is True:
                    comms.acknowledge.send_acknowledgement(1000)
                    comms.interface.send(str(basics.objects.dock_status).encode(encoding = "ascii", errors = "replace"))
                else: comms.acknowledge.send_acknowledgement(2003)
            elif command == b"rca-1.2:command_dock":
                if self.components[2][0] is True: basics.serial.dock()
                else: comms.acknowledge.send_acknowledgement(2003)
            elif command == b"rca-1.2:command_undock":
                if self.components[2][0] is True: basics.serial.undock()
                else: comms.acknowledge.send_acknowledgement(2003)
            else: comms.acknowledge.send_acknowledgement(2002)
            pass  # add more keys here
            print("[INFO]: Executed command: " + command.decode(encoding = "utf-8", errors = "replace"))
        pass
    pass
pass

if __name__ == "__main__": host()
