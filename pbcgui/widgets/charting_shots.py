from PySide6.QtWidgets import QWidget, QSizePolicy, QGridLayout, QGroupBox, QPushButton, QButtonGroup
from PySide6.QtGui import QKeySequence
from PySide6.QtCore import Signal

from ..data.entities import ShotTypes


class ChartingShotsWidget(QWidget):

    shot_type = Signal(str)

    def __init__(self, shot_types: ShotTypes):
        super().__init__()
        self.shot_types = shot_types

        # Create the "Shots" section
        layout = QGridLayout()
        section = QGroupBox("Shots")

        # Create a layout for the section
        section_layout = QGridLayout()
        section.setLayout(section_layout)

        self.buttons = []

        # Add shots buttons
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        for idx, shot_type in enumerate(shot_types):
            j = idx % 5
            i = idx // 5
            button = QPushButton(f"{shot_type.value} - {shot_type.name}")
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if idx < 9:
                button.setShortcut(QKeySequence(f"Ctrl+{idx+1}"))
            elif idx == 9:
                button.setShortcut(QKeySequence(f"Ctrl+0"))
            else:
                button.setShortcut(QKeySequence(f"Ctrl+Alt+{idx-9}"))
            section_layout.addWidget(button, j, i)
            self.button_group.addButton(button)
            self.buttons.append(button)

        layout.addWidget(section)
        self.setLayout(layout)
        self.button_group.buttonClicked.connect(self.emit_shot_type)

    def emit_shot_type(self, button):
        """Emit the shot type selected signal
        
        Args:
            button (QPushButton): The button that was clicked

        """
        self.shot_type.emit(button.text())

    def get_selected_shot(self) -> int:
        """Get the selected shot
        
        Returns:
            int: The index of the selected shot

        """
        for idx, button in enumerate(self.buttons):
            if button.isChecked():
                return self.shot_types.find(idx)    

    def reset_buttons(self):
        self.button_group.setExclusive(False)  # Disable autoExclusive
        for button in self.button_group.buttons():
            button.setChecked(False)
        self.button_group.setExclusive(True)  # Enable autoExclusive