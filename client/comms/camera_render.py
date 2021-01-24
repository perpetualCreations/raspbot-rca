"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Camera feed rendering function to be put through multiprocessing.
"""

from comms import objects

def render():
    """
    Camera render function for multiprocessing.
    :return: none.
    """
    print("[INFO]: Camera feed render is active!")
    while True:
        rpi_name, image = objects.image_hub.recv_image()
        image = objects.cv2.imdecode(image, 1)
        objects.cv2.imshow(rpi_name, image)
        objects.cv2.waitKey(1)
        objects.image_hub.send_reply(b'OK')
    pass
pass
