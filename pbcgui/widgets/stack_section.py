from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QButtonGroup, QGroupBox, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QGridLayout

from ..utility import unique_names


class StackSectionWidget(QWidget):
    """Class to encapsulate stack section for sidear"""

    # 3 groups of stack buttons
    stacks_possible = [
        ['A2 Left', 'A2 Right'],
        ['B2 Left', 'B2 Right'],
        ['No Stack']
    ]

    # keyboard shortcuts
    stack_shortcuts = {
        'A2 Left': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Up),
        'A2 Right': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Right),
        'B2 Left': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Left),
        'B2 Right': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Down)
    }

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()   
        section = QGroupBox("Stack")
        section_layout = QGridLayout()
        section.setLayout(section_layout)
        layout.addWidget(section)
        
        # create the button group
        button_group = QButtonGroup()
        button_group.setExclusive(True)
        self.buttons = []

        
        for idx, stacks in enumerate(self.stacks_possible):
            for jdx, stack in enumerate(stacks):
                button = QPushButton(stack)
                button.setCheckable(True)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                shortcut = self.stack_shortcuts.get(stack)
                if shortcut:
                    button.setShortcut(shortcut)
                section_layout.addWidget(button, idx, jdx)
                self.buttons.append(button)
                button_group.addButton(button)

        self.setLayout(layout)  

    def update_buttons(self, players):
        """Updates the text of the stack buttons"""
        players = unique_names([p.split()[0] for p in players])
        self.buttons[0].setText(f'{players[1]} Left')
        self.buttons[1].setText(f'{players[1]} Right')
        self.buttons[2].setText(f'{players[3]} Right')
        self.buttons[3].setText(f'{players[3]} Left')

