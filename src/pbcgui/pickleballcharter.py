import sys
from PySide6.QtCore import Signal, QDate, Qt
from PySide6.QtWidgets import QDateEdit, QTableWidget, QTabWidget, QMainWindow, QLineEdit, QMenu, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSizePolicy, QGroupBox, QLabel
from PySide6.QtGui import QAction, QKeySequence, QPalette, QColor

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

class AppPalette(QPalette):
    """Sets the palette for the app"""
    def __init__(self):
        super().__init__()

        # Define colors
        white = QColor(255, 255, 255)
        light_grey = QColor(224, 224, 224)
        medium_grey = QColor(189, 189, 189)
        dark_grey = QColor(117, 117, 117)
        light_blue = QColor(144, 202, 249)
        medium_blue = QColor(33, 150, 243)
        dark_blue = QColor(25, 118, 210)

        self.setColor(QPalette.Window, QColor(240, 240, 240))  # Light grey background
        self.setColor(QPalette.WindowText, Qt.black)  # Black text on light background
        self.setColor(QPalette.Base, QColor(255, 255, 255))  # White background for input fields
        self.setColor(QPalette.AlternateBase, QColor(240, 240, 240))  # Light grey background for alternate elements
        self.setColor(QPalette.ToolTipBase, Qt.white)  # White tooltip background
        self.setColor(QPalette.ToolTipText, Qt.black)  # Black tooltip text
        self.setColor(QPalette.Text, Qt.black)  # Black text on light background
        self.setColor(QPalette.Button, QColor(240, 240, 240))  # Light grey buttons
        self.setColor(QPalette.ButtonText, Qt.black)  # Black text on buttons
        self.setColor(QPalette.BrightText, Qt.red)  # Bright red text for alerts
        self.setColor(QPalette.Link, QColor(42, 130, 218))  # Blue links
        self.setColor(QPalette.Highlight, QColor(42, 130, 218))  # Blue highlight color
        self.setColor(QPalette.HighlightedText, Qt.white)  # White text on highlighted background


class TouchscreenApp(QMainWindow):
    """Main class for charting app"""

    score_changed = Signal(tuple)

    def __init__(self, db_path:str = 'pickleballcharter.db'):
        super().__init__()
        self.score = (0, 0, 2)
        self.buttons = []
        self.button_states = {}
        self.db_handler = DatabaseHandler(db_path)
        self.initUI()
        self.setPalette(AppPalette())

    def initUI(self):
        # Create a tab widget
        self.tab_widget = QTabWidget()

        # Initialize the first and second tabs
        self.initUIMenus()
        self.initUISetupGame()
        self.initUIChartGame()

        # Set the tab widget as the central widget
        self.setCentralWidget(self.tab_widget)

    def initUIMenus(self):
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

    def initUISetupGame(self):
        first_tab = QWidget()
        main_layout = QHBoxLayout()
        first_tab.setLayout(main_layout)

        # Create a vertical layout for the buttons and fields
        first_layout = QVBoxLayout()
        main_layout.addLayout(first_layout)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        first_layout.addLayout(button_layout)

        # Add a form for creating a new game or reading an existing game
        new_game_button = QPushButton("Create New Game")
        load_game_button = QPushButton("Load Existing Game")

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

        # Connect the buttons to slots
        new_game_button.clicked.connect(self.db_handler.create_new_game)
        load_game_button.clicked.connect(self.db_handler.read_existing_game)

        # Add the first tab to the tab widget
        self.tab_widget.addTab(first_tab, "Game Setup")

    def initUIChartGame(self):
        # Create the second tab
        second_tab = QWidget()
        second_layout = QVBoxLayout()
        second_tab.setLayout(second_layout)

        # Create a horizontal layout
        layout = QHBoxLayout()

        # Create the first column with three sections
        first_column = QVBoxLayout()
        for section_name in ["Score", "Stack"]:
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

        # Add the second tab to the tab widget
        second_layout.addLayout(layout)
        self.tab_widget.addTab(second_tab, "Game Play")

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
