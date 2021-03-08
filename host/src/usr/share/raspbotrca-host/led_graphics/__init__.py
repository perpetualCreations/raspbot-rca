"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.1, revised for v1.2
led_graphics module, for controlling onboard LED matrix
Made by perpetualCreations

Host-only module.
"""

print("[INFO]: Initiating led_graphics module...")

try:
    from basics import basics
    from time import sleep
    from typing import Union
except ImportError as ImportErrorMessage:
    print("[FAIL]: Imports failed! See below for details.")
    print(ImportErrorMessage)
    basics.exit(1)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(ImportWarningMessage)
    basics.exit(1)
pass

print("[INFO]: Initiation of led_graphics complete!")

class ledGraphics:
    """
    Class for managing LED matrix on SenseHAT.
    Only relevant if you have a SenseHAT as part of your hardware configuration.
    """
    def __init__(self) -> None:
        """
        Initiation function, loads hardware configuration and defines a few class variables.
        """
        self.components = basics.load_hardware_config()
        if self.components[1][0] is True:
            import sense_hat
            self.sense = sense_hat.SenseHat()
        else: self.sense = None

    def display(self, command: str, frames: Union[None, list] = None) -> None:
        """
        Multi-purpose function for controlling SenseHAT's LED matrix. Accepts a command and frame parameter.
        :param command: str, either 'play', 'stop', 'image', to select mode, play accepts list format and image a set of images, stop will end display and clear.
        :param frames: list, with pixel positions or set of image filenames/path, default NONE
        :return: None
        """
        if command == "play" and frames is not None:
            print("[INFO]: led_graphics is now displaying frames (from list format).")
            while True:
                for x in frames:
                    self.sense.set_pixels(x)
                    sleep(1)
                pass
            pass
        elif command == "stop":
            self.sense.clear()
            print("[INFO]: led_graphics cleared and stopped.")
        elif command == "image" and frames is not None:
            print("[INFO]: led_graphics is now displaying frames (from image format).")
            for x in frames:
                self.sense.load_image(x)
                sleep(1)
            pass
        else:
            print("[FAIL]: Entered command parameter for led_graphics module is invalid!")
            self.sense.clear()
        pass
    pass
