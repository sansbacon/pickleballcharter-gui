from PySide6.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QLabel, QSizePolicy
from PySide6.QtGui import QFont

from ..utility import next_score, score_to_string, string_to_score


class ScoreSectionWidget(QWidget):
    """Creates the score section of the sidebar"""

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()   
        section = QGroupBox("Score")
        section_layout = QHBoxLayout() 
        section.setLayout(section_layout)
        layout.addWidget(section)

        self.score_label = QLabel("0-0-2")
        self.score_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        section_layout.addWidget(self.score_label)

        self.setLayout(layout)

    def resizeEvent(self, event):
        # Calculate the new font size based on the height of the widget.
        # You might need to adjust the factor depending on your specific needs.
        new_font_size = self.height() * 0.25
        font = self.score_label.font()  # Get the current font
        font.setPointSize(new_font_size)  # Set the new font size
        self.score_label.setFont(font)  # Apply the new font

    def update_score(self, winner):
        # Update the score based on the winner
        # This is just a placeholder, replace it with your actual logic
        current_score = string_to_score(self.score_label.text())
        new_score = next_score(current_score, winner)
        self.score_label.setText(score_to_string(new_score))

