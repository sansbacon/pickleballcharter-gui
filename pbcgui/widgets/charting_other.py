from PySide6.QtCore import Signal
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QButtonGroup, QPushButton, QSizePolicy


class ShotSideWidget(QWidget):

    shot_side = Signal(str)

    def __init__(self):
        super().__init__()
        self.buttons = []
        layout = QHBoxLayout()

        # Side Widget
        section = QGroupBox("Shot Side")
        section_layout = QVBoxLayout()
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
        self.button_group.buttonClicked.connect(self.emit_shot_side)

    def emit_shot_side(self, button):
        self.shot_side.emit(button.text())

    def reset_buttons(self):
        self.button_group.setExclusive(False)  # Disable autoExclusive
        for button in self.button_group.buttons():
            button.setChecked(False)
        self.button_group.setExclusive(True)  # Enable autoExclusive


class ShotLocationWidget(QWidget):

    shot_location = Signal(str)

    def __init__(self):
        super().__init__()
        self.buttons = []
        layout = QVBoxLayout()

        # Outcome Widget
        section = QGroupBox("Shot Location")
        section_layout = QVBoxLayout()
        section.setLayout(section_layout)
        layout.addWidget(section)

        # Side Buttons
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        for location in ['LEFT_OUTSIDE', 'LEFT_INSIDE', 'CENTER', 'RIGHT_INSIDE', 'RIGHT_OUTSIDE']:
            button = QPushButton(location)
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            section_layout.addWidget(button)
            self.button_group.addButton(button)
            self.buttons.append(button)
            
        self.setLayout(layout)
        self.button_group.buttonClicked.connect(self.emit_shot_location)
        
    def emit_shot_location(self, button):
        self.shot_location.emit(button.text())

    def reset_buttons(self):
        self.button_group.setExclusive(False)  # Disable autoExclusive
        for button in self.button_group.buttons():
            button.setChecked(False)
        self.button_group.setExclusive(True)  # Enable autoExclusive


class ShotOutcomeWidget(QWidget):

    shot_over = Signal(str)

    def __init__(self):
        super().__init__()
        self.buttons = []
        layout = QHBoxLayout()

        # Outcome Widget
        section = QGroupBox("Shot Outcome")
        section_layout = QVBoxLayout()
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
        
        self.button_group.buttonClicked.connect(self.emit_shot_over)
        
    def emit_shot_over(self, button):
        self.shot_over.emit(button.text())
        self.reset_buttons()

    def reset_buttons(self):
        self.button_group.setExclusive(False)  # Disable autoExclusive
        for button in self.button_group.buttons():
            button.setChecked(False)
        self.button_group.setExclusive(True)  # Enable autoExclusive


class RallyWinnerWidget(QWidget):

    # rally over emits 'server' or 'returner' to indicate who won the rally
    # next_server emits an integer to indicate who should serve next
    rally_over = Signal(str)

    def __init__(self):
        super().__init__()
        self.buttons = []
        layout = QHBoxLayout()

        # Outcome Widget
        section = QGroupBox("Rally Winner")
        section_layout = QVBoxLayout()
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
        
        self.button_group.buttonClicked.connect(self.emit_rally_winner)
        
        self.setLayout(layout)

    def emit_rally_winner(self, button):       
        winner = 'server' if button.text() == 'Serving Team' else 'returner'
        self.rally_over.emit(winner)
        self.reset_buttons()

    def reset_buttons(self):
        self.button_group.setExclusive(False)  # Disable autoExclusive
        for button in self.button_group.buttons():
            button.setChecked(False)
        self.button_group.setExclusive(True)  # Enable autoExclusive