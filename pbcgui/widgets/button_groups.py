from PySide6.QtCore import Qt

from PySide6.QtWidgets import QButtonGroup


class ArrowKeyButtonGroup(QButtonGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setExclusive(True)
        self.buttons = []

    def addButton(self, button, id=None):
        if id is None:
            super().addButton(button)
        else:
            super().addButton(button, id)
        self.buttons.append(button)
        
    def keyPressEvent(self, event):
        current_index = self.buttons.index(self.checkedButton())
        if event.key() == Qt.Key_Left:
            next_index = (current_index - 1) % len(self.buttons)
        elif event.key() == Qt.Key_Right:
            next_index = (current_index + 1) % len(self.buttons)
        else:
            return
        self.buttons[next_index].setChecked(True)