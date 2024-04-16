from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

class ChartingMainWidget(QWidget):

    def __init__(self, shots_widget, other_widgets):
        super().__init__()

        layout = QVBoxLayout()
        self.shots_widget = shots_widget
        self.other_widget = self.create_other_widget(other_widgets)
        layout.addWidget(self.shots_widget, 67)
        layout.addWidget(self.other_widget, 33)
        self.setLayout(layout)

    def create_other_widget(self, other_widgets):
        main_widget = QWidget()
        layout = QHBoxLayout()
        for widget in other_widgets:
            layout.addWidget(widget)
        main_widget.setLayout(layout)
        return main_widget
        