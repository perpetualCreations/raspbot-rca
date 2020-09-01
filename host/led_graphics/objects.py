"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1, revised for v1.2
led_graphics module. for controlling onboard LED matrix
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through led_graphics.objects.
"""

try:
    import sense_hat
    from time import sleep
except ImportError as e:
    sense_hat = None
    sleep = None
    print("[FAIL]: Imports failed! See below for details.")
    print(e)
    exit(1)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
pass

sense = sense_hat.SenseHat()
