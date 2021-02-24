"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Contains connect function.
"""

from comms import objects, interface, disconnect, acknowledge, camera_render

def connect() -> None:
    """
    Connects to an IP with port number, and starts an encrypted connection.
    :return: None
    """
    if objects.is_connected is True: return None
    print("[INFO]: Creating socket connection with " + objects.host + " on port " + str(objects.port) + "...")
    try: objects.socket_main.connect((objects.host, objects.port))
    except objects.socket.error as SocketErrorMessage:
        print("[FAIL]: Failed to connect! See below for details.")
        print(SocketErrorMessage)
        objects.messagebox.showerror("Raspbot RCA: Connection Failed", "While connecting to the bot for main communications an error was raised.\n" + str(SocketErrorMessage))
        disconnect.disconnect()
        return None
    pass
    if acknowledge.receive_acknowledgement() is False:
        disconnect.disconnect()
        return None
    pass
    interface.send(objects.auth)
    if acknowledge.receive_acknowledgement() is False:
        print("[FAIL]: Closing connection due to invalid authentication...")
        disconnect.disconnect()
        return None
    pass
    print("[INFO]: Trying to connect to telemetry stream...")
    objects.process_telemetry_refresh_kill_flag = False
    try: objects.socket_telemetry.connect((objects.host, 64222))
    except objects.socket.error as SocketErrorMessage:
        print("[FAIL]: Failed to connect! See below for details.")
        print(SocketErrorMessage)
        objects.messagebox.showerror("Raspbot RCA: Connection Failure", "While connecting to the bot for telemetry communications an error was raised.\n" + str(SocketErrorMessage))
        disconnect.disconnect()
        return None
    pass
    print("[INFO]: Trying to start camera feed...")
    if objects.image_hub is None: objects.image_hub = objects.imagezmq.ImageHub(open_port = ("tcp://" + objects.socket_main.getsockname()[0] + ":" + str(objects.cam_port)))
    objects.process_camera_feed_kill_flag = False
    objects.process_camera_feed = objects.process.create_process(camera_render.render)
    print("[INFO]: Successfully connected to host!")
    objects.socket_main.setblocking(True) # blocking keeps on getting disabled
    if objects.components[2][0]:
        interface.send(b"rca-1.2:get_dock_status")
        if acknowledge.receive_acknowledgement() is False:
            print("[FAIL]: Closing connection due to failure to retrieve dock status...")
            disconnect.disconnect()
            return None
        pass
        objects.dock_status = objects.literal_eval(interface.receive().decode(encoding = "utf-8", errors = "replace"))
        print("[INFO]: Updated dock status from host.")
    pass
    objects.messagebox.showinfo("Raspbot RCA: Connection Successful", "You are now connected to the bot." + "\n Bot IP (in case you want to use SSH): " + objects.host)
    objects.is_connected = True
pass
