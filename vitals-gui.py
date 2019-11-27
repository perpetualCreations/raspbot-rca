"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1
# vitals-gui module (for creating a GUI for vitals.py)
# creates GUI
# Made by Taian Chen (perpetualCreations)
"""

try:
    print("[INFO]: Starting imports...")
    import tkinter
    from vitals import vitals
    from time import gmtime
    from time import strftime
except ImportError as e:
    tkinter = None
    vitals = None
    gmtime = None
    strftime = None
    print("[FAIL]: Imports failed! See below.")
    print(e)
    exit(1)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

class vitals_gui:
    """Creates a GUI interface for user to access the Vitals module of Raspbot RCA-G"""
    def __init__(self):
        print("[INFO]: Vitals GUI loaded!")
        print("[INFO]: Loading graphics...")
        self.content = ""
        root = tkinter.Tk()
        root.title("Raspbot RCA-G: Vitals")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(400, 370))
        root.resizable(width=False, height=False)
        graphics_title = tkinter.Label(root, text = "Bot Vitals", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 0, column = 0, padx = (0, 500))
        self.graphics_vitals = tkinter.Text(root, height = 15)
        self.graphics_vitals.configure(state = tkinter.DISABLED)
        self.graphics_vitals.grid(row = 1, column = 0, pady = (5, 14))
        graphics_vitals_frame_buttons = tkinter.Frame(root, bg = "#344561")
        graphics_vitals_button_reload = tkinter.Button(graphics_vitals_frame_buttons, text = "Refresh", fg = "white", bg = "#344561", width = 40, font = ("Calibri", 12), command = lambda: vitals_gui.vitals_get(self))
        graphics_vitals_button_reload.pack(side = tkinter.TOP)
        graphics_vitals_button_save = tkinter.Button(graphics_vitals_frame_buttons, text = "Save", fg = "white", bg = "#344561", width = 40, font = ("Calibri", 12), command = lambda: vitals_gui.vitals_save(self))
        graphics_vitals_button_save.pack(side = tkinter.BOTTOM)
        graphics_vitals_frame_buttons.grid(row = 2, column = 0, padx = (0, 250))
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
