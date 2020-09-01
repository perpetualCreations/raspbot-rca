"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1, revised for v1.2
led_graphics module. for controlling onboard LED matrix
Made by perpetualCreations

Contains exception classes within led_graphics module.
"""

from led_graphics import objects

class InvalidCommand:
    """
    Class within led_graphics serving as an exception when a display command is invalid.
    """
    print("[FAIL]: Entered command parameter for led_graphics module is invalid!")
    objects.sense.clear()
pass