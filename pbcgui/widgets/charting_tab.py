from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .log import LogWidget


class ChartTabWidget(QWidget):

    def __init__(self, sidebar_widget, main_widget, log_widget):
        super().__init__()

        self.sidebar_widget = sidebar_widget
        self.main_widget = main_widget
        self.log_widget = log_widget

        vlayout = QVBoxLayout()

        # Create a horizontal layout
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.sidebar_widget)
        hlayout.addWidget(self.main_widget)
        hlayout.addWidget(self.log_widget)

        hlayout.setStretch(0, 15)
        hlayout.setStretch(1, 60)
        hlayout.setStretch(2, 25)
        vlayout.addLayout(hlayout)
        self.setLayout(vlayout)
