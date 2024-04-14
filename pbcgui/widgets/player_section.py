from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QButtonGroup, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QSizePolicy

from ..utility import unique_names


class PlayerSectionWidget(QWidget):
    """A widget for the player section of the sidebar"""
    
    def __init__(self, parent=None):
        super(PlayerSectionWidget, self).__init__(parent)
        self.player_section = QGroupBox("Player")
        self.player_section_layout = QVBoxLayout()
        self.player_section.setLayout(self.player_section_layout)
    
        self.player_button_group = QButtonGroup()
        self.player_button_group.setExclusive(True)
        self.buttons = []

        player_shortcuts = {
            ('A', 1): QKeySequence(Qt.ControlModifier | Qt.Key_Up),
            ('A', 2): QKeySequence(Qt.ControlModifier | Qt.Key_Right),
            ('B', 1): QKeySequence(Qt.ControlModifier | Qt.Key_Left),
            ('B', 2): QKeySequence(Qt.ControlModifier | Qt.Key_Down),
        }

        for team in ["A", "B"]:
            row_layout = QHBoxLayout()
            self.player_section_layout.addLayout(row_layout)
            for i in range(1, 3):
                player_button = QPushButton(f"Player {team}{i}")
                player_button.setCheckable(True)
                player_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                player_button.setShortcut(player_shortcuts[(team, i)])
                row_layout.addWidget(player_button)
                self.player_button_group.addButton(player_button)
                self.buttons.append(player_button)
    
    def update_buttons(self, players):
        """Updates the text of the stack buttons"""
        for idx, player in enumerate(unique_names([p.split()[0] for p in players])):
            self.buttons[idx].setText(player)
        