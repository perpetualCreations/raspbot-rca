"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# cmdline module (for functions that did not receive a gui)
# Made by Taian Chen
"""

try:
    print("[INFO]: Starting imports...")
    import time
    import os
    from subprocess import call
    import serial
    import tkinter
    from time import sleep
except ImportError as e:
    time = None
    os = None
    serial = None
    tkinter = None
    call = None
    sleep = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class Raspbot:
    def __init__(self):
        """Initiation function of Raspbot RCA."""
        print("[INFO]: Started cmdline!")
        Raspbot.input(self)
    pass
    def input(self):
        """Prompt for commander to give commands to the bot. Science and vitals are handled through the GUI version."""
        print("[INFO]: Text input active. Enter commands below (use cmds for list of commands).")
        command = input("~ ")
        if command == "cmds":
            print("Commands Available: ")
            print("cmds: Lists commands. \n shutdown: Shuts down the bot. \n reboot: Reboots the bot. \n exit: Closes application, however leaves bot running.")
            print("nav: Opens another prompt for user to enter a navigation task. Enter exit to close prompt.")
            print("imager: Takes picture with mounted camera, saves as an image file.")
            print("Other commands are handled through the GUI windows.")
            print("Good luck, commander.")
            Raspbot.input(self)
        elif command == "shutdown":
            Raspbot.shutdown(self)
        elif command == "reboot":
            Raspbot.reboot(self)
        elif command == "exit":
            Raspbot.application_exit(self)
        elif command == "nav":
            Raspbot.nav(self)
        elif command == "nav_stop":
            Raspbot.nav_stop(self)
        elif command == "imager":
            Raspbot.imager(self)
        else:
            print("[FAIL]: Invalid command! Please see cmds for list of valid commands.")
            Raspbot.input(self)
        pass
    pass
    def shutdown(self):
        """Shuts down the bot."""
        print("[INFO]: Shutting down bot...")
        time.sleep(3)
        from os import system
        system("sudo shutdown now")
    pass
    def reboot(self):
        """Reboots the bot."""
        print("[INFO]: Rebooting bot...")
        time.sleep(3)
        from os import system
        system("sudo reboot now")
    pass
    def application_exit(self):
        """Stops application."""
        print("[INFO]: Stopping application.")
        time.sleep(3)
        from sys import exit as appstop
        appstop(0)
    pass
    def imager(self):
        """Captures an image from USB webcam serving as a camera, saves as an image file."""
        print("[INFO]: Starting imager hardware...")
        print("[INFO]: Generating timestamps...")
        from time import gmtime
        from time import strftime
        timestamp = strftime("%b%d%Y%H%M%S"), gmtime()
        timestamp_output = timestamp[0]
        timestamp_str = str(timestamp_output)
        import pygame
        import pygame.camera
        pygame.camera.init()
        cam = pygame.camera.Camera("/dev/video0", (640, 480))
        cam.start()
        img = cam.get_image()
        cam.stop()
        image_filename = "image-" + timestamp_str + ".png"
        pygame.image.save(img, image_filename)
        print("[INFO]: Imaging finished.")
        Raspbot.input(self)
    pass
    def nav(self): #TODO troubleshoot motors and also rename motor-direction lettering
        """Gives prompt for user to enter navigation type and length."""
        print("[INFO]: Navigation input active.")
        print("[INFO]: Please enter movement type, stop to stop navigations, or type exit to leave prompt.")
        print("[INFO]: Valid navigations: F (forwards), B (backwards), W (left, forwards), X (left, backwards), Y (right, forwards), Z (right, backwards), C (spin counterclockwise), or S (spin clockwise).")
        nav_input = input("Navigation input ~ ")
        global movement, nav_type, nav_duration
        movement = ""
        nav_type = ""
        if nav_input == "F" or "f":
            movement = "forwards"
            nav_type = nav_input
            nav_type.upper()
        elif nav_input == "B" or "b":
            movement = "backwards"
            nav_type = nav_input
            nav_type.upper()
        elif nav_input == "W" or "w":
            movement = "left"
            nav_type = nav_input
            nav_type.upper()
        elif nav_input == "X" or "x":
            movement = "left, reversed"
            nav_type = nav_input
            nav_type.upper()
        elif nav_input == "Y" or "y":
            movement = "right"
            nav_type = nav_input
            nav_type.upper()
        elif nav_input == "Z" or "z":
            movement = "right, reversed"
            nav_type = nav_input
            nav_type.upper()
        elif nav_input == "C" or "c":
            movement = "counterclockwise"
            nav_type = nav_input
            nav_type.upper()
        elif nav_input == "S" or "s":
            movement = "clockwise"
            nav_type = nav_input
            nav_type.upper()
        elif nav_input == "stop" or nav_input == "STOP":
            Raspbot.nav_stop(self)
        elif nav_input == "exit" or nav_input == "EXIT":
            Raspbot.input(self)
        else:
            print("[FAIL]: Invalid value.")
            Raspbot.nav(self)
        pass
        print("[INFO]: Please enter the number the seconds to run motors.")
        nav_input = input("Navigation input ~ ")
        if "." in nav_input:
            try:
                nav_duration = float(nav_input)
            except ValueError:
                print("[FAIL]: Invalid value, not a decimal or integer, or exit command.")
                Raspbot.nav(self)
            pass
        else:
            try:
                nav_duration = int(nav_input)
            except ValueError:
                print("[FAIL]: Invalid value, not a decimal or integer, or exit command.")
                Raspbot.nav(self)
            pass
        pass
        nav_input_str = str(nav_input)
        print("You commanded to move " + movement + " for " + nav_input_str + ". Please enter Y/N to confirm/cancel.")
        confirm = input("Y/N ~ ")
        if confirm == "y" or confirm == "Y":
            print("[INFO]: Navigation active.")
            nav_type_byte = nav_type.encode(encoding = "ascii", errors = "replace")
            arduino = serial.Serial('/dev/ttyACM0', 9600)
            arduino.write(nav_type_byte)
            while nav_input != 0:
                sleep(1)
                arduino.write(b"T")
                distance = arduino.read_until()
                distance = distance.encode(encoding = "utf-8", errors = "replace")
                if distance < 30:
                    arduino.write(b"A")
                    print("[FAIL]: 30mm of distance between object in front of bot and bot chassis. Stopped navigation.")
                pass
                nav_input =- 1
            pass
            arduino.write(b"A")
            Raspbot.input(self)
        elif confirm == "n" or confirm == "N":
            print("[INFO]: Navigation cancelled.")
            Raspbot.input(self)
        else:
            print("[FAIL]: Invalid input.")
            Raspbot.nav(self)
        pass
    pass
    def nav_stop(self):
        """Stops navigation."""
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        arduino.write(b"A")
        Raspbot.input(self)
    pass
pass

r = Raspbot()
