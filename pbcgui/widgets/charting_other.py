from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QButtonGroup, QPushButton, QSizePolicy
from PySide6.QtGui import QKeySequence

from ..data import ShotOutcomes

class ShotSideWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.buttons = []
        layout = QHBoxLayout()

        # Side Widget
        section = QGroupBox("Shot Side")
        section_layout = QHBoxLayout()
        section.setLayout(section_layout)
        layout.addWidget(section)

        # Side Buttons
        shortcuts = {'Forehand': 'F', 'Backhand': 'B'}
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        for side in ['Forehand', 'Backhand']:
            button = QPushButton(side)
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setShortcut(QKeySequence(shortcuts[side]))
            section_layout.addWidget(button)
            self.button_group.addButton(button)
            self.buttons.append(button)
            
        self.setLayout(layout)


class ShotOutcomeWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.buttons = []
        layout = QHBoxLayout()

        # Outcome Widget
        section = QGroupBox("Shot Outcome")
        section_layout = QHBoxLayout()
        section.setLayout(section_layout)
        layout.addWidget(section)

        # Side Buttons
        shortcuts = {'Winner': 'W', 'Continue': 'C', 'Error Unforced': 'U', 'Error Forced': 'E'}
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        for effect in ['Winner', 'Continue', 'Error Unforced', 'Error Forced']:
            button = QPushButton(effect)
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setShortcut(QKeySequence(shortcuts[effect]))
            section_layout.addWidget(button)
            self.button_group.addButton(button)
            self.buttons.append(button)
            
        self.setLayout(layout)


class RallyWinnerWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.buttons = []
        layout = QHBoxLayout()

        # Outcome Widget
        section = QGroupBox("Rally Winner")
        section_layout = QHBoxLayout()
        section.setLayout(section_layout)
        layout.addWidget(section)

        # Side Buttons
        shortcuts = {'Serving Team': 'S', 'Receiving Team': 'R'}
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        for item in shortcuts:
            button = QPushButton(item)
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setShortcut(QKeySequence(shortcuts[item]))
            section_layout.addWidget(button)
            self.button_group.addButton(button)
            self.buttons.append(button)
            
        self.setLayout(layout)