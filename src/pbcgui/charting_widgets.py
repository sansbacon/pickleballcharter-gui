from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton


class ChartGameWidget(QWidget):
    def __init__(self, parent=None):
        super(ChartGameWidget, self).__init__(parent)

        vlayout = QVBoxLayout()
        self.setLayout(vlayout)

        # Create a horizontal layout
        hlayout = QHBoxLayout()

        # Create the first column with three sections
        first_column = QVBoxLayout()
        for section_name in ["Score", "Stack"]:
            section = QGroupBox(section_name)
            section_layout = QVBoxLayout()
            section.setLayout(section_layout)
            first_column.addWidget(section)

            # If this is the "Score" section, add a button to it
            if section_name == "Score":
                button = QPushButton("0-0-2")
                button.setCheckable(True)  # Make the button checkable
                section_layout.addWidget(button)

        # Create the second column with two sections
        second_column = QVBoxLayout()
        second_column.setStretch(0, 25)  # First box takes up 25% of the space
        second_column.setStretch(1, 75)  # Second box takes up 75% of the space

        for section_name in ["Player", "Shot"]:
            section = QGroupBox(section_name)
            section_layout = QVBoxLayout()
            section.setLayout(section_layout)
            second_column.addWidget(section)

        # Create the third column
        third_column = QVBoxLayout()
        for section_name in ["Outcome", "Action"]:
            section = QGroupBox(section_name)
            section_layout = QVBoxLayout()
            section.setLayout(section_layout)
            third_column.addWidget(section)

        hlayout.addLayout(first_column)
        hlayout.addLayout(second_column)
        hlayout.addLayout(third_column)

        hlayout.setStretch(0, 25)  # First column takes up 25% of the space
        hlayout.setStretch(1, 50)  # Second column takes up 50% of the space
        hlayout.setStretch(2, 25)  # Third column takes up 25% of the space

        # Add the second tab to the tab widget
        vlayout.addLayout(hlayout)
