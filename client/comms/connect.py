"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by Taian Chen

Contains connect function.
"""

from comms import objects, interface, disconnect, acknowledge

def connect():
    """
    Connects to an IP with port number, and starts an encrypted connection.
    :return: none.
    """
    print("[INFO]: Creating socket connection...")
    try:
        objects.socket.connect((objects.host, objects.port))
    except objects.socket.error as se:
        print("[FAIL]: Failed to connect! See below for details.")
        print(se)
        objects.messagebox.showerror("Raspbot RCA: Connection Failed", "While connecting to the bot for main communications an error was raised. Please see console output for more details.")
    pass
    if acknowledge.receive_acknowledgement() is False:
        return None
    pass
    interface.send(objects.auth)
    if acknowledge.receive_acknowledgement() is False:
        print("[INFO]: Closing connection due to invalid authentication...")
        disconnect.disconnect()
        return None
    pass
    print("[INFO]: Successfully connected to host!")
    print("[INFO]: Creating socket connection (for camera view)...")
    try:
        objects.socket_camera.connect((objects.host, objects.cam_port))
    except objects.socket.error as sce:
        print("[FAIL]: Failed to connect! See below for details.")
        print(sce)
        objects.messagebox.showerror("Raspbot RCA: Connection Failed", "While connecting to the bot for camera view, an error was raised. Please see console output for more details.")
    pass
    if acknowledge.receive_acknowledgement() is False:
        return None
    pass
    interface.send(objects.auth)
    if acknowledge.receive_acknowledgement() is False:
        print("[INFO]: Closing connection due to invalid authentication...")
        disconnect.disconnect()
    pass
    print("[INFO]: Successfully connected to host (for camera view)!")
    if objects.components[2][0]:
        interface.send(b"rca-1.2:get_dock_status")
        objects.dock_status = objects.literal_eval(interface.receive().decode(encoding = "utf-8", errors = "replace"))
        print("[INFO]: Updated dock status from host.")
    pass
    objects.messagebox.showinfo("Raspbot RCA: Connection Successful", "You are now connected to the bot." + "\n Bot IP (in case you want to use SSH): " + objects.host)
    objects.net_status_data.set("Status: " + "Connected")
pass
