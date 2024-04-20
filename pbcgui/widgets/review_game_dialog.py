import json

from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QVBoxLayout, QDialog, QTextEdit
)

from ..data import Game


class ReviewGameDialog(QDialog):

    game_reviewed = Signal(Game)

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.setWindowTitle("Review Game")
        self.layout = QVBoxLayout()

        # Create a QTextEdit instance
        self.game_json_edit = QTextEdit()
        # Make the QTextEdit read-only
        self.game_json_edit.setReadOnly(True)
        # Convert the game object to JSON and set it as the text of the QTextEdit
        self.game_json_edit.setText(json.dumps(self.game.to_dict(), indent=4))

        # Add the QTextEdit to the layout
        self.layout.addWidget(self.game_json_edit)

    def accept(self):
        self.player_added.emit(self.game)
        super().accept()
