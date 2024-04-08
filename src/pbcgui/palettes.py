from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


class AppPalette(QPalette):
    """Sets the palette for the app"""
    def __init__(self):
        super().__init__()

        # Define colors
        white = QColor(255, 255, 255)
        light_grey = QColor(224, 224, 224)
        medium_grey = QColor(189, 189, 189)
        dark_grey = QColor(117, 117, 117)
        light_blue = QColor(144, 202, 249)
        medium_blue = QColor(33, 150, 243)
        dark_blue = QColor(25, 118, 210)

        self.setColor(QPalette.Window, QColor(240, 240, 240))  # Light grey background
        self.setColor(QPalette.WindowText, Qt.black)  # Black text on light background
        self.setColor(QPalette.Base, QColor(255, 255, 255))  # White background for input fields
        self.setColor(QPalette.AlternateBase, QColor(240, 240, 240))  # Light grey background for alternate elements
        self.setColor(QPalette.ToolTipBase, Qt.white)  # White tooltip background
        self.setColor(QPalette.ToolTipText, Qt.black)  # Black tooltip text
        self.setColor(QPalette.Text, Qt.black)  # Black text on light background
        self.setColor(QPalette.Button, QColor(240, 240, 240))  # Light grey buttons
        self.setColor(QPalette.ButtonText, Qt.black)  # Black text on buttons
        self.setColor(QPalette.BrightText, Qt.red)  # Bright red text for alerts
        self.setColor(QPalette.Link, QColor(42, 130, 218))  # Blue links
        self.setColor(QPalette.Highlight, QColor(42, 130, 218))  # Blue highlight color
        self.setColor(QPalette.HighlightedText, Qt.white)  # White text on highlighted background


