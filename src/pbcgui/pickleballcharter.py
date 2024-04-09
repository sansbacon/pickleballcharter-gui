import sys
from PySide6.QtCore import Signal, QDate, Qt
from PySide6.QtWidgets import QDateEdit, QTableWidget, QTabWidget, QMainWindow, QLineEdit, QMenu, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSizePolicy, QGroupBox, QLabel
from PySide6.QtGui import QAction, QKeySequence, QPalette, QColor

from charting_widgets import ChartGameWidget
from db import DatabaseHandler
from menus import AppMenuBar
from palettes import AppPalette
from utility import next_possible_scores
from setup_widgets import SetupGameWidget


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
        self.shots = {
            1: ['Serve'],
            2: ['Return'],
            3: ['Drop', 'Drive'],
            4: ['Fourth Shot'],
            5: ['Transition', 'Dink-A', 'Dink-B', 'Attack-A','Attack-B', 'Defend', 'Counter', 'Erne', 'Putaway', 'Lob']
        }
        self.players = {'A': [], 'B': []}

    def initUI(self):
        # Create a menu bar
        menu_bar = AppMenuBar(self)
        self.setMenuBar(menu_bar)  # Set the menu bar of the main window

        # Create a tab widget
        self.tab_widget = QTabWidget()

        # Initialize the first tab
        self.setup_game_widget = SetupGameWidget(self)
        self.setup_game_widget.newGameRequested.connect(self.create_new_game)  # Connect to the create_new_game method
        self.setup_game_widget.loadGameRequested.connect(self.load_existing_game)  # Connect to the load_existing_game method
        self.tab_widget.addTab(self.setup_game_widget, "Setup Game")
        
        # Initialize the second tab
        self.chart_game_widget = ChartGameWidget(self)
        self.tab_widget.addTab(self.chart_game_widget, "Chart Game")

        # Set the tab widget as the central widget
        self.setCentralWidget(self.tab_widget)

    def create_new_game(self):
        # Code to create a new game goes here
        pass

    def load_existing_game(self):
        # Code to load an existing game goes here
        pass

    def update_buttons(self):
        # Clear the Score section
        self.score_section_layout.clear()

        if self.score == (0, 0, 2):
            # If the score is 0,0,2, display a single button with the score
            button = QPushButton("0-0-2")
            self.score_section_layout.addWidget(button)
        else:
            # For any other score, display buttons with the possible next scores
            possible_scores = next_possible_scores(self.score)
            for new_score in possible_scores:
                score_str = '-'.join([str(s) for s in new_score])
                button = QPushButton(score_str)
                self.score_section_layout.addWidget(button)

    def update_button_state(self, button, checked):
        # Update the button's state in the dictionary
        self.button_states[button] = checked

    def update_score(self, new_score):
        self.score = new_score
        self.score_changed.emit(self.score)  # Emit the score_changed signal


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TouchscreenApp()
    window.showMaximized()
    sys.exit(app.exec())
