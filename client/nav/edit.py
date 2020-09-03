"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
nav.py module, contains navigation functions
Made by perpetualCreations

Navigation script editing interface.
"""

from nav import objects

def nav_edit():
    """
    Opens OS built-in text editor, similarly to client.set_configuration_gui().
    Also similarly to client.set_configuration_gui() will be updated to an actual editor.
    :return: none.
    """
    platform = objects.system()
    if platform in ["Linux", "Ubuntu", "Debian", "Raspbian"]:
        root = objects.tkinter.Toplevel()
        root.title("Raspbot RCA: Nav Name Entry")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(260, 131))
        root.resizable(width = False, height = False)
        graphics_title = objects.tkinter.Label(root, text = "Enter script name.", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 0, column = 0)
        graphics_entry = objects.tkinter.Entry(root, bg = "white", fg = "black", font = ("Calibri", 12))
        graphics_entry.grid(row = 1, column = 0, padx = (10, 0))
        graphics_confirm_button = objects.tkinter.Button(root, bg = "white", fg = "black", text = "Confirm", width = 8, height = 1, font = ("Calibri", 12), command = lambda: call("sudo nano " + graphics_entry.get(), shell = True))
        graphics_confirm_button.grid(row = 2, column = 0, padx = (10, 0), pady = (5, 0))
        root.mainloop()
    elif platform == "Windows":
        root = objects.tkinter.Toplevel()
        root.title("Raspbot RCA: Nav Name Entry")
        root.configure(bg = "#344561")
        root.geometry('{}x{}'.format(260, 131))
        root.resizable(width = False, height = False)
        graphics_title = objects.tkinter.Label(root, text = "Enter script name.", fg = "white", bg = "#344561", font = ("Calibri", 16))
        graphics_title.grid(row = 0, column = 0)
        graphics_entry = objects.tkinter.Entry(root, bg = "white", fg = "black", font = ("Calibri", 12))
        graphics_entry.grid(row = 1, column = 0, padx = (10, 0))
        graphics_confirm_button = objects.tkinter.Button(root, bg = "white", fg = "black", text = "Confirm", width = 8, height = 1, font = ("Calibri", 12), command = lambda: Popen(["notepad.exe", graphics_entry.get()]))
        graphics_confirm_button.grid(row = 2, column = 0, padx = (10, 0), pady = (5, 0))
        root.mainloop()
    else:
        objects.messagebox.showerror("Raspbot RCA: OS Unsupported", "Client OS is unsupported, please manually edit configuration! Open an issue on Github for your operating system to be supported.")
    pass
pass