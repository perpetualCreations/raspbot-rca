"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
nav.py module, contains navigation functions
Made by perpetualCreations

Client version of nav module.
"""

print("[INFO]: Initiating nav module...")

from nav import edit, gui, nav, objects

objects.components = objects.basics.basics.load_hardware_config()

print("[INFO]: Initiation of nav module complete!")
