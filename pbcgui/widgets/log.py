import json

from PySide6.QtWidgets import QWidget, QVBoxLayout,QGroupBox, QTextEdit


class LogWidget(QWidget):
    """A simple widget that logs text read only"""
    def __init__(self, title="Log"):
        super().__init__()
        layout = QVBoxLayout()
        section = QGroupBox(title)
        section_layout = QVBoxLayout()
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        section_layout.addWidget(self.log_console)
        section.setLayout(section_layout)
        layout.addWidget(section)
        self.setLayout(layout)

    def append(self, text):
        self.log_console.append(text)

    def clear(self):
        self.log_console.clear()


class RallyLogWidget(LogWidget):
    """A simple widget that logs text read only"""

    def add_entity(self, e):
        text = json.dumps(e.to_dict(), indent=4)
        self.log_console.append(text)
        self.log_console.append("\n")