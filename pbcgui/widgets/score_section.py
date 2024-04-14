from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton
from PySide6.QtCore import Signal

from ..utility import next_score, unique_names


class ScoreSectionWidget(QWidget):
    """Creates the score section of the sidebar"""

    rally_over = Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.score_section = QGroupBox('Score')
        self.score_section_layout = QVBoxLayout()
        self.score_section.setLayout(self.score_section_layout)

        self.score_button = QPushButton("0-0-2")
        self.score_section_layout.addWidget(self.score_button)

        self.server_wins_button = QPushButton("Server Wins")
        self.score_section_layout.addWidget(self.server_wins_button)

        self.receiver_wins_button = QPushButton("Receiver Wins")
        self.score_section_layout.addWidget(self.receiver_wins_button)

       # Connect the clicked signal of the buttons to a method that emits rally_over
        self.server_wins_button.clicked.connect(lambda: self.emit_rally_over("server"))
        self.receiver_wins_button.clicked.connect(lambda: self.emit_rally_over("receiver"))

    def emit_rally_over(self, winner):
        score = self.score_button.text().split('-')
        new_score = next_score(score, winner)
        self.rally_over.emit('-'.join([str(s) for s in new_score]))