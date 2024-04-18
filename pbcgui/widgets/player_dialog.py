from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QLineEdit, QComboBox, QDialog, QDialogButtonBox, QLineEdit
)

from ..data import Player


class PlayerDialog(QDialog):

    player_added = Signal(Player)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Player")
        self.layout = QVBoxLayout()

        # First Name
        self.first_name_label = QLabel("First Name:")
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setFocus()
        self.layout.addWidget(self.first_name_label)
        self.layout.addWidget(self.first_name_edit)

        # Last Name
        self.last_name_label = QLabel("Last Name:")
        self.last_name_edit = QLineEdit()
        self.layout.addWidget(self.last_name_label)
        self.layout.addWidget(self.last_name_edit)

        # Nickname
        self.nickname_label = QLabel("Nickname:")
        self.nickname_edit = QLineEdit()
        self.layout.addWidget(self.nickname_label)
        self.layout.addWidget(self.nickname_edit)

        # Gender
        self.gender_label = QLabel("Gender:")
        self.gender_list = QComboBox()
        self.gender_list.setEditable(False)
        self.gender_list.addItems(['Male', 'Female', 'Other'])
        self.layout.addWidget(self.gender_label)
        self.layout.addWidget(self.gender_list)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def accept(self):
        player = self.get_data()
        self.player_added.emit(player)
        super().accept()

    def get_data(self):
        return Player(**{
          'first_name': self.first_name_edit.text(),
          'last_name': self.last_name_edit.text(),
          'nickname': self.nickname_edit.text(),
          'gender': self.gender_list.currentText()
        })


