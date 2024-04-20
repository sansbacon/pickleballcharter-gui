import json
import logging

from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QVBoxLayout, QDialog, QDialogButtonBox
)

from .log import LogWidget
from ..data import Game


class ReviewGameDialog(QDialog):

    game_reviewed = Signal(bool)

    def __init__(self, game: Game):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self.game = game
        self.setWindowTitle("Review Game")
        self.layout = QVBoxLayout()

        # Create a QTextEdit instance
        self.log_widget = LogWidget("Game Rallies and Metadata:")
        self.log_widget.append(json.dumps(game.to_dict(), indent=4))

        # Add the QTextEdit to the layout
        self.layout.addWidget(self.log_widget)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Add the QDialogButtonBox to the layout
        self.layout.addWidget(self.buttonBox)

        # Set the layout of the dialog
        self.setLayout(self.layout)

    def accept(self):
        self.logger.debug(f'Game reviewed and accepted!')
        self.game_reviewed.emit(True)
        super().accept()

    def reject(self):
        self.logger.debug(f'Game reviewed and rejected!')
        self.game_reviewed.emit(False)
        super().accept()

    def set_game(self, game: Game):
        self.game = game
        self.log_widget.clear()
        self.log_widget.append(json.dumps(game.to_dict(), indent=4))    
