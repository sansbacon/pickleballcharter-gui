from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout


class ChartTabWidget(QWidget):

    def __init__(self, sidebar_widget, main_widget):
        super().__init__()

        self.sidebar_widget = sidebar_widget
        self.main_widget = main_widget

        vlayout = QVBoxLayout()

        # Create a horizontal layout
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.sidebar_widget)
        hlayout.addWidget(self.main_widget)

        hlayout.setStretch(0, 25)
        hlayout.setStretch(1, 75)
        vlayout.addLayout(hlayout)
        self.setLayout(vlayout)
