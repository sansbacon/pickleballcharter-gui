from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, Signal

# Add this to the class definition
class RallyReviewWidget(QWidget):
    """A widget for reviewing and editing rallies and shots in a game.

    Attributes:
        game (Game): The game to review.
        rallies (list): The rallies in the game.
        shots (list): The shots in the game.
        table (QTableWidget): The table for displaying and editing the rallies and shots.
        save_button (QPushButton): The button for saving changes.
    """

    game_edited = Signal(object)  # Signal emitted when the game is edited

    def __init__(self, game):
        """Initialize the widget with a game.

        Args:
            game (Game): The game to review.

        """
        super().__init__()
        self.game = game
        self.rallies = []
        self.shots = []
        self.table = QTableWidget()
        self.populate_rallies_and_shots()
        self.create_table()

        # Create Save Changes button
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)

        # Add table and button to layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def create_table(self):
        """Create the table for displaying and editing the rallies and shots."""
        self.table.setRowCount(len(self.rallies))
        self.table.setColumnCount(4)
        for i, (rally, shot) in enumerate(zip(self.rallies, self.shots)):
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))  # Rally number
            self.table.setItem(i, 1, QTableWidgetItem(str(i + 1)))  # Point number
            self.table.setItem(i, 2, QTableWidgetItem(str(rally)))  # Rally
            self.table.setItem(i, 3, QTableWidgetItem(str(shot)))   # Shot
        self.table.itemChanged.connect(self.handle_item_changed)

    def handle_item_changed(self, item):
        """Handle a change to an item in the table.

        Args:
            item (QTableWidgetItem): The item that changed.

        """
        if item.column() == 0:
            self.rallies[item.row()] = item.text()
        else:
            self.shots[item.row()] = item.text()

    def populate_rallies_and_shots(self):
        """Populate the rallies and shots from the game."""
        for rally in self.game.rallies:
            self.rallies.append(rally)
            for shot in rally.shots:
                self.shots.append(shot)

    def save_changes(self):
        """Save changes to the game and emit the game_edited signal."""
        # Emit game_edited signal with the updated Game object
        self.game_edited.emit(self.game)

    