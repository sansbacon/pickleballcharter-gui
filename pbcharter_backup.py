import sys
from PySide6.QtCore import Signal, QDate
from PySide6.QtWidgets import QDateEdit, QFormLayout, QTabWidget, QMainWindow, QLineEdit, QMenu, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSizePolicy, QGroupBox, QLabel
from PySide6.QtGui import QAction, QKeySequence

from tinydb import TinyDB, Query


class DatabaseHandler:
    def __init__(self, db_path):
        self.db = TinyDB(db_path)

    def create_new_game(self):
        self.db.insert({'type': 'game', 'status': 'new'})

    def read_existing_game(self):
        Game = Query()
        game = self.db.search(Game.type == 'game')
        return game

    # Add more methods for other database operations as needed

class TouchscreenApp(QMainWindow):
    score_changed = Signal(tuple)  # Define a custom signal that emits a tuple

    def __init__(self, db_path:str = 'pickleballcharter.db'):
        super().__init__()
        self.db_handler = DatabaseHandler(db_path)

        # Create a tab widget
        tab_widget = QTabWidget()

        # Create the first tab
        first_tab = QWidget()
        first_layout = QVBoxLayout()
        first_tab.setLayout(first_layout)

        # Add a form for creating a new game or reading an existing game
        form_layout = QFormLayout()
        new_game_button = QPushButton("Create New Game")
        read_game_button = QPushButton("Read Existing Game")
        form_layout.addRow(new_game_button)
        form_layout.addRow(read_game_button)
        first_layout.addLayout(form_layout)

        """
                        # Make additions to setup section
                # Create the first column with a "Setup" section
                if section_name == 'Setup':
                    # Add labels and widgets for Game Date, Game Location, and Players
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

            
            """


        # Connect the buttons to slots
        new_game_button.clicked.connect(self.create_new_game)
        read_game_button.clicked.connect(self.read_existing_game)

        # Add the first tab to the tab widget
        tab_widget.addTab(first_tab, "Game Setup")

        ###########################
        # SECOND TAB
        ###########################
        second_tab = QWidget()

        self.score = (0, 0, 2)  # Initialize the score
        self.buttons = []  # Store the buttons in a list
        self.button_states = {}

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a horizontal layout
        layout = QHBoxLayout()

        # Create the first column with three sections
        first_column = QVBoxLayout()
        for section_name in ["Setup", "Score", "Stack"]:
            section = QGroupBox(section_name)
            section_layout = QVBoxLayout()
            section.setLayout(section_layout)
            first_column.addWidget(section)


            # If this is the "Score" section, add a button to it
            if section_name == "Score":
                button = QPushButton("0-0-2")
                button.setCheckable(True)  # Make the button checkable
                button.clicked.connect(lambda: button.setStyleSheet("background-color: #abcdef"))
                button.clicked.connect(lambda checked, button=button: self.update_button_state(button, checked))
                section_layout.addWidget(button)

        # Create the second column with two sections
        second_column = QVBoxLayout()
        second_column.setStretch(0, 25)  # First box takes up 25% of the space
        second_column.setStretch(1, 75)  # Second box takes up 75% of the space

        for section_name in ["Player", "Shot"]:
            section = QGroupBox(section_name)
            section_layout = QVBoxLayout()
            section.setLayout(section_layout)
            second_column.addWidget(section)

        # Create the third column
        third_column = QVBoxLayout()
        for section_name in ["Outcome", "Action"]:
            section = QGroupBox(section_name)
            section_layout = QVBoxLayout()
            section.setLayout(section_layout)
            third_column.addWidget(section)


        layout.addLayout(first_column)
        layout.addLayout(second_column)
        layout.addLayout(third_column)

        layout.setStretch(0, 25)  # First column takes up 25% of the space
        layout.setStretch(1, 50)  # Second column takes up 50% of the space
        layout.setStretch(2, 25)  # Third column takes up 25% of the space

        central_widget.setLayout(layout)

        ## MENU BAR
        menu_bar = self.menuBar()

        # Add a File menu with a Quit action
        file_menu = QMenu("File", self)
        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence.Quit)  # Set the shortcut to Ctrl+Q
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        menu_bar.addMenu(file_menu)

        # Add an Edit menu
        edit_menu = QMenu("Edit", self)
        # Add a standard "Copy" action
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)  # Set the shortcut to Ctrl+C
        edit_menu.addAction(copy_action)
        menu_bar.addMenu(edit_menu)

        # Add a Help menu
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)
        # Connect the score_changed signal to the update_buttons slot
        self.score_changed.connect(self.update_buttons)

    def update_button_state(self, button, checked):
        # Update the button's state in the dictionary
        self.button_states[button] = checked

    def update_score(self, new_score):
        self.score = new_score
        self.score_changed.emit(self.score)  # Emit the score_changed signal

    def update_buttons(self):
        # Clear the Score section
        self.score_section_layout.clear()

        if self.score == (0, 0, 2):
            # If the score is 0,0,2, display a single button with the score
            button = QPushButton("0-0-2")
            self.score_section_layout.addWidget(button)
        else:
            # For any other score, display buttons with the possible next scores
            possible_scores = self.next_possible_scores(self.score)
            for new_score in possible_scores:
                score_str = '-'.join([str(s) for s in new_score])
                button = QPushButton(score_str)
                self.score_section_layout.addWidget(button)

    @staticmethod
    def next_possible_scores(score):
        server_score, returner_score, server_number = score

        # If the server wins the rally, they score a point
        server_wins = (server_score + 1, returner_score, server_number)

        # If the returner wins the rally, they become the server, but don't score a point
        # The server number switches between 1 and 2
        returner_wins = (server_score, returner_score, 2 if server_number == 1 else 1)

        return [server_wins, returner_wins]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TouchscreenApp()
    window.showMaximized()
    sys.exit(app.exec())
