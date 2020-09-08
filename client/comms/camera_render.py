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
    TODO update from example
    :return: none.
    """
    while True:
        rpi_name, image = image_hub_receive
        cv2.imshow(rpi_name, image)
        cv2.waitKey(1)
        image_hub.send_reply(b"OK")
    pass
pass
