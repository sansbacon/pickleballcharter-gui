from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton


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
        for section_name in ["Shots", "Side", "Effect", "Rally Winner"]:
            section = QGroupBox(section_name)
            section_layout = QVBoxLayout()
            section.setLayout(section_layout)
            main_column.addWidget(section)
        return main_column

    def sidebar(self):
        """Creates the sidebar column with the following sections:"""
        # Create the first column with three sections
        # This column is on the left - sidebar
        first_column = QVBoxLayout()

        # Left 1 - Section 1 - Score
        score_section = QGroupBox('Score')
        score_section_layout = QVBoxLayout()
        score_button = QPushButton("0-0-2")
        score_section_layout.addWidget(score_button)
        score_section.setLayout(score_section_layout)
        first_column.addWidget(score_section)

        # Left 2 - Section 2 - Player
        player_section = QGroupBox("Player")
        player_section_layout = QVBoxLayout()
        player_section.setLayout(player_section_layout)
        first_column.addWidget(player_section)

        for team in ["A", "B"]:
            row_layout = QHBoxLayout()
            player_section_layout.addLayout(row_layout)
            for i in range(1, 3):
                player_button = QPushButton(f"Player {team}{i}")
                player_button.setCheckable(True)
                row_layout.addWidget(player_button)

        # Left 3 - Section 3 - Stack
        stack_section = QGroupBox("Stack")
        stack_section_layout = QVBoxLayout()
        stack_section.setLayout(stack_section_layout)
        first_column.addWidget(stack_section)

        # Create the first row of buttons
        first_row_layout = QHBoxLayout()
        stack_section_layout.addLayout(first_row_layout)

        button_a2_left = QPushButton("A2 Left")
        button_a2_left.setCheckable(True)
        first_row_layout.addWidget(button_a2_left)

        button_a2_right = QPushButton("A2 Right")
        button_a2_right.setCheckable(True)
        first_row_layout.addWidget(button_a2_right)

        # Create the second row of buttons
        second_row_layout = QHBoxLayout()
        stack_section_layout.addLayout(second_row_layout)

        button_b2_left = QPushButton("B2 Left")
        button_b2_left.setCheckable(True)
        second_row_layout.addWidget(button_b2_left)

        button_b2_right = QPushButton("B2 Right")
        button_b2_right.setCheckable(True)
        second_row_layout.addWidget(button_b2_right)

        return first_column
