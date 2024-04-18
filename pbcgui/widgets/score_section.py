from PySide6.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QLabel, QSizePolicy

from ..utility import score_to_string


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

    def update_label(self, score):
        # Update the score based on the winner
        self.score_label.setText(score_to_string(score))

