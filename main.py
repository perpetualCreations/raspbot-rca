"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# Made by Taian Chen
"""

try:
    print("[INFO]: Starting imports...")
    import time
    import os
    from subprocess import call
    from subprocess import Popen
    from time import sleep
except ImportError as e:
    time = None
    os = None
    tkinter = None
    call = None
    Popen = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class Raspbot:
    """Main class."""
    def __init__(self):
        """Initiation function of Raspbot RCA."""
        print("[INFO]: Starting Raspbot RC Application...")
        print("[INFO]: Retrieving current directory.")
        print("[INFO]: Starting other modules...")
        print("[INFO]: Starting module cmdline...")
        Popen("sudo python3 cmdline.py", shell = True)
        print("[INFO]: Starting module science...")
        Popen("sudo python3 science.py", shell = True)
        print("[INFO]: Starting module vitals-gui...")
        Popen("sudo python3 vitals-gui.py", shell = True)
        print("[INFO]: Starting module nav...")
        Popen("sudo python3 nav.py", shell = True)
        print("[INFO]: Starting module led_graphics...")
        Popen("sudo python3 led_graphics.py", shell = True)
        print("[INFO]: Starting live view from Pyimagesearch.")
        Popen("sudo python3 tkinter-photo-booth/photo_booth.py", shell = True)
        root = tkinter.Tk()
        root.title("Raspbot RCA-G: Main")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(260, 197))
        root.resizable(width=False, height=False)
        icon = tkinter.PhotoImage(file = "/home/pi/icon.png")
        graphics_icon = tkinter.Label(root, bg = "#344561", image = icon)
        graphics_icon.grid(row = 0, column = 0, pady = (2, 2), padx = (20, 0))
        graphics_title = tkinter.Label(root, text = "Main", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 1, column = 0, padx = (0, 290))
        graphics_main_frame_buttons = tkinter.Frame(root, bg = "#344561")
        graphics_main_button_off = tkinter.Button(graphics_main_frame_buttons, text = "Shutdown", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: call("sudo shutdown now", shell = True))
        graphics_main_button_off.pack(side = tkinter.TOP)
        graphics_main_button_hello_world = tkinter.Button(graphics_main_frame_buttons, text = "Reboot", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: call("sudo reboot now", shell = True))
        graphics_main_button_hello_world.pack(side = tkinter.BOTTOM)
        graphics_main_button_idle = tkinter.Button(graphics_main_frame_buttons, text = "Exit", fg = "white", bg = "#344561", width = 30, font = ("Calibri", 12), command = lambda: call("sudo pkill python3"), shell = True)
        graphics_main_button_idle.pack(side=tkinter.BOTTOM)
        graphics_main_frame_buttons.grid(row = 2, column = 0, padx = (0, 250))
        root.mainloop()
    pass
pass

r = Raspbot()
