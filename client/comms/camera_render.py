"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Camera feed rendering function to be put through multithreading.
"""

from comms import objects

def render() -> None:
    """
    Camera render function for multithreading.
    :return: None
    """
    print("[INFO]: Camera feed render thread has started.")
    while objects.process_camera_feed_kill_flag is False:
        rpi_name, image = objects.image_hub.recv_image()
        objects.frame_current = objects.cv2.imdecode(image, 1)
        objects.camera_updated = True
        objects.camera_tick += 1
        objects.image_hub.send_reply(b'OK')
    pass
    print("[INFO]: Camera feed render thread has ended.")
pass
