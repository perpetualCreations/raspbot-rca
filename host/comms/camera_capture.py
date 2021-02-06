"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, contains functions for socket communications.
Made by perpetualCreations

Camera feed capturing to be put through multithreading and initial transmission handle functions.
"""

from comms import objects

def capture() -> None:
    """
    Captures VideoStream and sends to client, for multithreading.
    @return: None
    """
    print("[INFO]: Camera feed capture thread has started.")
    while objects.process_camera_capture_kill_flag is False:
        result, encimg = objects.cv2.imencode('.jpg', objects.camera_stream.read(), [int(objects.cv2.IMWRITE_JPEG_QUALITY), 90]) # result is ignored, this is dirty
        objects.camera_sender.send_image(objects.socket.gethostname(), encimg)
    pass
    print("[INFO]: Camera feed capture thread has ended.")
pass

def connect() -> None:
    """
    Connects to client. Should be ran after initial socket connection protocol has finished.
    @return: None
    """
    print("[INFO]: Initiating camera stream...")
    objects.camera_sender = objects.imagezmq.ImageSender(connect_to = "tcp://" + objects.client_address[0] + ":" + str(objects.cam_port))
    objects.camera_stream = objects.VideoStream().start()
    objects.sleep(2)
    objects.process_camera_capture = objects.process.create_process(capture)
pass
