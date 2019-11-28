"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# nav module (for navigation)
# creates GUI
# Made by Taian Chen (perpetualCreations)
"""

try:
    print("[INFO]: Starting imports...")
    import tkinter
    from tkinter import messagebox
    from subprocess import call
    from time import gmtime
    from time import strftime
    from time import sleep
    from sense_hat import SenseHat
    import serial
except ImportError as e:
    tkinter = None
    call = None
    gmtime = None
    strftime = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
    exit(1)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class nav:
    """Creates a GUI interface for user to start navigating."""
    def __init__(self):
        print("[INFO]: Nav loaded!")
        print("[INFO]: Starting serial connection with Arduino microcontroller...")
        self.arduino = serial.Serial('/dev/ttyACM0', 9600)
        print("[INFO]: Declaring variables...")
        self.content = ""
        self.task = ""
        self.nav_task_active = False
        self.nav_time = 0
        self.distance_check = True
        print("[INFO]: Loading graphics...")
        root = tkinter.Tk()
        root.title("Raspbot RCA-G: Navigation")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(300, 300))
        root.resizable(width = False, height = False)
        graphics_title = tkinter.Label(root, text = "Nav Controls", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 0, column = 0)
        self.graphics_nav = tkinter.Text(root, width = 4, height = 2)
        self.graphics_nav.configure(state = tkinter.DISABLED)
        self.graphics_nav.grid(row = 1, column = 0, pady = (5, 14))
        graphics_nav_frame_buttons = tkinter.Frame(root, bg = "#344561")
        graphics_nav_button_forward = tkinter.Button(graphics_nav_frame_buttons, text = "F", fg = "white", bg = "#344561", font = ("Calibri", 12), command = lambda: nav.set_task(self, "F"))
        graphics_nav_button_forward.pack(side = tkinter.TOP)
        graphics_nav_button_backward = tkinter.Button(graphics_nav_frame_buttons, text = "B", fg = "white", bg = "#344561", font = ("Calibri", 12), command = lambda: nav.set_task(self, "B"))
        graphics_nav_button_backward.pack(side = tkinter.BOTTOM)
        graphics_nav_frame_buttons_left = tkinter.Frame(graphics_nav_frame_buttons, bg = "#344561")
        graphics_nav_button_left_forward = tkinter.Button(graphics_nav_frame_buttons_left, text = "LF", fg = "white", bg = "#344561", font = ("Calibri", 12), command = lambda: nav.set_task(self, "W")) # TODO confirm correct byte command
        graphics_nav_button_left_forward.pack(side = tkinter.TOP)
        graphics_nav_button_left_backward = tkinter.Button(graphics_nav_frame_buttons_left, text = "LB", fg = "white", bg = "#344561", font = ("Calibri", 12), command = lambda: nav.set_task(self, "X"))
        graphics_nav_button_left_backward.pack(side = tkinter.BOTTOM)
        graphics_nav_frame_buttons_left.pack(side = tkinter.LEFT)
        graphics_nav_frame_buttons_right = tkinter.Frame(graphics_nav_frame_buttons, bg = "#344561")
        graphics_nav_buttons_right_forward = tkinter.Button(graphics_nav_frame_buttons_right, text = "RF", fg = "white", bg = "#344561", font = ("Calibri", 12), command = lambda: nav.set_task(self, "Y"))
        graphics_nav_buttons_right_forward.pack(side = tkinter.TOP)
        graphics_nav_buttons_right_backwards = tkinter.Button(graphics_nav_frame_buttons_right, text = "RB", fg = "white", bg = "#344561", font = ("Calibri", 12), command = lambda: nav.set_task(self, "Z"))
        graphics_nav_buttons_right_backwards.pack(side = tkinter.BOTTOM)
        graphics_nav_frame_buttons_right.pack(side = tkinter.RIGHT)
        graphics_nav_frame_buttons.grid(row = 2, column = 0, padx = (0, 50))
        root.mainloop()
    pass
    def set_task(self, task):
        """Sets task variable, because lambda doesn't support variable assignment."""
        self.task = task
    pass
    def process_command(self, direction, time):
        """Asks user for confirmation and does pre-navigation check for existing navigation , then finally executes movement."""
        confirm = messagebox.askyesno("Raspbot RCA-G: Nav Confirm", "Are you sure you want to execute this navigation?")
        if confirm is True:
            print("[INFO]: Confirmed navigation by user.")
            if self.nav_task_active is True:
                nav.stop(self)
            pass
            direction_byte = direction.encode(encoding = "ascii", errors = "replace")
            self.arduino.write(direction_byte)
            while self.nav_time != 0:
                self.arduino.write(b"T")
                distance = self.arduino.read_until()
                distance.encode(encoding = "utf-8", errors = "replace")
                if distance > 30 and self.distance_check is True:
                    print("[FAIL]: Distance from object facing front of vehicle is less than 30mm! Collision warning!")
                    nav.stop(self)
                    messagebox.showwarning("Raspbot RCA-G: Collision Warning!", "The ToF distance sensor has detected an object less than 30mm away. A dialogue will appear to resume or stop navigation.")
                    str_nav_time = str(self.nav_time)
                    override = messagebox.askyesno("Raspbot RCA-G: Nav Confirm", "Override and resume navigation? Your current nav has " + str_nav_time + " left.")
                    if override is True:
                        print("[INFO]: Continued navigation.")
                        self.distance_check = False
                    else:
                        print("[INFO]: Ended navigation early due to collision warning.")
                        return None # TODO test and see if not clearing navigation variables has any negative effects on next navigation
                    pass
                else:
                    sleep(1)
                pass
            pass
            if self.nav_time == 0:
                nav.stop(self)
                print("[INFO]: Ended navigation, task complete!")
            pass
        else:
            print("[INFO]: Cancelled navigation by user.")
        pass
    pass
    def stop(self):
        """Stops navigation."""
        print("[INFO]: Stopped navigation.")
        self.arduino.write(b"A")
    pass
pass

