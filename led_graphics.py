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
        self.display_current = ""
        root = tkinter.Tk()
        root.title("Raspbot RCA-G: LED Graphics Control")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(260, 131))
        root.resizable(width=False, height=False)
        graphics_title = tkinter.Label(root, text = "LED Controls", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 0, column = 0, padx = (0, 290))
        graphics_led_frame_buttons = tkinter.Frame(root, bg = "#344561")
        graphics_led_button_off = tkinter.Button(graphics_led_frame_buttons, text = "Off", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: led_graphics.display(self, "stop", None))
        graphics_led_button_off.pack(side = tkinter.TOP)
        graphics_led_button_hello_world = tkinter.Button(graphics_led_frame_buttons, text = "Hello World", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: led_graphics.display(self, "image", self.helloworld))
        graphics_led_button_hello_world.pack(side = tkinter.BOTTOM)
        graphics_led_button_idle = tkinter.Button(graphics_led_frame_buttons, text = "Idle", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: led_graphics.display(self, "image", self.idle))
        graphics_led_button_idle.pack(side=tkinter.BOTTOM)
        graphics_led_frame_buttons.grid(row = 2, column = 0, padx = (0, 250))
        root.mainloop()
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
