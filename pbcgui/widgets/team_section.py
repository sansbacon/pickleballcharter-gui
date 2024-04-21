from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QSizePolicy


class TeamSectionWidget(QWidget):
    """Creates the score section of the sidebar"""

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()   
        section = QGroupBox("Serving Team")
        section_layout = QVBoxLayout() 
        section.setLayout(section_layout)
        layout.addWidget(section)
        self.labels = []

        server_label = QLabel("Server 1")
        server_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        section_layout.addWidget(server_label)
        self.labels.append(server_label)

        team_label = QLabel("Team 1")
        team_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        section_layout.addWidget(team_label)
        self.labels.append(team_label)

        self.setLayout(layout)

    def resizeEvent(self, event):
        # Calculate the new font size based on the height of the widget.
        # You might need to adjust the factor depending on your specific needs.
        new_font_size = self.height() * 0.15
        for idx, label in enumerate(self.labels):
            font = label.font()  # Get the current font
            font.setPointSize(new_font_size)  # Set the new font size
            self.labels[idx].setFont(font)  # Apply the new font

    def update_label(self, values):
        # Update the score based on the serving team
        for idx, value in enumerate(values):
            self.labels[idx].setText(value)
