from PySide6.QtWidgets import QWidget, QSizePolicy, QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QButtonGroup
from PySide6.QtGui import QKeySequence

from entities import ShotTypes


class ChartGameWidget(QWidget):
    def __init__(self, parent=None):
        super(ChartGameWidget, self).__init__(parent)

        vlayout = QVBoxLayout()
        self.setLayout(vlayout)

        # Create a horizontal layout
        hlayout = QHBoxLayout()

        hlayout.addLayout(self.sidebar())
        hlayout.addLayout(self.main_column())

        hlayout.setStretch(0, 25)  # First column takes up 25% of the space
        hlayout.setStretch(1, 75)  # Second column takes up 50% of the space

        # Add the second tab to the tab widget
        vlayout.addLayout(hlayout)

    def main_column(self):
        """Creates the main column with the following sections:"""
        main_column = QVBoxLayout()

        # Create the "Shots" section
        shots_section = QGroupBox("Shots")
        shots_section_layout = QGridLayout()
        shots_section.setLayout(shots_section_layout)
        main_column.addWidget(shots_section)

        # Add shots buttons
        self.shots_button_group = QButtonGroup()
        self.shots_button_group.setExclusive(True)
        for idx, shot_type in enumerate(ShotTypes):
            j = idx % 5
            i = idx // 5
            button = QPushButton(f"{shot_type.value} - {shot_type.name}")
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if idx < 9:
                button.setShortcut(QKeySequence(f"Ctrl+{idx+1}"))
            elif idx == 9:
                button.setShortcut(QKeySequence(f"Ctrl+0"))
            else:
                button.setShortcut(QKeySequence(f"Ctrl+Alt+{idx-9}"))
            shots_section_layout.addWidget(button, j, i)
            self.shots_button_group.addButton(button)

        ############
        # Create the other sections
        # Create a horizontal layout for the "Side" and "Effect" sections
        side_effect_layout = QHBoxLayout()

        for section_name in ["Side", "Effect", "Rally Winner"]:
            section = QGroupBox(section_name)
            section_layout = QVBoxLayout()
            section.setLayout(section_layout)
            side_effect_layout.addWidget(section)

        # Add the horizontal layout to the main column
        main_column.addLayout(side_effect_layout)

        return main_column
    
    def sidebar(self):
        """Creates the sidebar column with the following sections:"""
        # Create the first column with three sections
        # This column is on the left - sidebar
        first_column = QVBoxLayout()

        # Left 1 - Section 1 - Score
        score_section = QGroupBox('Score')
        score_section_layout = QVBoxLayout()
        self.score_button = QPushButton("0-0-2")
        score_section_layout.addWidget(self.score_button)
        score_section.setLayout(score_section_layout)
        first_column.addWidget(score_section)

        # Left 2 - Section 2 - Player
        player_section = QGroupBox("Player")
        player_section_layout = QVBoxLayout()
        player_section.setLayout(player_section_layout)
        first_column.addWidget(player_section)

        self.player_button_group = QButtonGroup()
        self.player_button_group.setExclusive(True)

        for team in ["A", "B"]:
            row_layout = QHBoxLayout()
            player_section_layout.addLayout(row_layout)
            for i in range(1, 3):
                player_button = QPushButton(f"Player {team}{i}")
                player_button.setCheckable(True)
                row_layout.addWidget(player_button)
                self.player_button_group.addButton(player_button)

        stack_section = QGroupBox("Stack")
        stack_section_layout = QVBoxLayout()
        stack_section.setLayout(stack_section_layout)
        first_column.addWidget(stack_section)

        # create the button group
        self.stack_button_group = QButtonGroup()
        self.stack_button_group.setExclusive(True)

        # Create the first row of buttons
        first_row_layout = QHBoxLayout()
        stack_section_layout.addLayout(first_row_layout)

        for stacks in ['A2 Left', 'A2 Right']:
            button = QPushButton(stacks)
            button.setCheckable(True)
            first_row_layout.addWidget(button)
            self.stack_button_group.addButton(button)

        # Create the second row of buttons
        second_row_layout = QHBoxLayout()
        stack_section_layout.addLayout(second_row_layout)

        for stacks in ['B2 Left', 'B2 Right']:
            button = QPushButton(stacks)
            button.setCheckable(True)
            second_row_layout.addWidget(button)
            self.stack_button_group.addButton(button)
            
        return first_column
