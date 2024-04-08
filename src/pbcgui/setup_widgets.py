from PySide6.QtCore import QDate, Signal

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QSizePolicy, QGroupBox,
    QLabel, QDateEdit, QLineEdit, QTableWidget
)


class SetupGameWidget(QWidget):

    newGameRequested = Signal()  # Signal for requesting a new game
    loadGameRequested = Signal()  # Signal for requesting to load a game

    def __init__(self, parent=None):
        super(SetupGameWidget, self).__init__(parent)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Create a vertical layout for the buttons and fields
        first_layout = QVBoxLayout()
        main_layout.addLayout(first_layout)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        first_layout.addLayout(button_layout)

        # Add a form for creating a new game or reading an existing game
        new_game_button = QPushButton("Create New Game")
        new_game_button.clicked.connect(self.newGameRequested.emit) 
        load_game_button = QPushButton("Load Existing Game")
        load_game_button.clicked.connect(self.loadGameRequested.emit)

        # Set the size policy of the buttons to expanding in the vertical direction
        new_game_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        load_game_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        button_layout.addWidget(new_game_button)
        button_layout.addWidget(load_game_button)

        # Add labels and widgets for Game Date, Game Location, and Players
        section = QGroupBox("Game Information")
        section_layout = QVBoxLayout()
        section.setLayout(section_layout)

        game_date_label = QLabel("Game Date")
        game_date_picker = QDateEdit()
        game_date_picker.setDate(QDate.currentDate())  # Set the default date to today's date
        game_date_picker.setCalendarPopup(True)  # Show a calendar popup
        game_date_picker.setDisplayFormat("MMMM d, yyyy")  # Set the display format to "March 24, 2024"
        section_layout.addWidget(game_date_label)
        section_layout.addWidget(game_date_picker)

        game_location_label = QLabel("Game Location")
        game_location_edit = QLineEdit()
        section_layout.addWidget(game_location_label)
        section_layout.addWidget(game_location_edit)

        for i in range(1, 5):
            player_label = QLabel(f"Player {i}")
            player_edit = QLineEdit()
            section_layout.addWidget(player_label)
            section_layout.addWidget(player_edit)

        # Add the section to the main layout
        first_layout.addWidget(section)
        first_layout.setStretchFactor(button_layout, 33)
        first_layout.setStretchFactor(section, 67)

        # Create a table widget for displaying the games
        games_table = QTableWidget()
        games_table.setColumnCount(5)  # Set the number of columns
        games_table.setHorizontalHeaderLabels(["Game ID", "Game Date", "Game Location", "Player 1", "Player 2"])  # Set the column headers
        main_layout.addWidget(games_table)

