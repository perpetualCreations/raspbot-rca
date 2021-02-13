"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Made by perpetualCreations

webhelper.py, helper script for the webbrowser module.
PySide6 crashes when webbrowser is called for some reason.

Use webhelper.py as a command:
python3 webhelper.py <target-domain-here>

...Where <target-domain-here> is a web address with prefix https:// or http://
"""

import webbrowser
from sys import argv

webbrowser.open_new(argv[1])
