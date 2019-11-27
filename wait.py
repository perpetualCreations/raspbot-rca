# Raspbot Remote Control Application (Raspbot RCA), v1.0
# wait module (for motor activity timer), unused
# Made by Taian Chen

class wait:
    def __init__(self):
        print("[INFO]: Wait module loaded!")
    pass
    def nav_sleep(self, seconds):
        from time import sleep
        sleep(seconds)
        import serial
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        arduino.write(b"A")
        print("[INFO]: Navigation ended.")
    pass
pass
