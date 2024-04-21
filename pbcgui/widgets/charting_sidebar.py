from PySide6.QtWidgets import QWidget, QVBoxLayout


class ChartingSidebarWidget(QWidget):
    """A widget for the sidebar of the charting tab"""

    def __init__(self, player_section_widget, score_section_widget, stack_section_widget, team_section_widget):
        super().__init__()
        self.player_section = player_section_widget
        self.score_section = score_section_widget
        self.stack_section = stack_section_widget
        self.team_section = team_section_widget

        layout = QVBoxLayout()

        # Left 1 - Section 1 - Score
        layout.addWidget(self.score_section, 15)

        # Left 2 - Section 2 - Serving Team
        layout.addWidget(self.team_section, 15)

        # Left 3 - Section 2 - Player
        layout.addWidget(self.player_section, 40)

        # Left 4 - Section 3 - Stack
        layout.addWidget(self.stack_section, 30)

        self.setLayout(layout)

