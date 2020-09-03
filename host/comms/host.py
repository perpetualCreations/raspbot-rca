"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, contains functions for socket communications.
Made by perpetualCreations

Listen/run loop.
"""

def run():
    """

    """
    print("[INFO]: Creating open server socket...")
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.setblocking(False)
    self.socket.settimeout(5)
    self.socket.bind((socket.gethostname(), self.port))
    self.socket.setblocking(True)
    self.socket.listen(1)
    connection, client_address = self.socket.accept()
    self.socket.setblocking(False)
    with connection:
        print("[INFO]: Received connection from ", client_address, ".")
        connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
        data = SHA3_512.new(host.receive(self, connection.recv(4096))).hexdigest().encode(encoding="ascii",
                                                                                          errors="replace")
        if data == self.auth:
            print("[INFO]: Client authenticated!")
            connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
        else:
            print("[FAIL]: Client authentication invalid! Given code does not match authentication code.")
            connection.sendall(host.send(self, b"rca-1.2:authentication_invalid"))
            self.socket.close()
            basics.restart_shutdown.restart()
        pass
        while True:
            command = host.receive(self, connection.recv(4096))
            if command == b"rca-1.2:command_shutdown":
                connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                basics.restart_shutdown.shutdown()
            elif command == b"rca-1.2:command_reboot":
                connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                basics.restart_shutdown.reboot()
            elif command == b"rca-1.2:command_update":
                connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                basics.basics.os_update()
            elif command == b"rca-1.2:command_battery_check":
                connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
            elif command == b"rca-1.2:command_science_collect":
                connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                if self.components[1][0] is True or self.components[1][1] is True or self.components[1][2]:
                    connection.sendall(host.send(self, science.science.get()))
                else:
                    connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                pass
            elif command == b"rca-1.2:nav_start":
                connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                nav_command = host.receive(self, connection.recv(4096)).decode(encoding="utf-8", errors="replace")
                nav_command_list = nav_command.split()
                basics.basics.serial("/dev/ttyACM0", "send", nav_command_list[0].encode(encoding="ascii", errors="replace"))
                basics.process.create_process(host.nav_timer,
                                              (self, int(nav_command_list[1]), literal_eval(nav_command_list[2])))
            elif command == b"rca-1.2:disconnected":
                self.socket.close()
                print("[INFO]: Client has disconnected.")
                basics.restart_shutdown.restart()
            elif command == b"rca-1.2:led_graphics":
                connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                if self.components[1][0] is True and self.components[1][1] is True and self.components[1][2] is True:
                    led_command = host.receive(self, connection.recv(4096)).decode(encoding="utf-8", errors="replace")
                    if led_command == b"play":
                        raise NotImplementedError
                    elif led_command == b"image":
                        connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                        led_graphics.led_graphics.display("image", self.pattern_led[
                            int(host.receive(self, connection.recv(4096)).decode(encoding="utf-8", errors="replace"))])
                    elif led_command == b"stop":
                        connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                        led_graphics.led_graphics.display("stop", None)
                    pass
                else:
                    connection.sendall(host.send(self, b"rca-1.2:hardware_unavailable"))
                pass
            elif command == b"rca-1.2:command_ch_check":
                connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                hardware_check.computer_hardware_check.collect()
                hardware_check.computer_hardware_check.convert()
                connection.sendall(host.send(self, hardware_check.computer_hardware_check.report()))
            elif command == b"rca-1.2:get_dock_status":
                if self.components[2][0] is True:
                    connection.sendall(host.send(self, b"rca-1.2:connection_acknowledge"))
                    dock_status_str = str(self.dock_status)
                    connection.sendall(host.send(self, dock_status_str.encode(encoding="ascii", errors="replace")))
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
