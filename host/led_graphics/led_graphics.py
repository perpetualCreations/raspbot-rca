"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1, revised for v1.2
led_graphics module. for controlling onboard LED matrix
Made by perpetualCreations

Main module for controlling LED graphics.
"""

from led_graphics import errors, objects

def display(command, frames):
    """Multi-purpose function for controlling SenseHAT's LED matrix. Accepts a command and frame parameter."""
    if command == "play" and frames is not None:
        print("[INFO]: led_graphics is now displaying frames (from list format).")
        while True:
            for x in frames:
                print("[INFO]: Rendering frame...")
                objects.sense.set_pixels(x)
                print("[INFO]: Rendered.")
                objects.sleep(1)
            pass
        pass
    elif command == "stop":
        print("[INFO]: led_graphics is now stopping display.")
        objects.sense.clear()
        print("[INFO]: led_graphics cleared.")
    elif command == "image":
        print("[INFO]: led_graphics is now displaying frames (from image format).")
        for x in frames:
            print("[INFO]: Rendering frame...")
            objects.sense.load_image(x)
            print("[INFO]: Rendered.")
            objects.sleep(1)
        pass
    else:
        raise errors.InvalidCommand
    pass
pass
