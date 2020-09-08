"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, contains functions for socket communications.
Made by perpetualCreations

Camera feed capturing to be put through multiprocessing and initial transmission handle functions.
"""

from comms import objects

def capture():
    """
    Captures VideoStream and sends to client, for multiprocessing.
    """
    while True:
        objects.camera_send.send_image(objects.host, objects.camera_stream.read())
    pass
pass

def connect():
    """
    Connects to client. Should be ran after initial socket connection protocol has finished.
    """
    print("[INFO]: Initiating camera stream...")
    objects.camera_send = objects.imagezmq.ImageSender(connect_to = "tcp://" + objects.client_address[0] + ":" + str(objects.cam_port))
    objects.camera_stream = VideoStream(usePiCamera = False).start()
    sleep(2)
    objects.process_camera_capture = objects.process.create_process(capture, ())
pass
