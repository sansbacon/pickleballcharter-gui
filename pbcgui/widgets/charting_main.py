from PySide6.QtWidgets import QWidget, QVBoxLayout


class ChartingMainWidget(QWidget):

    def __init__(self, shots_widget, other_widget = None):
        super().__init__()

        layout = QVBoxLayout()
        self.shots_widget = shots_widget
        self.other_widget = other_widget
        layout.addWidget(self.shots_widget)
        layout.addWidget(self.other_widget)
        self.setLayout(layout)

