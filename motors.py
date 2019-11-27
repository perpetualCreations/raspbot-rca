"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# nav module (for navigation)
# creates GUI
# Made by Taian Chen (perpetualCreations)
"""

try:
    print("[INFO]: Starting imports...")
    import tkinter
    from subprocess import call
    from time import gmtime
    from time import strftime
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
    """Creates a GUI interface for user to start navigations."""
    def __init__(self):
        print("[INFO]: Nav loaded!")
        print("[INFO]: Loading graphics...")
        self.content = ""
        root = tkinter.Tk()
        root.title("Raspbot RCA-G: Navigation")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(300, 300))
        root.resizable(width=False, height=False)
        graphics_title = tkinter.Label(root, text = "Nav Controls", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 0, column = 0)
        self.graphics_nav = tkinter.Text(root, width = 4, height = 2)
        self.graphics_nav.configure(state = tkinter.DISABLED)
        self.graphics_nav.grid(row = 1, column = 0, pady = (5, 14))
        graphics_nav_frame_buttons = tkinter.Frame(root, bg = "#344561")
        graphics_nav_button_reload = tkinter.Button(graphics_nav_frame_buttons, text = "Refresh", fg = "white", bg = "#344561", width = 40, font = ("Calibri", 12), command = lambda: nav_gui.nav_get(self))
        graphics_nav_button_reload.pack(side = tkinter.TOP)
        graphics_nav_button_save = tkinter.Button(graphics_nav_frame_buttons, text = "Save", fg = "white", bg = "#344561", width = 40, font = ("Calibri", 12), command = lambda: nav_gui.nav_save(self))
        graphics_nav_button_save.pack(side = tkinter.BOTTOM)
        graphics_nav_frame_buttons.grid(row = 2, column = 0, padx = (0, 250))
        root.mainloop()
    pass
    def vitals_get(self):
        """Calls vitals module and collects output into self.content for displaying."""
        print("[INFO]: Refreshing vitals information...")
        v = vitals()
        v.str_conversion()
        self.content = v.report()
        self.graphics_vitals.configure(state = tkinter.NORMAL)
        self.graphics_vitals.delete("1.0", tkinter.END)
        self.graphics_vitals.insert("1.0", self.content)
        self.graphics_vitals.configure(stat = tkinter.DISABLED)
    pass
    def vitals_save(self):
        """Collects self.content for saving to a text file."""
        if self.content == "":
            print("[FAIL]: No vitals data found, early exiting the function...")
            return None
        pass
        print("[INFO]: Generating timestamps...")
        timestamp = strftime("%b%d%Y%H%M%S"), gmtime()
        timestamp_output = timestamp[0]
        timestamp_str = str(timestamp_output)
        file_report_name = "vitals-report-" + timestamp_str + ".txt"
        print("[INFO]: Generating text file report...")
        file_report = open(file_report_name, "w+")
        file_report.write(self.content)
        file_report.close()
        print("[INFO]: Done!")
    pass
pass

vg = vitals_gui()

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
    if nav_task_active is True:
        Raspbot.nav_stop(self)
    pass
    print("[INFO]: Navigation active.")
    nav_type_byte = str.encode(nav_type)
    arduino = serial.Serial('/dev/ttyACM0', 9600)
    arduino.write(nav_type_byte)
    time.sleep(nav_duration)
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

