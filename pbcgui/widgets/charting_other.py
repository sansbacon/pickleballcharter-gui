from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout

#from ..entities import ShotTypes


class ChartingOtherWidget(QWidget):

    def __init__(self):
        super().__init__()

        ############
        # Create the other sections
        # Create a horizontal layout for the "Side" and "Effect" sections
        layout = QHBoxLayout()

        for section_name in ["Side", "Effect", "Rally Winner"]:
            section = QGroupBox(section_name)
            section_layout = QVBoxLayout()
            section.setLayout(section_layout)
            layout.addWidget(section)

        self.setLayout(layout)