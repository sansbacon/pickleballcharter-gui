import json
import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QButtonGroup, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QSizePolicy

from ..data import Rally
from ..utility import unique_names


class PlayerSectionWidget(QWidget):
    """A widget for the player section of the sidebar"""
    
    shot_started = Signal(int)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

        # Create a layout for the section
        layout = QVBoxLayout()   
        section = QGroupBox("Player")

        # Create a layout for the section
        layout = QVBoxLayout()   
        section = QGroupBox("Player")
        section_layout = QVBoxLayout() 
        section.setLayout(section_layout)
        layout.addWidget(section)

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.buttons = []

        player_shortcuts = {
            ('A', 1): QKeySequence(Qt.ControlModifier | Qt.Key_Up),
            ('A', 2): QKeySequence(Qt.ControlModifier | Qt.Key_Right),
            ('B', 1): QKeySequence(Qt.ControlModifier | Qt.Key_Left),
            ('B', 2): QKeySequence(Qt.ControlModifier | Qt.Key_Down),
        }

        for team in ["A", "B"]:
            row_layout = QHBoxLayout()
            section_layout.addLayout(row_layout) 
            for i in range(1, 3):
                player_button = QPushButton(f"Player {team}{i}")
                player_button.setCheckable(True)
                player_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                player_button.setShortcut(player_shortcuts[(team, i)])
                row_layout.addWidget(player_button)
                self.button_group.addButton(player_button)
                self.buttons.append(player_button)

        self.button_group.buttonClicked.connect(self.emit_shot_started)
        self.setLayout(layout)

    def emit_shot_started(self, button):
        """Emits the rally started signal"""
        button_index = self.buttons.index(button)
        self.shot_started.emit(button_index)

    def reset_buttons(self):
        self.button_group.setExclusive(False)  # Disable autoExclusive
        for button in self.button_group.buttons():
            button.setChecked(False)
        self.button_group.setExclusive(True)  # Enable autoExclusive

    def update_buttons(self, players):
        """Updates the text of the stack buttons"""
        #self.logger.debug(f"Updating player buttons: {json.dumps([p.to_dict() for p in players])}")
        for idx, player in enumerate(unique_names([p.first_name for p in players])):
            self.buttons[idx].setText(player)
        