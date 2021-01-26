"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
gui.py module, user interface built with pyside2 and loaded from a .ui file.
Made by perpetualCreations

Client-only module.
"""

print("[INFO]: Initiating gui module...")

try:
    print("[INFO]: Starting imports...")
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QFile, QIODevice
    from PySide6.QtGui import *
    from sys import argv
    from basics import basics
except ImportError as ImportErrorMessage:
    print("[FAIL]: Imports failed! See below.")
    print(ImportErrorMessage)
    exit(1)
except ImportWarning as ImportWarningMessage:
    print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
    print(ImportWarningMessage)
    exit(1)
pass

print("[INFO]: Initiation of gui module complete!")

class gui:
    """
    Class for QtGUI.
    """
    def __init__(self):
        """
        Loads UI file and defines signals.
        """
        self.app = QApplication(argv)
        self.app.setWindowIcon(QIcon("favicon.ico")) # it just works
        ui_file = QFile("main.ui")
        if not ui_file.open(QIODevice.ReadOnly):
            print("[FAIL]: UI XML file is not in read-only. Is it being edited by another application?")
            basics.exit(1)
        pass
        self.loader = QUiLoader()
        self.window = self.loader.load(ui_file)
        ui_file.close()
        if not self.window:
            print("[FAIL]: UI XML file could not be loaded to generate interface.")
            print(self.loader.errorString())
            basics.exit(1)
        pass
        self.window.show()
        basics.exit(self.app.exec_())

test = gui()
