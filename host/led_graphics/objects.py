"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1, revised for v1.2
led_graphics module. for controlling onboard LED matrix
Made by perpetualCreations

Contains objects for module, including any package imports. Interact with these objects through led_graphics.objects.
"""

try:
    from basics import basics
    import sense_hat
    from time import sleep
    import configparser
except ImportError as e:
    print("[FAIL]: Imports failed! See below for details.")
    print(e)
    basics.exit(1)
except ImportWarning as e:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(e)
    basics.exit(1)
pass

components = [[None], [None, None, None], [None], [None, None]] # components list, overwritten by __init__
sense = None # SenseHAT object, overwritten by __init__ after reading hardware configuration
