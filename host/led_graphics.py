"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# led_graphics module (for controlling onboard LED matrix)
# creates GUI
# Made by Taian Chen
"""

try:
    print("[INFO]: Starting imports...")
    from sense_hat import SenseHat
    from time import sleep
    sense = SenseHat()
    import tkinter
except ImportError as e:
    SenseHat = None
    sleep = None
    tkinter = None
    print("[FAIL]: Imports failed! See below for details.")
    print(e)
    exit(1)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class led_graphics:
    def __init__(self):
        global led_graphics_beLoaded
        led_graphics_beLoaded = None
        print("[INFO]: led_graphics loaded!")
        print("[INFO]: Loading LED patterns from memory...")
        self.error = ["error1.png", "error2.png"]
        self.helloworld = ["helloworld.png"]
        self.idle = ["idle1.png", "idle2.png"]
        self.poweron = ["power-on.png"]
        self.poweroff = ["power-off.png"]
        start = ["start1.png", "start2.png", "start3.png", "start4.png"]
        print("[INFO]: Loading graphics...")

    pass
    def InvalidCommand(self):
        """Exception when entered command parameter for led_graphics is invalid."""
        print("[EXCP]: InvalidCommand, entered command parameter for led_graphics is invalid.")
        sense.clear()
    pass
    def display(self, command, frames):
        """Multi-purpose function for controlling SenseHAT's LED matrix. Accepts a command and frame parameter."""
        global led_graphics_beLoaded
        if command == "play" and frames is not None:
            print("[INFO]: led_graphics is now displaying frames (from list format).")
            while True:
                for x in frames:
                    print("[INFO]: Rendering frame...")
                    sense.set_pixels(x)
                    print("[INFO]: Rendered.")
                    sleep(1)
                pass
            pass
        elif command == "stop":
            print("[INFO]: led_graphics is now stopping display.")
            sense.clear()
            print("[INFO]: led_graphics cleared.")
        elif command == "image":
            print("[INFO]: led_graphics is now displaying frames (from image format).")
            for x in frames:
                print("[INFO]: Rendering frame...")
                sense.load_image(x)
                print("[INFO]: Rendered.")
                sleep(1)
            pass
        else:
            raise led_graphics.InvalidCommand(self)
        pass
    pass
pass

lg = led_graphics()
