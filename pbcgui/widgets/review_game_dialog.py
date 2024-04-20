import json
import logging

from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QVBoxLayout, QDialog, QDialogButtonBox
)

from .log import LogWidget
from ..data import Game


class ReviewGameDialog(QDialog):

    game_reviewed = Signal(Game)

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

        # Create a QDialogButtonBox with OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Connect the accepted and rejected signals to the accept and reject slots
        self.button_box.accepted.connect(self.on_accepted)
        self.button_box.rejected.connect(self.on_rejected)

        # Add the QDialogButtonBox to the layout
        self.layout.addWidget(self.button_box)

        # Set the layout of the dialog
        self.setLayout(self.layout)

    def on_accepted(self):
        self.logger.debug(f'Game reviewed and accepted: {self.game}')
        self.game_reviewed.emit(self.game)
        super().accept()

    def on_rejected(self):
        self.logger.debug(f'Game review rejected: {self.game}')
        super().reject()

    def set_game(self, game: Game):
        self.game = game
        self.logger.debug(f'Setting game for review: {game}')
        self.log_widget.clear()
        self.log_widget.append(json.dumps(game.to_dict(), indent=4))    
