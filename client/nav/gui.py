

def nav_load_gui(self):
    """
    Creates GUI for loading navigation script.
    :return: none.
    """
    root = tkinter.Toplevel()
    root.title("Raspbot RCA: Nav Load")
    root.configure(bg="#344561")
    root.geometry('{}x{}'.format(260, 131))
    root.resizable(width=False, height=False)
    graphics_title = tkinter.Label(root, text="Enter script name to load.", fg="white", bg="#344561",
                                   font=("Calibri", 16))
    graphics_title.grid(row=0, column=0)
    graphics_entry = tkinter.Entry(root, bg="white", fg="black", font=("Calibri", 12))
    graphics_entry.grid(row=1, column=0, padx=(10, 0))
    graphics_confirm_button = tkinter.Button(root, bg="white", fg="black", text="Confirm", width=8, height=1,
                                             font=("Calibri", 12),
                                             command=lambda: client.nav_load(self, graphics_entry.get()))
    graphics_confirm_button.grid(row=2, column=0, padx=(10, 0), pady=(5, 0))
    root.mainloop()
pass